# 02. Bot Lifecycle

A Discord bot is usually a long-running process:

1. Load configuration.
2. Create a client/bot object.
3. Choose intents.
4. Register/load command modules.
5. Connect to Discord Gateway.
6. Receive events.
7. Respond through library calls that use Discord's APIs.

In this repo, `main.py` does that with `discord.py`.

```mermaid
sequenceDiagram
    participant Process as Python process
    participant Bot as discord.py Bot
    participant Discord as Discord Gateway/API
    participant DB as SQLite

    Process->>Bot: create MyBot and dmbot
    Bot->>DB: init_db(), done_init_db(), dm_init_db()
    Bot->>Bot: load cogs
    Bot->>Discord: login with bot token
    Discord-->>Bot: READY event
    Bot->>Discord: sync slash commands
    Discord-->>Bot: command/events over Gateway
    Bot->>DB: read/write todos and settings
    Bot->>Discord: send response or DM
```

## How This Maps To `main.py`

| Code | Meaning |
| --- | --- |
| `commands.Bot(...)` | Creates a Discord bot client |
| `command_prefix="!"` | Enables old-style text commands like `!ping` |
| `discord.Intents.default()` | Starts with default event permissions |
| `intents.message_content = True` | Allows reading raw message text for prefix commands |
| `intents.members = True` | Allows member data |
| `intents.presences = True` | Allows presence/activity data |
| `setup_hook()` | Initializes DBs and loads cogs before ready |
| `on_ready()` | Runs after bot connects and is ready |
| `self.tree.sync()` | Syncs slash commands to Discord |

## Cogs

A cog is a module/class used to group commands or event logic.

```mermaid
flowchart TD
    Main["main.py"] --> Load["load_extension / reload_extension"]
    Load --> Todo["dm_cogs/cogs/todo.py"]
    Load --> RemindStart["dm_cogs/cogs/check_date.py"]
    Load --> RemindEnd["dm_cogs/cogs/emdtime.py"]
    Load --> Respond["dm_cogs/cogs/respond.py"]
    Main --> Load2["second bot loads dm_cogs/*.py"]
    Load2 --> Bypass["dm_cogs/bypasswhat.py"]
    Load2 --> GameCheck["dm_cogs/checkgame.py"]
```

## Study Notes

- Bot tokens are secrets. Keep them out of Git.
- A connected bot can receive Gateway events.
- Slash commands need to be registered/synced before users see them.
- Prefix commands require message content access, but slash commands usually do not.

## Official Docs To Read

- Gateway: https://docs.discord.com/developers/events/gateway.md
- Gateway Events: https://docs.discord.com/developers/events/gateway-events.md
- Bots & Companion Apps: https://docs.discord.com/developers/bots/overview.md
