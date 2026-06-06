**1. `bot.py` skeleton** First thing coded. Got the bot online with nothing else — just confirmed it could connect to Discord.

**2. `database.py` — `setup_db()` only** Added the DB connection and created the `users` table. Confirmed `economy.db` appeared on disk.

**3. `cogs/economy.py` — empty cog** Just the class shell and `setup()` function, no commands yet. Added `load_extension()` to `bot.py` and confirmed the bot still started with no errors.

**4. `database.py` — `get_balance()`** Added the first DB read function, then wired `/balance` into the cog and added `tree.sync()` to `bot.py`. First time a user could actually interact with the bot.

**5. `database.py` — `add_balance()`, `get_last_work()`, `set_last_work()`** Added all three remaining DB functions, then wrote the full `/work` command in the cog.