# vxtwitterBot

A Discord bot that replaces messages that contain `https://twitter.com` or `https://x.com` URLs with `https://vxtwitter.com` (https://github.com/dylanpdx/BetterTwitFix).

### Differences between [joaocmd/vxTwitterBot](https://github.com/joaocmd/vxTwitterBot) and this fork:
* Support for `https://x.com` links
* Added config option to enable/disable deleting original message
* Added config option to enable/disable replying to original message
* Removed Twitter API GIF/video and Discord embed checks as every `https://twitter.com` or `https://x.com` embed is currently broken on Discord

## Usage

Copy the `config-template.json` to a `config.json` and edit as necessary.
The config file is structured as follows:

```json
{
    "DISCORD_TOKEN": "<TOKEN_HERE>",
	"REPLY_TO": 0, // replies to original message, off by default
	"DELETE_OP": 1, // deletes original message
    "PREAMBLE": "wrote:\n", // message starts with "@mention wrote:\n"
    "MATCH1": "https://twitter.com",
	"MATCH2": "https://x.com",
    "REPLACE": "https://vxtwitter.com"
}

```

## Necessary bot permissions

The following permissions are necessary to run the bot:
* Read Messages/View Channels (Requires message content intent)
* Send Messages
* Manage Messages
* Embed Links
