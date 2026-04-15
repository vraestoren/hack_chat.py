# <img src="https://hack.chat/favicon.ico" width="28" style="vertical-align:middle;" /> hack_chat.py

> Web API wrapper for [hack.chat](https://hack.chat) a minimal, distraction-free chat platform.

## Installation

```bash
pip install websocket-client
```

## Quick Start

```python
from hack_chat import HackChat

def greet_user(chat, message, user):
    if "hello" in message.lower():
        chat.send_message(f"Wassup {user}!")

bot = HackChat(nickname="WelcomeBot", channel="programming")
bot.on_message += [greet_user]
bot.listen()
```

## Usage

### Connecting

```python
# Anonymous
bot = HackChat(nickname="MyBot", channel="programming")

# With password
bot = HackChat(nickname="MyBot", password="secret", channel="programming")
```

### Events

```python
def on_message(chat, message, user):
    print(f"{user}: {message}")

def on_join(chat, user):
    print(f"{user} joined")

def on_leave(chat, user):
    print(f"{user} left")

def on_statistics(chat, text):
    print(f"Stats: {text}")

bot.on_message += [on_message]
bot.on_join += [on_join]
bot.on_leave += [on_leave]
bot.on_statistics += [on_statistics]

bot.listen()
```

### Messaging

```python
bot.send_message("Hello, everyone!")
bot.send_message_to("alice", "Hey, just you.")
```

### Room

```python
bot.change_nickname("NewName")
bot.move_to_channel("lounge")
bot.invite_user("alice")
bot.request_statistics()
```

### Moderation
> Requires admin or moderator password.

```python
bot.kick_user("spammer")
bot.ban_user("spammer")
bot.unban_user("192.168.1.1")
bot.add_moderator("alice")
bot.save_config()
```

## API Reference

| Method | Description |
|---|---|
| `send_message(message)` | Send a message to the channel |
| `send_message_to(nickname, message)` | Send a private message |
| `change_nickname(nickname)` | Change your nickname |
| `move_to_channel(channel)` | Move to a different channel |
| `invite_user(nickname)` | Invite a user to your channel |
| `request_statistics()` | Request server statistics |
| `kick_user(nickname)` | Kick a user *(mod only)* |
| `ban_user(nickname)` | Ban a user *(mod only)* |
| `unban_user(ip)` | Unban an IP *(mod only)* |
| `add_moderator(nickname)` | Promote a user to moderator *(mod only)* |
| `save_config()` | Save server config *(mod only)* |
| `listen()` | Start listening for events |
