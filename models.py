class MessageRequest:
    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id
        self.reply_id = None
        self.replied = False
        self.sent = False

    async def send(self, channel):
        """
        Send the message request to a user
        """
        self.sent = True
        sent_msg = await channel.send(self.message)
        self.reply_id = sent_msg.id
