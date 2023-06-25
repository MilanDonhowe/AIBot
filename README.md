# AIBot
Boilerplate discord.py + openAI bot w/ sqlite3 for customizable bots that you can easily run.

It is automatically setup to save message history (per-user) in a sqlite database.

## Running the Bot:

1. Create a .env file with your OpenAI & Discord Bot tokens.
Example .env content (these are fake keys/tokens):
```
OPENAI_API_KEY=sk-3242hksdghrekug34gkfhrgeeriguh
DISCORD_TOKEN=MWY3ZjY4ZDhjNjllMGYzZj.g4OGM3NjYzMWNlNTc1ZjVmZDNiZGFmNzQy.N2E4MWQxZWVjZDRiYjFhYzAzNjhiZA==
```

2. Customize the starting bot prompt in `prompt.py`
For instance:
```python
intro =  [
    ("system", "You are a Discord Bot that should translate messages from english to morse code.", 0),
    ("user", "hello there", 0),
    ("assistant", ".... . .-.. .-.. --- / - .... . .-. .", 0)
]
```

Then you can run the bot in python via:
```python3 bot.py```

For continuous deployment on a linux server, I'd recommend using a [systemd service](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system_administrators_guide/chap-managing_services_with_systemd) but frankly any solution you prefer also works.

## References
- [discord.py docs](https://discordpy.readthedocs.io/en/stable/index.html)
- [OpenAI docs](https://platform.openai.com/docs/api-reference/chat)
- [OpenAI python library](https://github.com/openai/openai-python)
- [sqlite3 python reference](https://docs.python.org/3/library/sqlite3.html)
