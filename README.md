# slackbot

… simple slack bot

* register the bot at your https://slack.com/apps/manage/custom-integrations
* get the token
* install dependencies
* configure systemd service and install it (or set environment variables for cli)


## Install

requires python 3.5, uses asyncio, and the stuff from requirements.txt:

```
PYTHONUSERBASE=$PWD/py-env pip install --user -r requirements.txt
```


## Use

```
export PYTHONUSERBASE=$PWD/py-env
python -m slackbot --help
```
