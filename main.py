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
YOUTUBE_MATCH = os.getenv('YOUTUBE_MATCH', r'')
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')
INSTAGRAM_REPLACE = os.getenv('INSTAGRAM_REPLACE', '')
INSTAGRAM_REEL_REPLACE = os.getenv('INSTAGRAM_REEL_REPLACE', '')
TIKTOK_REPLACE = os.getenv('TIKTOK_REPLACE', '')
YOUTUBE_REPLACE = os.getenv('YOUTUBE_REPLACE', '')

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
    def __init__(self, video_id: str):
        super().__init__()
        self.video_id = video_id

    @discord.ui.button(label="▶ Ver en Nadeko", style=discord.ButtonStyle.primary)
    async def youtube_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        inv_url = f"https://inv.nadeko.net/watch?v={self.video_id}"
        await interaction.response.send_message(f"Aquí tienes el video sin anuncios: {inv_url}", ephemeral=True)

async def process_instagram_links(message: discord.Message):
    reference_message = message.reference
    allowed_mentions = discord.AllowedMentions(
        everyone=message.mention_everyone,
        users=message.mentions,
        roles=message.role_mentions
    )

    new_message = None

    # Match full Instagram reel URL and extract the path
    match = re.search(r'https://www\.instagram\.com(/reel/[a-zA-Z0-9_-]+)', message.content)
    if match:
        reel_path = match.group(1)  # This will be /reel/DGvQARyRVuP
        new_link = f"https://www.kkinstagram.com{reel_path}/"  # Append trailing slash
        new_message = f'{message.author.mention} {PREAMBLE}{new_link}'
    elif INSTAGRAM_MATCH in message.content:
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(INSTAGRAM_MATCH, INSTAGRAM_REPLACE)}'

    if not new_message:
        return

    logger.info(f'{message.guild.name}: {message.author} {message.content}')

    if reference_message:
        replied_message = await message.channel.fetch_message(reference_message.message_id)
        await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=replied_message)
    else:
        await message.channel.send(new_message, allowed_mentions=allowed_mentions)

    if DELETE_OP == 1:
        await message.delete()

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
    youtube_links = re.findall(YOUTUBE_MATCH, message.content)

    # Handle Twitter/X links
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

    # In the on_message function, handle the YouTube links
    youtube_links = re.findall(YOUTUBE_MATCH, message.content)
    unique_youtube_ids = list(dict.fromkeys(youtube_links))

    if unique_youtube_ids:
        for index, video_id in enumerate(unique_youtube_ids):
            logger.info(f'{message.guild.name}: {message.author} YouTube Video ID: {video_id}')
            view = YouTubeButtonView(video_id)
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"

            if index == 0:
                # Keep the original message text, but only keep the first link
                # Remove all YouTube links from message
                cleaned_text = re.sub(YOUTUBE_MATCH, '', message.content).strip()

                # If there's text before the link, append the link after the preamble on a new line
                if cleaned_text:
                    final_text = f'{cleaned_text}\n{youtube_url}'
                else:
                    final_text = youtube_url  # Just the link if there's no text

                # Remove newlines from the preamble to prevent extra space
                cleaned_preamble = PREAMBLE.replace('\n', ' ')  # Replace any newline in the preamble with a space

                response_msg = f'{message.author.mention} {cleaned_preamble}\n{final_text}'

                if reference_message:
                    replied_message = await message.channel.fetch_message(reference_message.message_id)
                    await message.channel.send(response_msg, allowed_mentions=allowed_mentions,
                                               reference=replied_message, view=view)
                else:
                    await message.channel.send(response_msg, allowed_mentions=allowed_mentions, view=view)
            else:
                # Separate message for each remaining link
                response_msg = f'{message.author.mention} {PREAMBLE}\n{youtube_url}'
                await message.channel.send(response_msg, allowed_mentions=allowed_mentions, view=view)

        if DELETE_OP == 1:
            await message.delete()

    # Process Instagram links
    await process_instagram_links(message)

    # Handle TikTok links
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

    await process_social_media(re.findall(TIKTOK_MATCH, message.content), TIKTOK_MATCH, TIKTOK_REPLACE)
    await process_social_media(re.findall(TIKTOK_VM_MATCH, message.content), TIKTOK_VM_MATCH, TIKTOK_REPLACE)

bot.run(DISCORD_TOKEN, log_handler=None)
