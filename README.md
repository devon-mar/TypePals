# TypePals 💻
TypePals is a new Discord bot used to vent or send out message requests, and for
strangers to anonymously respond with nice messages! 
 
We hope you find versatility in our bot to spark connections with strangers while maintaining 
anonymity or finding a space to vent your problems!

If you don't find a need to vent or request advice, feel free to send out some sweet messages to 
lift others up! 😊

 
## Intended Use
This bot was designed for those who need a space to vent or look for some unbiased advice while
maintaining anonymity. In return, others can also use this space to write out nice comments for
others to view or reply to those in need of someone else's opinion! 😄
 
## Features
### General
- All messaging privately done in your DMs with the bot! No need to worry about others peeping
 your messages in the server!
- Communicate with the bot by directly messaging them or simple commands!
- Feel free to shamelessly vent your problems with complete privacy!
- Messages limited to 400 characters so it is kept concise and space efficient!


### Usage
- Send out messages/requests! Vent your problems or request for advice from strangers online in
 complete privacy!
- Channel your inner sage and reply to others' requests whenever you feel like it!
- View the responses to your messages/requests when you would like!

### Commands
Command | Usage
--------|------------
<message/request> | Message the bot with any messages/requests to be sent out to others
/read | Look at others' messages/requests and reply to them as you like
/responses | View responses to your messages/requests
/help | Brings up a quick menu to remind you of commands

## Setup
1. Download the zip file from the green "Code" button above

2. Extract the zip file into a folder
3. Create a ```.txt``` file, but change its name to just ```.env```! 
    3. **Note that there is NO name in front of  ```.env```**
4. Open up the newly created ```.env``` file using Notepad or another of your choice
5. Follow the ```Creating a Bot Account``` on this site:
```https://discordpy.readthedocs.io/en/latest/discord.html```
6. Copy the token from step 7 (of the site)
7. Within ```.env```, you will have to add in **THREE** lines:
    7. ```DISCORD_TOKEN = <the_token_you_obtained_from_the_prior_sites>```
    7. ```DELETE_THRESHOLD = <integer_greater_than_0>``` 
        7. More information in the Questions section
    7. ```DB_URI = <database_URI>``` 
        7. Ignore this if you aren't sure what this is. More information in the Questions section
8. Go back to ```https://discordpy.readthedocs.io/en/latest/discord.html``` and complete the 
```Inviting Your Bot``` section
9. Run ```bot.py``` file and your bot should turn Online on Discord
10. Message the bot whenever you feel like it!

### Questions
- How do I send out a message to vent my problems or request for advice?
    - Simply message the bot like you were messaging anyone else on Discord! It will reply with a 
    green check if it is properly received!
    
- How do I reply to other people?
    - Use the command ```/read``` to view others' messages. You can use Discord's own reply feature
    by right clicking the message then using ```Reply``` in order to send back a response!
    
- How do I view responses people sent back to my messages?
    - Use the command ```/responses``` to see your responses on letters!
    
- What is ```DISCORD_TOKEN``` used for?
    - It specifically links ```bot.py``` with the Discord bot so it knows what commands to use.
    
- What is ```DELETE_THRESHOLD``` used for?
    - It limits how many responses a message can get before the message is removed from the pile of
    other messages! Note that a message won't be deleted until ```/responses``` is used by the 
    person who wrote the original message!
    
- What is ```DB_URI``` used for?
    - Without a ```DB_URI```, messages are deleted the moment the bot stops running. So it is 
    required if you want the messages to be stored even when the bot is shut down.
    - An example of what one should look like: ```sqlite:////tmp/test.db```

