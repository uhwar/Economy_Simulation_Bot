
#### Step 1 — Project skeleton + bot connects

**Create these files (all empty for now):**

```
economy-bot/
├── bot.py
├── database.py
├── cogs/
│   └── economy.py
│   └── __init__.py     ← empty file, just needs to exist
```

> The `__init__.py` tells Python "this folder is a package." Without it, `load_extension("cogs.economy")` fails.

**Write `bot.py` first — the minimal version:**

```python
import discord
from discord.ext import commands

TOKEN = "YOUR_TOKEN"

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("Bot ready.")

bot = MyBot()
bot.run(TOKEN)
```

**Test:** Run it. You should see `Bot ready.` in your terminal and the bot appear online in Discord. Nothing else yet.

---

#### Step 2 — Database setup

**Write `database.py` with only `setup_db()`:**

```python
import aiosqlite

DB_PATH = "economy.db"

async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id   INTEGER PRIMARY KEY,
                balance   INTEGER DEFAULT 0,
                last_work INTEGER DEFAULT 0
            )
        """)
        await db.commit()
```

**Then update `setup_hook()` in `bot.py`:**

```python
async def setup_hook(self):
    await database.setup_db()
    print("Bot ready.")
```

**Test:** Run the bot. Check your folder — `economy.db` should now exist. You can open it with [DB Browser for SQLite](https://sqlitebrowser.org/) to visually confirm the `users` table was created.

---

#### Step 3 — Load the cog (empty)

**Put this in `cogs/economy.py`:**

```python
import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Economy(bot))
```

**Update `setup_hook()` in `bot.py`:**

```python
async def setup_hook(self):
    await database.setup_db()
    await self.load_extension("cogs.economy")
    print("Bot ready.")
```

**Test:** Bot should still start and print `Bot ready.` with no errors. If the cog fails to load, you'll see a traceback here.

---

#### Step 4 — `/balance` command + `get_balance()` in DB

Add `get_balance()` to `database.py`, then add the `/balance` slash command to the cog, then add `tree.sync()` to `bot.py`.

This is the first time a user can actually interact with the bot.

**Test:** Type `/balance` in Discord. You should get back `0 coins` (since no one has any yet).

---

#### Step 5 — `add_balance()` in DB + `/work` command

Add `add_balance()` and both `get_last_work()` / `set_last_work()` to `database.py`, then write the full `/work` command.

**Test:**

- Use `/work` → should earn coins
- Check `/balance` → balance should reflect it
- Use `/work` again immediately → should get the cooldown message
- Wait or temporarily set `WORK_COOLDOWN = 10` to test expiry fast, then set it back

---

### Summary Table

|Step|What You Write|What You Test|
|---|---|---|
|1|`bot.py` skeleton|Bot goes online|
|2|`setup_db()`|`economy.db` file appears|
|3|Empty cog + `load_extension`|Bot still starts, no errors|
|4|`get_balance()` + `/balance`|Slash command responds|
|5|`add_balance()` + `/work`|Full earn + cooldown loop|

Each step has one thing that can break, so when something goes wrong you know exactly where to look. Come back when you hit step 4 and I'll walk you through adding `tree.sync()` correctly.