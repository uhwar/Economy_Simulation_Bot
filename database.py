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
# Bank Heist Functions
async def rob_bank(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            # Update this to off_shore when feature is up *********
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

async def set_jail_until(user_id: int, timestamp: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT or IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET jail_until = ? WHERE user_id = ?",
            (timestamp, user_id)
        )
        await db.commit()

async def get_jail_until(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT jail_until FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] is not None else 0

# Work Database Functions
async def get_last_work(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT last_work FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

            return row[0] if row else 0

async def set_last_work(user_id: int, timestamp: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET last_work = ? WHERE user_id = ?",
            (timestamp, user_id)
        )
        await db.commit()
# Balance Database Functions
async def add_balance(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

async def get_balance(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
                "SELECT balance FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def remove_balance(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

