# SECRET SANTA telegram bot

Telegram bot to create and participate in Secret Santa events.

## How to install

Python should already be installed. The project is tested on Python3.11. The project should work fine with 3.10 and newer versions, but YMMV. 

Download or clone the project.

Using virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) is recommended for project isolation.

Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```

Create SQLite database
```commandline
python manage.py migrate
```

Set up environmental variables. 
To configure those settings, create `.env` file in root folder (or rename `.env.example` to `.env`) and write down the following variables:
- `SECRET_KEY` - A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
- `DEBUG` - A boolean that turns on/off debug mode. If your app raises an exception when DEBUG is True, Django will display a detailed traceback, including a lot of metadata about your environment, such as all the currently defined Django settings (from settings.py).
- `ALLOWED_HOSTS` - A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. [See details at Django docs.](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts)
- `TELEGRAM_TOKEN` - Access token of your bot. You get one from [BotFather Telegram bot](https://t.me/BotFather) when you create a bot.

Start a dev server
```commandline
python manage.py runserver
```

## How to use
Run the bot
```commandline
python manage.py runbot
```

To use the bot as a Secret Santa game organizer, start the bot with the regular `/start` command.

To use it as a player to sign up for an existing game, follow special link to bot (should be sent by the organizer). The link will look like: `https://t.me/<your_bot_name>?start=<game_id>`

## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).