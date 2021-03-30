# Discord-Study-Bot
<p align="left">
<a href="https://github.com/shubhayu-64/Discord-Study-Bot/blob/main/LICENSE" alt="Lisence"><img src="https://img.shields.io/github/license/shubhayu-64/Discord-Study-Bot"></a> <a href="https://github.com/shubhayu-64/Discord-Study-Bot/issues" alt="Issues"><img src="https://img.shields.io/github/issues/shubhayu-64/Discord-Study-Bot"></a> <a href="https://twitter.com/intent/follow?screen_name=shubhayu64" alt="Twiter-Follow"><img src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2Fshubhayu64"></a>
</p>

Discord-Study-Bot is an open-source solution for implementing a Study-Time-based leaderboard system in discord servers. This features an Overall leaderboard and leaderboards based on a Daily, Weekly, and Monthly basis.

## Features

- Global Study-Time Leaderboard   ​
- Monthly Study-Time Leaderboard
- Weekly Study-Time Leaderboard
- Daily Study-Time Leaderboard

## Installation

1. Clone the repo or download manually.
```bash
git clone https://github.com/shubhayu-64/Discord-Study-Bot.git
``` 
2. Move to cloned/downloaded directory ``` cd Discord-Study-Bot```
3. Use [pip](https://pip.pypa.io/en/stable/) to install Discord-Study-Bot. 
```bash
pip install -r requirements.txt
```
4. Make a bot from [Discord Developer Portal](https://discord.com/developers/applications) and grab the token and fill in token.txt
5. Make a remote database in [MongoDB](https://www.mongodb.com/) and fill in database.py with your cluster, database, and collection.


## Deploy on heroku
- Create a new app in heroku and choose your relevant region.
- Fork this repo and make it private. 
- Add your API keys or follow 4. and 5. of Installation.
- Add a Procfile with worker as study-bot.py
- Add deployment method as Github in the website.
- Go ahead and deploy on heroku.

## Usage

- Join your Discord bot on your server.
- Build Study text and voice channel and add them in study-bot.py<br><br>
![Study Channels](https://i.pinimg.com/originals/2d/b7/43/2db74372de4cbc31f22e5515bfca06e0.png)<br><br>
- Replace Channel IDs with your channel IDs.
- Add your studying discord role.<br><br>
![Studing Role](https://i.pinimg.com/originals/56/7e/83/567e8373382d1a13973beed20a2f1751.png)<br><br>
- Run ``` python study-bot.py```
- Type ``` +help``` in your server.

## FAQ

* I don't see my bot on my server!<br>
     Invite it by using this URL: https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot<br>
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
