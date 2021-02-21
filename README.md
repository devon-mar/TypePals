# TypePals 💻
TypePals is a new Discord bot used to vent or send out message requests, and for
strangers to anonymously respond with nice messages! 
 
We hope you find versatility in our bot to spark connections with strangers while maintaining 
anonymity or finding a space to vent your problems!

If you don't find a need to vent or request advice, feel free to send out some sweet messages to 
lift others up! 😊

 
## Intended Use 👍
We hope this bot is used with good intentions to help others when they are feeling down and in 
 return you can vent or ask for help whenever you'd also like. The benefit of anonymity helps you
 to vent without feeling concerns of privacy, but, still receive a personal responses from another
 human being! 😄 We would be overjoyed if this bot helps you through hard times!
 
## Features 🙌
### General
- All messaging privately done in your DMs with the bot! No need to worry about others peeping
 your messages in the server! 🤫
 
- Communicate with the bot by directly messaging them or simple commands!
- Feel free to shamelessly vent your problems with complete privacy! 🔒
- Responses are printed onto a letter jpg instead of just a block of text!
- Messages limited to 400 characters so it is kept concise and space efficient!
- Filter to ensure hateful messages are kept out of the system, including variations of many
different words! 🛑


### Usage
- Send out messages/requests! Vent your problems or request for advice from strangers online in
 complete privacy!
 
- Channel your inner sage and reply to others' requests whenever you feel like it!
- View the responses to your messages/requests when you would like!
- Send out nice messages to others to make their day better! 😀

### Commands 🔌 :gear:
Command | Usage
--------|------------
<message/request> | Message the bot with any messages/requests to be sent out to others
/read | Look at others' messages/requests and reply to them as you like
/responses | View responses to your messages/requests
/help | Brings up a quick menu to remind you of commands

## Setup 🔨
1. ```git clone``` the repository

2. Extract the zip file into a folder
3. Create a ```.txt``` file, but change its name to just ```.env```! 
    3. **Note that there is NO name in front of  ```.env```**
4. Open up the newly created ```.env``` file using Notepad or another of your choice
5. Follow the ```Creating a Bot Account``` on this site:
```https://discordpy.readthedocs.io/en/latest/discord.html```
6. Copy the token from step 7 (of the site)
7. Within ```.env```, there are **three** lines you can add:
    7. ```DISCORD_TOKEN = <the_token_you_obtained_from_the_prior_sites>```
        7. REQUIRED
    7. ```DELETE_THRESHOLD = <integer_greater_than_0>``` 
        7. OPTIONAL - More information in Questions section
    7. ```DATABASE_URL = <example_address_in_questions>``` 
        7. OPTIONAL - More information in Questions section
8. Go back to ```https://discordpy.readthedocs.io/en/latest/discord.html``` and complete the 
```Inviting Your Bot``` section
9. Run ```bot.py``` file and your bot should turn Online on Discord
10. Directly message the bot whenever you feel like it! 🎉

### Questions 🆘
- How do I send out a message to vent my problems or request for advice?
    - Simply direct message the bot like you were messaging anyone else on Discord! It will reply 
    with a green check if it is properly received!
    
- How do I reply to other people?
    - Use the command ```/read``` to view others' messages. You can use Discord's own reply feature
    by right clicking the message then using ```Reply``` in order to send back a response!
    
- How do I view responses people sent back to my messages?
    - Use the command ```/responses``` to see your responses on letters!

```.env``` variable  | Usage
---------------------|------
```DISCORD_TOKEN``` | Used to specifically link your ```bot.py``` with the Discord bot
```DELETE_THRESHOLD``` | Limits how many responses a message can get before the message is removed from the pile of messages!
```DATABASE_URL``` | Allows for messages to be kept even after turning off ```bot.py```

- What happens if I don't have a ```DATABASE_URL```?
    - The messages and responses are all deleted when you turn off ```bot.py```, so if you want to
    keep them even after turning off the bot, you will need a ```DATABASE_URL```!
         
- What happens if it goes over the ```DELETE_THRESHOLD``` and I haven't used ```/responses``` to
view responses to my messages?
    - Don't worry! Your messages remain past the ```DELETE_THRESHOLD``` until you use 
    ```/responses``` to view the responses! Note that if you DO NOT have a ```DATABASE_URL```, it will
    still be deleted when you turn off ```bot.py```.
    
- What should a ```DATABASE_URL``` look like?
    - ```sqlite:////tmp/test.db```
