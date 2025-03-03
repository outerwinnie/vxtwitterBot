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
YOUTUBE_MATCH = os.getenv('YOUTUBE_MATCH', '')
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')
INSTAGRAM_REPLACE = os.getenv('INSTAGRAM_REPLACE', '')
INSTAGRAM_REEL_REPLACE = os.getenv('INSTAGRAM_REEL_REPLACE', '')
TIKTOK_REPLACE = os.getenv('TIKTOK_REPLACE', '')
YOUTUBE_REPLACE = os.getenv('YOUTUBE_REPLACE', '')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Button Classes
class TweetButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="🔗 Ver Tweet en xCancel", url=url))  # Button linking to tweet

class YouTubeButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="▶ Watch on Youtube", url=url))  # Button linking to Invidious

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    # Extract social media links
    twitter_links = re.findall(r'https://twitter\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    x_links = re.findall(r'https://x\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    youtube_links = re.findall(r'https?:\/\/(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', message.content)
    instagram_links = re.findall(r'https://(www\.)?instagram\.com/p/[a-zA-Z0-9_-]+/?(\?[^/]+)?', message.content)
    instagram_reel_links = re.findall(r'https:\/\/www\.instagram\.com\/reel\/[A-Za-z0-9_-]+', message.content)
    tiktok_links = re.findall(r'https://www\.tiktok\.com/(?:@[\w.]+/video/\d+|t/[a-zA-Z0-9_-]+)\/?', message.content)
    tiktok_vm_links = re.findall(r'https://vm\.tiktok\.com/[a-zA-Z0-9]+/', message.content)

    reference_message = message.reference
    allowed_mentions = discord.AllowedMentions(
        everyone=message.mention_everyone,
        users=message.mentions,
        roles=message.role_mentions
    )

    # Handle Twitter/X links with BUTTONS
    for tweet_id in twitter_links + x_links:
        tweet_url = f"https://xcancel.com/i/web/status/{tweet_id}"  # Mobile-friendly tweet link
        logger.info(f'{message.guild.name}: {message.author} {message.content}')

        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(TWITTER_MATCH, TWITTER_REPLACE)}'
        view = TweetButtonView(url=tweet_url)  # Attach button

        if reference_message:
            replied_message = await message.channel.fetch_message(reference_message.message_id)
            await message.channel.send(
                new_message, allowed_mentions=allowed_mentions, reference=replied_message, view=view
            )
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, view=view)

        if DELETE_OP == 1:
            await message.delete()

    # Handle YouTube links with BUTTONS
    for video_id in youtube_links:
        youtube_url = f"https://youtube.com/watch?v={video_id}"  # Youtube link
        logger.info(f'{message.guild.name}: {message.author} {message.content}')

        new_message = f'{message.author.mention} {PREAMBLE}' + re.sub(
            r"https?://(www\.)?youtube\.com/watch\?v=",
            "https://inv.nadeko.net/watch?v=",
            message.content
        )
        view = YouTubeButtonView(url=youtube_url)  # Attach button

        if reference_message:
            replied_message = await message.channel.fetch_message(reference_message.message_id)
            await message.channel.send(
                new_message, allowed_mentions=allowed_mentions, reference=replied_message, view=view
            )
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, view=view)

        if DELETE_OP == 1:
            await message.delete()

    # Handle Instagram, TikTok links WITHOUT buttons
    async def process_social_media(match, match_str, replace_str):
        if match:
            logger.info(f'{message.guild.name}: {message.author} {message.content}')
            new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(match_str, replace_str)}'

            if reference_message:
                replied_message = await message.channel.fetch_message(reference_message.message_id)
                await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=replied_message)
            else:
                await message.channel.send(new_message, allowed_mentions=allowed_mentions)

            if DELETE_OP == 1:
                await message.delete()

    await process_social_media(instagram_links, INSTAGRAM_MATCH, INSTAGRAM_REPLACE)
    await process_social_media(instagram_reel_links, INSTAGRAM_REEL_MATCH, INSTAGRAM_REEL_REPLACE)
    await process_social_media(tiktok_links, TIKTOK_MATCH, TIKTOK_REPLACE)
    await process_social_media(tiktok_vm_links, TIKTOK_VM_MATCH, TIKTOK_REPLACE)

bot.run(DISCORD_TOKEN, log_handler=None)
