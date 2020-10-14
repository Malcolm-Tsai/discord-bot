# Discord-Bot

Discord bot with a few basic commands, developed in python

## Steps to setup the bot

Ensure you have Python 3 correctly installed on your host device with pip

**Create a bot on the discord developer portal**.
To do so you must have a discord account and then you must follow these steps, and retrieve your token (5th picture): https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token

**Next, download the project and change directory into the project directory at the first level and run the requirements.txt like this:** pip install -r requirements.txt

**Next go to https://code.google.com/apis/console while logged into a google account and create a project and retrieve it's API key and console id (or cse_id)**

Finally, in config.json in the project folder, edit the values of the config according to A) what you want to name the bot, B) the google api key you created C) the google console id you created and D) the discord bot token you created.

## Usage

To run the you must be in the local directory of bot.py

Type 'python bot.py' to run the bot and momentarily you will see '{your bot name} online'

Command examples
```
Search youtube for video: .yt charlie bit my finger 
Search for recipe: .recipe apple pie
Ask 8 ball question: .8ball will it rain today
Get weather info about a city: .w ottawa
Translate text: .tr en J'aime la pizza
Google search: .g what is the mass–energy equivalence equation
Image search: .image unicorn
```

## Author

Malcolm Tsai
