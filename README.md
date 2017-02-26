# slackbot

… simple slack bot

* register the bot at your https://slack.com/apps/manage/custom-integrations
* get the token
* install dependencies
* configure systemd service and install it (or set environment variables for cli)


## Install for development:

requires python 3.5, uses asyncio, and the stuff from requirements.txt:

```
export PYTHONUSERBASE=$PWD/py-env
pip install --user -e .
```

## Usage:

```
export PYTHONUSERBASE=$PWD/py-env
python -m slackbot --help
```


## Setup a systemd service

Create a user for the bot, the example file uses `slackbot`.
I haven't published the code to pypi, so install the bot from git to `/opt/slackbot`.
If you use some other directory change `PYTHONUSERBASE=` below and in the service file.


```
export PYTHONUSERBASE=/opt/slackbot
pip install --user git+https://github.com/gdamjan/slackbot@master#egg=slackbot
```

Then copy the `slackbot.service` to `/etc/systemd/system/` and start it, or enable it, or both:

```
sudo systemctl start slackbot
# or
sudo systemctl enable slackbot
# or
sudo systemctl enable --now slackbot
```

Don't forget to set the slack access token (and run `systemctl daemon-reload` after you edit the service file).
