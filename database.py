import aiosqlite
import time

DB_PATH = "economy.db"

MIGRATIONS = [
    "ALTER TABLE users ADD COLUMN jail_until REAL DEFAULT 0",
]

async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id    INTEGER PRIMARY KEY,
                balance    INTEGER DEFAULT 0,
                last_work  INTEGER DEFAULT 0,
                jail_until REAL    DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transaction_log (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL,
                action        TEXT    NOT NULL,
                amount        INTEGER NOT NULL,
                balance_after INTEGER NOT NULL,
                time_stamp    TEXT    DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bank_accounts (
                user_id INTEGER PRIMARY KEY,
                bank_balance INTEGER DEFAULT 0,
                interest_rate FLOAT DEFAULT 0.01,
                last_interest_calculation INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        for migration in MIGRATIONS:
            try:
                await db.execute(migration)
            except Exception:
                pass
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

async def log_transaction(user_id: int, action:str, amount: int, balance_after: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO transaction_log (user_id, action, amount, balance_after) VALUES (?, ?, ?, ?)",
            (user_id, action, amount, balance_after)
        )
        await db.commit()
# Bank Functions
async def create_bank_account(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO bank_accounts (user_id) VALUES (?)", (user_id,)
        )
        await db.commit()

async def get_bank_balance(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT bank_balance FROM bank_accounts WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def deposit_to_bank(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        # Create account if doesn't exist
        await db.execute(
            "INSERT OR IGNORE INTO bank_accounts (user_id) VALUES (?)", (user_id,)
        )
        # Remove from wallet
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (amount, user_id)
        )
        # Add to bank
        await db.execute(
            "UPDATE bank_accounts SET bank_balance = bank_balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

async def withdraw_from_bank(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        # Add to wallet
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,)
        )
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        # Remove from bank
        await db.execute(
            "UPDATE bank_accounts SET bank_balance = bank_balance - ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()

async def get_last_interest_calculation(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT last_interest_calculation FROM bank_accounts WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] is not None else 0

async def calculate_interest(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        # Ensure account exists
        await db.execute(
            "INSERT OR IGNORE INTO bank_accounts (user_id) VALUES (?)", (user_id,)
        )
        
        # Get current balance and last calculation
        async with db.execute(
            "SELECT bank_balance, last_interest_calculation, interest_rate FROM bank_accounts WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if not row:
                return
            
            bank_balance = row[0] or 0
            last_calc = row[1] or 0
            interest_rate = row[2] or 0.01
        
        now = int(time.time())
        
        # Calculate days since last interest
        if last_calc == 0:
            days = 0
        else:
            days = (now - last_calc) // 86400  # seconds in a day
        
        if days > 0 and bank_balance > 0:
            # Compound interest: new_balance = balance * (1 + rate)^days
            new_balance = int(bank_balance * ((1 + interest_rate) ** days))
            interest_earned = new_balance - bank_balance
            
            if interest_earned > 0:
                await db.execute(
                    "UPDATE bank_accounts SET bank_balance = ?, last_interest_calculation = ? WHERE user_id = ?",
                    (new_balance, now, user_id)
                )
                await db.commit()
                return interest_earned
        
        # Update last calculation time even if no interest earned
        await db.execute(
            "UPDATE bank_accounts SET last_interest_calculation = ? WHERE user_id = ?",
            (now, user_id)
        )
        await db.commit()
        return 0

async def get_interest_rate(user_id: int) -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT interest_rate FROM bank_accounts WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0.01