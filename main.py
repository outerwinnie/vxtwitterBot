import discord
import os
import re
from logger import logger

# Load configuration from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DELETE_OP = int(os.getenv('DELETE_OP', 0))  # Default to 0 if not set
PREAMBLE = os.getenv('PREAMBLE', '')
TWITTER_MATCH = os.getenv('TWITTER_MATCH', '')
X_MATCH = os.getenv('X_MATCH', '')
INSTAGRAM_MATCH = os.getenv('INSTAGRAM_MATCH', '')
INSTAGRAM_REEL_MATCH = os.getenv('INSTAGRAM_REEL_MATCH', '')
TIKTOK_VM_MATCH = os.getenv('TIKTOK_VM_MATCH', '')
TIKTOK_MATCH = os.getenv('TIKTOK_MATCH', '')
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')
INSTAGRAM_REPLACE = os.getenv('INSTAGRAM_REPLACE', '')
INSTAGRAM_REEL_REPLACE = os.getenv('INSTAGRAM_REEL_REPLACE', '')
TIKTOK_REPLACE = os.getenv('TIKTOK_REPLACE', '')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

class TweetButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="🔗 View Tweet", url=url))

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    # Match different social media links
    twitter_match = re.search(r'https://twitter\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    x_match = re.search(r'https://x\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    instagram_link = re.findall(r'https://(www\.)?instagram\.com/p/[a-zA-Z0-9_-]+/?(\?[^/]+)?', message.content)
    instagram_reel_link = re.findall(r'https?://(www\.)?instagram\.com/reel/[a-zA-Z0-9_-]+/(\?igsh=[a-zA-Z0-9_-]+)?', message.content)
    tiktok_link = re.findall(r'https://www\.tiktok\.com/(?:@[\w.]+/video/\d+|t/[a-zA-Z0-9_-]+)\/?', message.content)
    tiktok_vm_link = re.findall(r'https://vm\.tiktok\.com/[a-zA-Z0-9]+/', message.content)

    async def process_message(match, match_str, replace_str, base_url):
        if match:
            tweet_id = match.group(1)
            tweet_url = f"{base_url}{tweet_id}"

            logger.info(f'{message.guild.name}: {message.author} {message.content}')
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(match_str, replace_str)}'
            reference_message = message.reference
            allowed_mentions = discord.AllowedMentions(
                everyone=message.mention_everyone,
                users=message.mentions,
                roles=message.role_mentions
            )

            view = TweetButtonView(url=tweet_url)

            if reference_message:
                replied_message = await message.channel.fetch_message(reference_message.message_id)
                await message.channel.send(
                    new_message,
                    allowed_mentions=allowed_mentions,
                    reference=replied_message,
                    view=view
                )
            else:
                await message.channel.send(
                    new_message,
                    allowed_mentions=allowed_mentions,
                    view=view
                )

            if DELETE_OP == 1:
                await message.delete()

    # Process Twitter/X messages with buttons
    await process_message(twitter_match, TWITTER_MATCH, TWITTER_REPLACE, "https://twitter.com/i/web/status/")
    await process_message(x_match, X_MATCH, TWITTER_REPLACE, "https://x.com/i/web/status/")

    # Process other social media links (without buttons)
    async def process_other_message(match, match_str, replace_str):
        if match:
            logger.info(f'{message.guild.name}: {message.author} {message.content}')
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(match_str, replace_str)}'
            reference_message = message.reference
            allowed_mentions = discord.AllowedMentions(
                everyone=message.mention_everyone,
                users=message.mentions,
                roles=message.role_mentions
            )

            if reference_message:
                replied_message = await message.channel.fetch_message(reference_message.message_id)
                await message.channel.send(
                    new_message,
                    allowed_mentions=allowed_mentions,
                    reference=replied_message
                )
            else:
                await message.channel.send(
                    new_message,
                    allowed_mentions=allowed_mentions
                )

            if DELETE_OP == 1:
                await message.delete()

    # Handle Instagram, TikTok messages
    await process_other_message(instagram_link, INSTAGRAM_MATCH, INSTAGRAM_REPLACE)
    await process_other_message(instagram_reel_link, INSTAGRAM_REEL_MATCH, INSTAGRAM_REEL_REPLACE)
    await process_other_message(tiktok_link, TIKTOK_MATCH, TIKTOK_REPLACE)
    await process_other_message(tiktok_vm_link, TIKTOK_VM_MATCH, TIKTOK_REPLACE)

bot.run(DISCORD_TOKEN, log_handler=None)