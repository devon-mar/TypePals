import discord
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MessageRequest(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    message = Column(String(400))
    # The user who sent out this request so that we can send them their responses
    user_id = Column(Integer)
    responses = relationship("Response", backref="original_message", lazy="dynamic")
    replied = Column(Boolean)
    sent = Column(Boolean)

    def __repr__(self) -> str:
        return f"<MessageRequest {self.id}>"

    async def send(self, channel, session):
        """
        Send the message request to a channel to be replied to or just read
        """
        await Response.send(self, channel, session)

    @classmethod
    async def create(cls, message, user_id, session):
        mr = cls(
            message=message,
            user_id=user_id,
            replied=False,
            sent=False,
        )
        session.add(mr)
        session.commit()

    def delete(self, session):
        for r in self.responses:
            session.delete(r)
        session.delete(self)
        session.commit()


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    # Replys to this discord message id are responses to the original message
    discord_message = Column(Integer, unique=True)
    # The message that this is a reply to
    reply_to = Column(Integer, ForeignKey("requests.id"))
    # The content of the reply
    message = Column(String(400), nullable=True)
    user_id = Column(Integer)

    def __repr__(self) -> str:
        return f"<Response {self.id}>"

    @classmethod
    async def send(cls, original: MessageRequest, channel, session):
        r = cls()
        sent_msg = await channel.send(original.message)
        r.discord_message = sent_msg.id
        original.responses.append(r)
        session.commit()

    async def set_message(self, msg: discord.Message, session: Session) -> None:
        self.user_id = msg.author.id
        self.message = msg.content
        session.commit()
