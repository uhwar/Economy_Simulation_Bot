# Discord Economy Bot

A Discord bot implementing an economy system with async Python, SQLite database management, and modular architecture using Discord.py.

## Technical Implementation

### **Concepts Demonstrated**
- **Async/Await Patterns** - Non-blocking I/O operations with Python coroutines
- **Database Design** - SQLite schema design with foreign key relationships and audit logging
- **Modular Architecture** - Separation of concerns using Discord.py cogs and shared data layer
- **Financial Calculations** - Compound interest implementation with time-based accrual
- **Production Practices** - Environment variable configuration and secure token management

## Technical Stack
- **Python 3.8+** with async/await patterns
- **discord.py** for Discord API interaction
- **aiosqlite** for async SQLite operations  
- **SQLite** for data persistence
- **python-dotenv** for configuration management

## Architecture

```mermaid
flowchart TD
    A[Discord User] --> B[/Slash Command/]
    B --> C[bot.py - Main Entry]
    C --> D[cogs/economy.py - Game Logic]
    C --> E[cogs/banking.py - Financial System]
    C --> F[cogs/admin.py - Admin Tools]
    
    D --> G[database.py - Data Layer]
    E --> G
    F --> G
    
    G --> H[(economy.db - SQLite)]
```

## Project Structure
```
Economy_Bot/
├── bot.py              # Bot configuration and startup
├── database.py         # Database operations and schema
├── cogs/               # Modular command groups
│   ├── economy.py      # Core economy commands
│   ├── banking.py      # Banking system with interest
│   └── admin.py        # Administrative utilities
├── adjust_balance.py   # Utility for balance adjustments
├── .env.example        # Environment template
└── .gitignore          # Version control exclusions
```

## Database Design
```sql
-- Primary user data
CREATE TABLE users (
    user_id   INTEGER PRIMARY KEY,
    balance   INTEGER DEFAULT 0,
    last_work INTEGER DEFAULT 0,
    jail_until INTEGER DEFAULT 0
)

-- Banking system with compound interest
CREATE TABLE bank_accounts (
    user_id INTEGER PRIMARY KEY,
    bank_balance INTEGER DEFAULT 0,
    interest_rate FLOAT DEFAULT 0.01,
    last_interest_calculation INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)

-- Transaction audit trail
CREATE TABLE transaction_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    action        TEXT    NOT NULL,
    amount        INTEGER NOT NULL,
    balance_after INTEGER NOT NULL,
    time_stamp    TEXT    DEFAULT (datetime('now'))
)
```

## Key Technical Implementation

### Async Database Operations
```python
async def get_balance(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT balance FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0
```

### Compound Interest Calculation
```python
async def calculate_interest(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
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
        if last_calc > 0:
            days = (now - last_calc) // 86400
        else:
            days = 0
        
        if days > 0 and bank_balance > 0:
            # Compound interest: new_balance = balance * (1 + rate)^days
            new_balance = int(bank_balance * ((1 + interest_rate) ** days))
            await db.execute(
                "UPDATE bank_accounts SET bank_balance = ?, last_interest_calculation = ? WHERE user_id = ?",
                (new_balance, now, user_id)
            )
            await db.commit()
```

### Modular Command System
```python
# bot.py - loading extensions
async def setup_hook(self):
    await database.setup_db()
    await self.load_extension("cogs.economy")
    await self.load_extension("cogs.banking")
    await self.load_extension("cogs.admin")
    await self.tree.sync(guild=MY_GUILD)

# cogs/banking.py - command implementation
@app_commands.command(name="bank_deposit", description="Deposit coins to your bank account")
async def bank_deposit(self, interaction: discord.Interaction, amount: int):
    user_id = interaction.user.id
    if amount <= 0:
        await interaction.response.send_message("Amount must be more than 0.")
        return
    
    wallet_bal = await database.get_balance(user_id)
    if amount > wallet_bal:
        await interaction.response.send_message("You don't have enough coins in your wallet.")
        return
    
    await database.calculate_interest(user_id)
    await database.deposit_to_bank(user_id, amount)
    
    new_wallet = await database.get_balance(user_id)
    new_bank = await database.get_bank_balance(user_id)
    
    await interaction.response.send_message(
        f"Deposited {amount} coins to your bank.\n"
        f"Wallet: {new_wallet} coins\n"
        f"Bank: {new_bank} coins"
    )
```

## Features
- **/balance** - Check user balance
- **/work** - Earn coins with cooldown system
- **/gamba** - 50/50 gambling mechanics
- **/bank_balance** - View bank balance with interest
- **/bank_deposit** - Deposit coins to bank account
- **/bank_withdraw** - Withdraw from bank
- **/bank_interest** - Interest calculation details
- **/heist** - Risk/reward bank robbery
- **/jailbreak** - Player jail system
- **/give_player_balance** - Admin balance management
- **/admin_bailout** - Admin jail management

## Installation
```bash
pip install discord.py aiosqlite python-dotenv
cp .env.example .env
# Edit .env with DISCORD_TOKEN and GUILD_ID
python bot.py
```

## Environment Configuration
```env
DISCORD_TOKEN=your_bot_token
GUILD_ID=your_guild_id
```