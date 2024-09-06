# 🎉 **vxTwitter Bot** 🤖

Welcome to the **vxTwitter Bot** project! This bot enhances your Discord server by processing messages to replace specific links. 🚀

## 🛠️ **Features**

- **🔗 Link Replacement:** Automatically changes `twitter.com` and `x.com` links to `vxtwitter.com` in message content.
- **🗑️ Message Deletion:** Optionally deletes the original messages after processing.
- **🌟 Customizable:** Easily configure bot behavior using environment variables.

## 🐳 **Docker Setup**

To run the bot using Docker, follow these steps:

### 1. Build the Docker Image

```bash
docker build -t discord-bot .
```

### 2. Run the Docker Container

```bash
docker run -d \
  -e DISCORD_TOKEN=your_discord_token \
  -e REPLY_TO=1 \
  -e DELETE_OP=1 \
  -e PREAMBLE="Some preamble text" \
  -e MATCH1="text to match" \
  -e MATCH2="another text to match" \
  -e MATCH3="another text to match" \
  -e REPLACE="replacement text" \
  -e REPLACE2="replacement text" \
  discord-bot
```

## 📖 **How It Works**

The bot listens to messages in your Discord server. When it detects a message containing a link to `twitter.com` or `x.com`, it replaces the link with `vxtwitter.com`. 

For example:
- `https://twitter.com/username/status/1234567890` becomes `https://vxtwitter.com/username/status/1234567890`
- `https://x.com/username/status/1234567890` becomes `https://vxtwitter.com/username/status/1234567890`

The bot can also reply to the original message with the updated content and optionally delete the original message based on your configuration.
