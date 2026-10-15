import logging
import os

import discord

CHANNEL_ID = 1426814903607623823
ROLE_ID = 1555620188471431218

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True

client = discord.Client(
    intents=intents,
    max_messages=None,
    member_cache_flags=discord.MemberCacheFlags.none(),
    allowed_mentions=discord.AllowedMentions(
        everyone=False,
        users=False,
        roles=[discord.Object(id=ROLE_ID)],
        replied_user=False,
    ),
)

@client.event
async def on_ready():
    logging.info("Online as %s", client.user)

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if client.user is None or message.author.id == client.user.id:
        return

    try:
        await message.channel.send(
            f"<@&{ROLE_ID}>",
            reference=message.to_reference(fail_if_not_exists=False),
            mention_author=False,
        )
    except discord.HTTPException:
        logging.exception("Could not tag the role for message %s", message.id)

token = os.environ.get("DISCORD_TOKEN")

if not token:
    raise RuntimeError("Set the DISCORD_TOKEN environment variable.")

client.run(token)
