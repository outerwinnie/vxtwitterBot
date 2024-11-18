import discord
import os
import re
from logger import logger

# Load configuration from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
REPLY_TO = int(os.getenv('REPLY_TO', 0))  # Default to 0 if not set
DELETE_OP = int(os.getenv('DELETE_OP', 0))  # Default to 0 if not set
PREAMBLE = os.getenv('PREAMBLE', '')
TWITTER_MATCH = os.getenv('TWITTER_MATCH', '')
X_MATCH = os.getenv('X_MATCH', '')
INSTAGRAM_MATCH = os.getenv('INSTAGRAM_MATCH', '')
TIKTOK_VM_MATCH = os.getenv('TIKTOK_VM_MATCH', '')
TIKTOK_MATCH = os.getenv('TIKTOK_MATCH', '')
BLUESKY_MATCH = os.getenv('BLUESKY_MATCH', '')
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')
INSTAGRAM_REPLACE = os.getenv('INSTAGRAM_REPLACE', '')
TIKTOK_REPLACE = os.getenv('TIKTOK_REPLACE', '')
BLUESKY_REPLACE = os.getenv('BLUESKY_REPLACE', '')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    # Only need to match once, message.content.replace replaces all
    twitter_link = re.findall('https://twitter.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    x_link = re.findall('https://x.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    instagram_link = re.findall('https://www\.instagram\.com/p/[a-zA-Z0-9_-]+/?(\?[^/]+)?', message.content)
    instagram_reel_link = re.findall('https://www\.instagram\.com/reel/[a-zA-Z0-9_-]+/?(\?[^/]+)?', message.content)
    tiktok_link = re.findall('https:\/\/www\.tiktok\.com\/@[\w\.]+\/video\/\d+', message.content)
    tiktok_vm_link = re.findall('https:\/\/vm\.tiktok\.com\/[a-zA-Z0-9]+\/', message.content)
    bluesky_plc_link = re.findall('https:\/\/bsky\.app\/profile\/did:plc:[a-z0-9]{24}\/post\/[a-z0-9]+', message.content)
    bluesky_link = re.findall('https:\/\/bsky\.app\/profile\/[a-z0-9_.]+\.bsky\.social\/post\/[a-z0-9]+', message.content)

    if twitter_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(TWITTER_MATCH, TWITTER_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

    if x_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(X_MATCH, TWITTER_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

    if bluesky_link or bluesky_plc_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(BLUESKY_MATCH, BLUESKY_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message)
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions)

        if DELETE_OP == 1:
            await message.delete()

    if instagram_link or instagram_reel_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(INSTAGRAM_MATCH, INSTAGRAM_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

    if tiktok_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(TIKTOK_MATCH, TIKTOK_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message) 
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions) 
            
        if DELETE_OP == 1:
            await message.delete()

    if tiktok_vm_link:
        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(TIKTOK_VM_MATCH, TIKTOK_REPLACE)}'
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )
        if REPLY_TO == 1:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions, reference=message)
        else:
            await message.channel.send(new_message, allowed_mentions=allowed_mentions)

        if DELETE_OP == 1:
            await message.delete()

bot.run(DISCORD_TOKEN, log_handler=None)
