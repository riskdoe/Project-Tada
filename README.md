# Project Tada

A sub par proto type for a twitch bot that im writing for my final assessment as open polytechnic
Frontend build using htmx, tailwind and some Jinja2Templates
Refreshes elements on the page just by doing a html get request.

todo: find a way to get the server to tell the webapp to update rather then requesting a update every second for each element

## current UI
![brave_KaXdiH8wH7](https://github.com/riskdoe/Project-Tada/assets/91177665/deab3c35-7c1a-4b0a-9a37-638a6aff2c87)

(where command is mostly built for people that play mabinogi but can be edited or removed)

# Set up

Check the wiki page for the setup (https://github.com/riskdoe/Project-Tada/wiki/1:-Setup)

tldr
install python, install git
```
git clone https://github.com/riskdoe/Project-Tada.git
cd Project-Tada
pip install -r requirements.txt
python ./app.py
```

make sure to update the config in `config.json`

*only tested on windows. should work on linux just fine. no idea about mac*


## Libarys used
- https://github.com/Teekeks/pyTwitchAPI v4.1.0
- https://github.com/tiangolo/fastapi v0.109.0
- https://github.com/maces/fastapi-htmx 0.4.0
- https://github.com/encode/uvicorn v0.26.0


