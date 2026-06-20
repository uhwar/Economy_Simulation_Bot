# Banking System with Interest Action Plan

## 🎯 Goal
Add a banking system with interest accrual tied to player IDs

## 📋 Database Schema Changes

### New Table: `bank_accounts`
```sql
CREATE TABLE bank_accounts (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    interest_rate FLOAT DEFAULT 0.01,  -- 1% daily interest
    last_interest_calculation INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
```

### Modified Table: `users`
```sql
ALTER TABLE users ADD COLUMN total_wealth INTEGER DEFAULT 0;
```

## 📋 Implementation Tasks

### Phase 1: Database Layer (Day 1)
- [ ] **Add new table creation** to `setup_db()`
- [ ] **Create bank database functions**:
  - `create_bank_account(user_id)`
  - `get_bank_balance(user_id)`
  - `deposit_to_bank(user_id, amount)`
  - `withdraw_from_bank(user_id, amount)`
  - `calculate_interest(user_id)`
  - `get_interest_rate(user_id)`

### Phase 2: Interest Calculation (Day 1)
- [ ] **Interest calculation logic**:
  - Daily compounding interest (configurable rate)
  - Calculate only when account is accessed
  - Store last calculation timestamp
  - Formula: `new_balance = balance * (1 + interest_rate)^days`

- [ ] **Scheduled interest task** (optional):
  - Background task for all accounts
  - Runs daily at midnight
  - Updates bank balances automatically

### Phase 3: Bank Commands (Day 2)
- [ ] **`/bank` command**:
  - View current bank balance
  - Show interest rate and next calculation
  - Display total wealth (wallet + bank)

- [ ] **`/deposit <amount>` command**:
  - Transfer coins from wallet to bank
  - Validate sufficient wallet balance
  - Update both wallet and bank balances

- [ ] **`/withdraw <amount>` command**:
  - Transfer coins from bank to wallet
  - Validate sufficient bank balance
  - Apply interest before withdrawal

- [ ] **`/interest` command**:
  - Show current interest rate
  - Display projected earnings
  - Explain compounding mechanics

### Phase 4: Advanced Features (Day 2-3)
- [ ] **Tiered interest rates**:
  - Higher balances get better rates
  - Loyalty bonuses for long-term banking
  - Special event rates

- [ ] **Bank upgrades system**:
  - `/upgrade_bank` command
  - Cost-based tier improvements
  - Better interest rates per tier

- [ ] **Wealth tracking**:
  - Update `total_wealth` on all transactions
  - Leaderboard for total wealth
  - Rich player badges/roles

## 🏗️ Technical Implementation

### Database Functions (pseudo-code)
```python
async def calculate_interest(user_id: int):
    # Get current balance and last calculation
    # Calculate days since last interest
    # Apply compound interest formula
    # Update balance and timestamp
```

### Command Structure
```python
@app_commands.command(name="bank")
async def bank_command(self, interaction):
    # Calculate interest first
    await database.calculate_interest(user_id)
    # Get updated balance
    # Show bank info with interest details
```

### Interest Calculation Formula
```
Daily interest: balance * (1 + rate)^days
Where: rate = daily interest rate (e.g., 0.01 for 1%)
       days = days since last calculation
```

## 🎮 Game Design Considerations

### Balance Mechanics
- **Risk vs Reward**: Bank is safe but slow growth
- **Liquidity trade-off**: Money in bank can't be used for gambling/heists
- **Progression**: Higher tiers reward consistent banking

### Player Engagement
- Daily login incentives for interest calculation
- Wealth milestones and achievements
- Competitive leaderboards

## 📊 Success Metrics
- ✅ Bank accounts created for all existing users
- ✅ Interest calculates correctly
- ✅ Commands work without breaking existing features
- ✅ Players understand banking mechanics
- ✅ No performance impact on existing systems

## 🚀 Expected Outcome
A fully functional banking system that:
- Encourages long-term player engagement
- Adds depth to the economy
- Provides safe wealth storage
- Demonstrates advanced database design