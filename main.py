import discord
import os
import re
from logger import logger

# Load configuration from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DELETE_OP = int(os.getenv('DELETE_OP', 0))  # Default to 0 if not set
PREAMBLE = os.getenv('PREAMBLE', '')

# Social Media Matches & Replacements
TWITTER_MATCH = os.getenv('TWITTER_MATCH', '')
X_MATCH = os.getenv('X_MATCH', '')
INSTAGRAM_MATCH = os.getenv('INSTAGRAM_MATCH', '')
INSTAGRAM_REEL_MATCH = os.getenv('INSTAGRAM_REEL_MATCH', '')
TIKTOK_VM_MATCH = os.getenv('TIKTOK_VM_MATCH', '')
TIKTOK_MATCH = os.getenv('TIKTOK_MATCH', '')
YOUTUBE_MATCH = os.getenv('YOUTUBE_MATCH', r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)')
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')
INSTAGRAM_REPLACE = os.getenv('INSTAGRAM_REPLACE', '')
INSTAGRAM_REEL_REPLACE = "https://kkinstagram.com"
TIKTOK_REPLACE = os.getenv('TIKTOK_REPLACE', '')
YOUTUBE_REPLACE = os.getenv('YOUTUBE_REPLACE', r'https://inv.nadeko.net/watch?v=\1')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Button Classes for URLs
class TweetButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="🔗 Ver Tweet en xCancel", url=url))

class YouTubeButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="▶ Ver en YouTube", url=url))

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    reference_message = message.reference
    allowed_mentions = discord.AllowedMentions(
        everyone=message.mention_everyone,
        users=message.mentions,
        roles=message.role_mentions
    )

    # Extract Twitter/X links
    twitter_links = re.findall(r'https?://(?:www\.)?(twitter|x)\.com/([a-zA-Z0-9_]+)/status/(\d+)', message.content)

    for platform, username, tweet_id in twitter_links:
        vxtwitter_url = f"https://vxtwitter.com/{username}/status/{tweet_id}"
        xcancel_url = f"https://xcancel.com/i/web/status/{tweet_id}"

        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{re.sub(TWITTER_MATCH, TWITTER_REPLACE, message.content)}'
        view = TweetButtonView(url=xcancel_url)

        if reference_message:
            replied_message = await message.channel.fetch_message(reference_message.message_id)
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=replied_message, view=view)
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, view=view)

        if DELETE_OP == 1:
            await message.delete()

    # Handle YouTube links
    youtube_links = re.findall(YOUTUBE_MATCH, message.content)
    for video_id in youtube_links:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        logger.info(f'{message.guild.name}: {message.author} {message.content}')

        new_message = f'{message.author.mention} {PREAMBLE}{re.sub(YOUTUBE_MATCH, YOUTUBE_REPLACE, message.content)}'
        view = YouTubeButtonView(url=youtube_url)

        if reference_message:
            replied_message = await message.channel.fetch_message(reference_message.message_id)
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=replied_message, view=view)
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, view=view)

        if DELETE_OP == 1:
            await message.delete()

    # Process Instagram & TikTok
    async def process_social_media(match_str, replace_str, use_kkinstagram=False):
        if re.search(match_str, message.content):
            logger.info(f'{message.guild.name}: {message.author} {message.content}')
            new_message = f'{message.author.mention} {PREAMBLE}{re.sub(match_str, replace_str, message.content)}/' if use_kkinstagram else f'{message.author.mention} {PREAMBLE}{re.sub(match_str, replace_str, message.content)}'

            if reference_message:
                replied_message = await message.channel.fetch_message(reference_message.message_id)
                await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=replied_message)
            else:
                await message.channel.send(new_message, allowed_mentions=allowed_mentions)

            if DELETE_OP == 1:
                await message.delete()

    # Ensure only one replacement for Instagram Reels
    if re.search(INSTAGRAM_REEL_MATCH, message.content):
        await process_social_media(INSTAGRAM_REEL_MATCH, INSTAGRAM_REEL_REPLACE, use_kkinstagram=True)
    else:
        await process_social_media(INSTAGRAM_MATCH, INSTAGRAM_REPLACE)

    await process_social_media(TIKTOK_MATCH, TIKTOK_REPLACE)
    await process_social_media(TIKTOK_VM_MATCH, TIKTOK_REPLACE)

bot.run(DISCORD_TOKEN, log_handler=None)
