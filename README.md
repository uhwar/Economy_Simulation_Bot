# Discord Economy Bot

A fully functional Discord economy bot built with Python, `discord.py`, and SQLite. This project demonstrates modern bot development with slash commands, async/await patterns, database management, and complex game mechanics.

## 🚀 Project Overview

This Discord bot features a comprehensive economy system where users can earn coins through various activities, gamble their earnings, participate in high-risk heists, and even get involved in jail-based gameplay mechanics. The project showcases clean architecture with separation of concerns and proper async patterns.

## Explicit Goals

- Create a self running economy
- Create a fun experience for players
- Understand and learn asynchronous programming
- Understand and learn database fundamentals (further than syntax learned from books)
- Advance my understanding of data structures



## 🛠️ Tech Stack

- **Python 3.x** - Core programming language
- **discord.py** - Discord API interaction and slash commands
- **aiosqlite** - Async SQLite database operations
- **SQLite** - Lightweight file-based database
- **async/await** - Asynchronous programming for handling multiple users
- **Discord Chat** - Modern Discord bot interface

## 📁 Project Structure

```
Economy_Bot/
├── bot.py              # Main bot entry point and configuration
├── database.py         # All database operations and SQL management
├── cogs/
│   └── economy.py      # Economy commands and game logic
├── adjust_balance.py   # Admin utility for balance adjustments
├── economy.db          # SQLite database file
└── notes/              # Project documentation and planning
```

## 🎮 Core Features

### **Basic Economy**
- **`/balance`** - Check your current coin balance
- **`/work`** - Earn coins with a 1-hour cooldown system
- **`/gamba`** - 50/50 gambling with double-or-nothing mechanics

### **Advanced Gameplay**
- **`/heist`** - High-risk bank robbery with jail consequences
  - 50% chance to escape with 500 coins
  - 50% chance to get caught and serve jail time
- **`/jailbreak`** - Rescue jailed players with risk mechanics
  - Higher success rate when not in jail yourself
  - Risk getting jailed yourself on failed attempts

### **Jail System**
- Dynamic jail timers based on actions
- Jail time prevents certain activities
- Jailbreaking mechanics with risk/reward

## 🧠 Key Learnings & Concepts

### **Async/Await Architecture**
- Built with proper async/await patterns for handling multiple users simultaneously
- Non-blocking database operations using `aiosqlite`
- Event-driven architecture for Discord interaction handling

### **Database Design**
- SQLite with `aiosqlite` for async database operations
- Proper SQL injection prevention using parameterized queries
- Atomic operations for balance updates
- Schema design supporting multiple game mechanics

### **Software Architecture**
- **Separation of Concerns**: Clear division between bot logic, database operations, and command handling
- **Modular Design**: Commands organized in cogs for maintainability
- **Error Handling**: Graceful handling of user input errors and edge cases

### **Game Design Principles**
- **Risk/Reward Balance**: Gambling and heists have balanced probabilities
- **Progression Systems**: Work cooldowns encourage regular engagement
- **Social Interaction**: Jailbreaking promotes player interaction
- **Consequence Mechanics**: Jail system adds depth to gameplay

## 🔧 Technical Implementation

### **Database Schema**
```sql
CREATE TABLE users (
    user_id   INTEGER PRIMARY KEY,
    balance   INTEGER DEFAULT 0,
    last_work INTEGER DEFAULT 0,
    jail_until INTEGER DEFAULT 0
)
```

### **Command Structure**
- All commands use Discord's modern slash command system
- Proper validation of user input and balances
- Cooldown systems implemented at database level
- Real-time jail status checks

### **Async Patterns**
- All I/O operations are async to prevent blocking
- Proper connection management with context managers
- Thread-safe database operations

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Required packages: `discord.py`, `aiosqlite`

### Installation
1. Clone the repository
2. Install dependencies: `pip install discord.py aiosqlite`
3. Add your bot token to `bot.py`
4. Run the bot: `python bot.py`

## 📈 Future Enhancements

### Planned Features (from project notes)
- **Multiple Jobs** with different mechanics and rewards
- **Titles and Reputation System** influencing job availability
- **Pet System** with feeding and maintenance mechanics
- **Shop System** with rotating inventory
- **Offshore Banking** for hiding illicit gains
- **Leaderboards** and competitive elements
- **Mini-games** for job activities

### Technical Improvements
- Environment variable configuration
- Proper logging and error tracking
- Unit and integration testing
- Docker containerization
- Web dashboard for bot management

## 🤝 Contributing

This project was built as a learning exercise to understand:
- Modern Discord bot development with slash commands
- Async programming patterns in Python
- Database design and management
- Game mechanics implementation
- Clean architecture and code organization

The comprehensive notes in the `notes/` folder document the entire learning journey, from basic concepts to advanced implementation details.

## 📚 Learning Outcomes

Through this project, I gained experience with:
- Building production-ready Discord bots
- Designing and implementing database schemas
- Creating engaging game mechanics with proper balance
- Writing maintainable, well-documented code
- Debugging async applications
- Managing state across multiple users
- Implementing proper error handling and validation

## ⚠️ Note

This bot is for educational purposes and showcases modern Discord bot development techniques. Always follow Discord's Terms of Service and guidelines when deploying bots.

---

*Built with Python, discord.py, and a lot of learning!*