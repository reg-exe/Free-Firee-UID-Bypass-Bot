# 🤖 Discord Whitelist Bot

A powerful Discord bot for managing UID whitelist systems with JSONBin.io backend integration.

## ✨ Features

- **🔐 Whitelist Management**: Add, remove, and check UIDs
- **📅 Expiry System**: Set expiration dates for entries
- **👑 Owner Controls**: Protected commands for bot owner
- **📊 JSON Export**: Easy data viewing in JSON format
- **📝 Activity Logging**: Comprehensive operation logs
- **⏸️ Pause/Resume**: Temporary system control
- **🚀 JSONBin.io Integration**: Simple and fast database

## 🚀 Quick Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template?template=https://github.com/your-username/discord-whitelist-bot)

### 1-Click Railway Deployment:

1. **Click the "Deploy on Railway" button above**
2. **Connect your GitHub account**
3. **Configure environment variables** (see below)
4. **Deploy automatically** - Railway handles everything!

## 🔧 Environment Variables

### For Railway Deployment:
Add these in your Railway project **Variables** tab:

```env
JSONBIN_URL=https://api.jsonbin.io/v3/b/YOUR_BIN_ID
JSONBIN_API_KEY=$2a$10$YOUR_MASTER_KEY_HERE
DISCORD_BOT_TOKEN=your_discord_bot_token_here
LOG_CHANNEL_ID=123456789012345678
DEV_DISCORD_ID=123456789012345678
ALLOWED_CHANNEL=123456789012345678
```

### For Local Development (.env file):
```env
# JSONBin.io Configuration
JSONBIN_URL=https://api.jsonbin.io/v3/b/YOUR_BIN_ID
JSONBIN_API_KEY=$2a$10$YOUR_MASTER_KEY_HERE

# Discord Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token_here
LOG_CHANNEL_ID=123456789012345678
DEV_DISCORD_ID=123456789012345678
ALLOWED_CHANNEL=123456789012345678
```

## 🛠️ Local Development

### Prerequisites
- Python 3.8+
- Discord Bot Token
- JSONBin.io Account

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/discord-whitelist-bot.git
cd discord-whitelist-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

4. **Run the bot**
```bash
python main.py
```

### For VPS/Hosting:
```bash
# Install Python and git
sudo apt update
sudo apt install python3 python3-pip git

# Clone and setup
git clone https://github.com/your-username/discord-whitelist-bot.git
cd discord-whitelist-bot
pip3 install -r requirements.txt

# Create .env file and add your variables
nano .env

# Run with process manager (using pm2)
npm install -g pm2
pm2 start main.py --name "whitelist-bot" --interpreter python3
pm2 startup
pm2 save
```

## 📋 Bot Commands

### 🔵 Public Commands
| Command | Description | Usage |
|---------|-------------|--------|
| `/help` | Show all commands | `/help` |
| `/checkuid` | Check UID in JSON format | `/checkuid uid:12345` |
| `/viewuid` | View UID in box format | `/viewuid uid:12345` |
| `/listuids` | List all UIDs | `/listuids` |
| `/adduid` | Add new UID entry | `/adduid uid:12345 year:2024 month:12 day:31 comment:Test` |

### 🟣 Owner Only Commands
| Command | Description | Usage |
|---------|-------------|--------|
| `/removeuid` | Remove UID from whitelist | `/removeuid uid:12345` |
| `/pause` | Pause whitelist system | `/pause` |
| `/resume` | Resume whitelist system | `/resume` |

## 🗃️ JSONBin.io Setup

### 1. Create JSONBin Account
- Go to [JSONBin.io](https://jsonbin.io/)
- Sign up for free account

### 2. Create Your Bin
```bash
# Create initial empty array
curl -X POST https://api.jsonbin.io/v3/b \
  -H "Content-Type: application/json" \
  -H "X-Master-Key: $2a$10$YOUR_MASTER_KEY" \
  -d "[]"
```

### 3. Get Your Credentials
- **JSONBIN_URL**: `https://api.jsonbin.io/v3/b/YOUR_BIN_ID`
- **JSONBIN_API_KEY**: Your master key starting with `$2a$10$`

## 🔧 Configuration

### Environment Variables Details
| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | ✅ | `MTEyMzQ1NeeeeeeeDU2.G-8Pty.Z8UEYd` |
| `JSONBIN_URL` | Your JSONBin.io bin URL | ✅ | `https://api.jsonbin.io/v3/b/692833aeeeeeee1f40035391` |
| `JSONBIN_API_KEY` | JSONBin.io master key | ✅ | `$2a$10$FggI8qWQV8M6q1EB5qKvZOZeeeeeeee6XWnT24r9YE53JnUa` |
| `LOG_CHANNEL_ID` | Discord channel ID for logs | ✅ | `123456789012345678` |
| `DEV_DISCORD_ID` | Bot owner's Discord ID | ✅ | `123456789012345678` |
| `ALLOWED_CHANNEL` | Channel where commands work | ✅ | `123456789012345678` |

### Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Go to "Bot" section
4. Create bot and copy token
5. Enable "Message Content Intent"
6. Invite bot with permissions:
   - `applications.commands`
   - `Send Messages`
   - `Read Message History`
   - `Embed Links`

## 📁 Project Structure

```
discord-whitelist-bot/
├── main.py              # Main bot application
├── requirements.txt     # Python dependencies
├── runtime.txt         # Python version specification (optional)
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### requirements.txt
```txt
discord.py>=2.3.0
requests>=2.28.0
python-dotenv>=1.0.0
```

## 🚄 Railway Specific Setup

### Automatic Deployment:
1. Fork this repository
2. Connect Railway to your GitHub
3. Add environment variables in Railway dashboard
4. Deployment happens automatically on git push

### Manual Railway Setup:
```bash
# Create new project
railway init

# Link to your repo
railway link

# Set environment variables
railway variables set DISCORD_BOT_TOKEN=your_token_here
railway variables set JSONBIN_URL=your_jsonbin_url
railway variables set JSONBIN_API_KEY=your_master_key

# Deploy
railway up
```

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if bot is online in Discord
   - Verify channel permissions
   - Check environment variables

2. **Commands not syncing**
   - Wait up to 1 hour for global command sync
   - Restart bot to force sync

3. **Database errors**
   - Verify JSONBin.io credentials
   - Check bin structure is an array `[]`

4. **Railway Deployment Issues**
   - Check build logs in Railway dashboard
   - Verify all environment variables are set
   - Ensure requirements.txt is correct

### Logs & Monitoring
- **Railway**: Check logs in dashboard
- **Discord**: Monitor log channel
- **JSONBin.io**: Verify data updates in your bin

## 🔒 Security Features

- ✅ Channel-specific command restrictions
- ✅ Owner-only protected commands
- ✅ Environment variable protection
- ✅ Input validation
- ✅ Error handling
- ✅ Activity logging

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- Create an [Issue](https://github.com/your-username/discord-whitelist-bot/issues)
- Check [Railway Documentation](https://docs.railway.app/)
- Discord.py [Documentation](https://discordpy.readthedocs.io/)
- JSONBin.io [API Docs](https://jsonbin.io/api-reference)

---

**⭐ Don't forget to star this repository if you found it helpful!**

## 🔄 Update Instructions

When updating the bot:
- **Railway**: Automatic on git push
- **Local**: `git pull && pip install -r requirements.txt`
- **VPS**: `git pull && pm2 restart whitelist-bot`

Your bot is now ready for deployment on Railway or any hosting platform! 🎉
