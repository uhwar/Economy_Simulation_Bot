# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install discord.py aiosqlite python-dotenv
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your values:
```env
DISCORD_TOKEN=your_actual_bot_token_here
GUILD_ID=your_actual_guild_id_here
```

### 3. Get Your Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application (or select your existing bot)
3. Go to the "Bot" section
4. Click "Reset Token" and copy the new token
5. Paste it into your `.env` file as `DISCORD_TOKEN`

### 4. Get Your Guild (Server) ID

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Developer Mode (toggle on)
2. Right-click your Discord server icon
3. Click "Copy Server ID"
4. Paste it into your `.env` file as `GUILD_ID`

### 5. Run the Bot

```bash
python bot.py
```

You should see "Bot ready." in the console.

## Security Notes

- **Never commit your `.env` file to Git** - it contains secrets
- The `.env.example` file is safe to commit (it has placeholder values)
- Your `.env` file is already ignored by `.gitignore`
- If you accidentally expose your token, regenerate it immediately in the Discord Developer Portal

## Troubleshooting

**Bot doesn't appear online:**
- Check that your token is correct in `.env`
- Make sure the bot is invited to your server with proper permissions

**Commands don't appear:**
- Wait a few minutes after starting the bot (slash commands can take time to sync)
- Try running the bot again
- Make sure your `GUILD_ID` is correct

**Database errors:**
- The `economy.db` file will be created automatically on first run
- Make sure the bot has write permissions in the project directory
