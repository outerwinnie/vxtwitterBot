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
TWITTER_REPLACE = os.getenv('TWITTER_REPLACE', '')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


class TweetButtonView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="🔗 Ver Tweet", url=url))


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.id == bot.user.id:
        return

    twitter_match = re.search(r'https://twitter\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)
    x_match = re.search(r'https://x\.com/[a-zA-Z0-9_]*/status/([0-9]+)', message.content)

    if twitter_match:
        tweet_id = twitter_match.group(1)
        tweet_url = f"https://xcancel.com/i/web/status/{tweet_id}"

        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(TWITTER_MATCH, TWITTER_REPLACE)}'

        reference_message = message.reference
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )

        view = TweetButtonView(url=tweet_url)  # Button linking to the tweet

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

    if x_match:
        tweet_id = x_match.group(1)
        tweet_url = f"https://xcancel.com/i/web/status/{tweet_id}"

        logger.info(f'{message.guild.name}: {message.author} {message.content}')
        new_message = f'{message.author.mention} {PREAMBLE}{message.content.replace(X_MATCH, TWITTER_REPLACE)}'

        reference_message = message.reference
        allowed_mentions = discord.AllowedMentions(
            everyone=message.mention_everyone,
            users=message.mentions,
            roles=message.role_mentions
        )

        view = TweetButtonView(url=tweet_url)  # Button linking to the tweet

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


bot.run(DISCORD_TOKEN, log_handler=None)
