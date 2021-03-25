# Discord-Study-Bot

Discord-Study-Bot is an open-source solution for implementing a Study-Time-based leaderboard system in discord servers. This features an Overall leaderboard and leaderboards based on a Daily, Weekly, and Monthly basis.

## Features

- Global Study-Time Leaderboard   ​
- Monthly Study-Time Leaderboard
- Weekly Study-Time Leaderboard
- Daily Study-Time Leaderboard

## Installation

1. Clone the repo or download manually.
```bash
https://github.com/shubhayu-64/Discord-Study-Bot.git
``` 
2. Move to cloned/downloaded directory ``` cd Discord-Study-Bot```
3. Use [pip](https://pip.pypa.io/en/stable/) to install Discord-Study-Bot. 
```bash
pip install -r requirements.txt
```
4. Make a bot from [Discord Developer Portal](https://discord.com/developers/applications) and grab the token and fill in token.txt
5. Make a remote database in [MongoDB](https://www.mongodb.com/) and fill in database.py with your cluster, database, and collection.


## Usage

- Join your Discord bot on your server.
- Build Study text and voice channel and add them in study-bot.py
- Replace Channel IDs with your channel IDs.
- Add your studying discord role.
- Run ``` python study-bot.py```
- Type ``` +help``` in your server.

## FAQ

* I don't see my bot on my server!<br>
     Invite it by using this URL: https://discordapp.com/oauth2/authorize? 
      client_id=CLIENT_ID&scope=bot<br>
     Remember to replace CLIENT_ID with your bot client ID
* There aren't that many commands here...<br>
      Have any suggestion for a feature? Feel free to raise an issue.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT © Shubhayu Majumdar](https://github.com/shubhayu-64/Discord-Study-Bot/blob/main/LICENSE/)

## What next?
I will be working on deploying it on heroku. Add more interesting features related to studying in discord. 
