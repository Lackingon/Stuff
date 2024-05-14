import asyncio
import datetime
import os
import random

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv
from random import choice

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.hybrid_command()
async def votetimeout(ctx: commands.Context, user: discord.Member, time: int):
    total_members = len(ctx.guild.members)
    min_yes_votes_timeout = 4

    if time > 1800:
        await ctx.send("The maximum timeout duration is 30 minutes (1800 seconds).")
        return

    msg = await ctx.send(f"@here Shall we cast out {user.mention} for {time} seconds?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes_timeout:
        timeout = datetime.timedelta(seconds=time)
        await user.timeout(timeout)
        await ctx.send(f"{user.display_name} HAS BEEN CASTED OUT FOR {time} SECONDS!")
    else:
        await ctx.send(f"Not enough votes to cast out {user.display_name}.")


@bot.hybrid_command()
async def voteban(ctx: commands.Context, user: discord.Member):
    total_members = len(ctx.guild.members)
    min_yes_votes = 6

    msg = await ctx.send(f"@here Shall we ban {user.mention}?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 180
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        await user.ban()
        await ctx.send(f"{user.display_name} HAS BEEN BANNED!")
    else:
        await ctx.send(f"Not enough votes to ban {user.display_name}.")


@bot.hybrid_command()
async def votemute(ctx: commands.Context, user: discord.Member, time: int):
    if time > 1800:
        await ctx.send("The maximum mute duration is 30 minutes (1800 seconds).")
        return

    total_members = len(ctx.guild.members)
    min_yes_votes = 3

    msg = await ctx.send(f"@here Shall we mute {user.mention} for {time} seconds?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        await user.edit(mute=True)
        await ctx.send(f"{user.display_name} HAS BEEN MUTED FOR {time} SECONDS!")
        await asyncio.sleep(time)
        await user.edit(mute=False)
        await ctx.send(f"{user.display_name} HAS BEEN UNMUTED AFTER {time} SECONDS!")
    else:
        await ctx.send(f"Not enough votes to mute {user.display_name}.")


@bot.hybrid_command()
async def votegag(ctx: commands.Context, user: discord.Member, time: int):
    if time > 1800:
        await ctx.send("The maximum duration for removing chat privileges is 30 minutes (1800 seconds).")
        return

    total_members = len(ctx.guild.members)
    min_yes_votes = 3

    msg = await ctx.send(f"@here Shall we remove chat privileges from {user.mention} for {time} seconds?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        overwrite = ctx.channel.overwrites_for(user)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(user, overwrite=overwrite)
        await ctx.send(f"Chat privileges have been removed from {user.display_name} for {time} seconds!")
        await asyncio.sleep(time)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(user, overwrite=overwrite)
        await ctx.send(f"Chat privileges have been restored for {user.display_name} after {time} seconds!")
    else:
        await ctx.send(f"Not enough votes to remove chat privileges from {user.display_name}.")



@bot.hybrid_command()
async def removeeffects(ctx: commands.Context, user: discord.Member):
    total_members = len(ctx.guild.members)
    min_yes_votes = 5

    msg = await ctx.send(f"Shall we remove all effects on {user.mention}?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        try:
            await remove_all_effects(ctx, user)
            await ctx.send(f"All effects removed from {user.display_name}!")
        except discord.HTTPException as e:
            if e.code == 40032:
                await ctx.send("The target user is not connected to voice.")
            else:
                await ctx.send(f"An error occurred: {e}")
    else:
        await ctx.send(f"Not enough votes to remove effects from {user.display_name}.")


async def remove_all_effects(ctx, user):
    await user.remove_roles(*user.roles[1:])
    overwrite = ctx.channel.overwrites_for(user)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(user, overwrite=overwrite)


@bot.hybrid_command()
async def voteunban(ctx: commands.Context, user_id: str):
    total_members = len(ctx.guild.members)
    min_yes_votes = 6

    try:
        user = await bot.fetch_user(int(user_id))
    except discord.NotFound:
        await ctx.send("User not found.")
        return

    msg = await ctx.send(f"@here Shall we unban {user.name}#{user.discriminator}?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        try:
            await ctx.guild.unban(user)
            await ctx.send(f"{user.name}#{user.discriminator} HAS BEEN UNBANNED!")
        except discord.Forbidden:
            await ctx.send("I don't have permissions to unban users.")
    else:
        await ctx.send(f"Not enough votes to unban {user.name}#{user.discriminator}.")


@bot.hybrid_command()
async def nuke(ctx: commands.Context):
    total_members = len(ctx.guild.members)
    min_yes_votes = 3

    msg = await ctx.send("@here Are you sure you want to nuke this channel?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        await ctx.send("Nuking the channel...")
        await ctx.channel.delete()
        new_channel = await ctx.channel.clone(reason="Nuked by vote")
        await new_channel.send("Channel nuked by vote!")
    else:
        await ctx.send("Not enough votes to nuke the channel.")


@bot.hybrid_command()
async def coinflip(ctx: commands.Context, opponent: discord.Member):
    await ctx.send(f"{opponent.mention}, {ctx.author.display_name} has challenged you to a coin flip timeout!.")
    msg = await ctx.send("React with 👍 to accept the challenge, or 👎 to decline.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    accept_duration = 30

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=accept_duration,
                                         check=lambda reaction, user: user == opponent and str(reaction.emoji) in ["👍", "👎"])
    except asyncio.TimeoutError:
        await ctx.send("The challenge has timed out.")
        return

    if str(reaction.emoji) == "👎":
        await ctx.send(f"{opponent.display_name} declined the challenge.")
        return

    result = choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on {result}!")
    loser = ctx.author if result == "Heads" else opponent
    await loser.send("You lost the coin flip and have been timed out for 5 minutes!")
    await ctx.guild.get_member(loser.id).timeout(datetime.timedelta(minutes=5))
    await ctx.send(f"{loser.display_name} has been timed out for 5 minutes!")
    winner = ctx.author if loser == opponent else opponent
    await ctx.send(f"{winner.display_name} is the winner of the coin flip!")


@bot.hybrid_command()
async def changeicon(ctx: commands.Context, icon_url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as response:
                if response.status != 200:
                    await ctx.send("Failed to fetch the image.")
                    return
                icon_data = await response.read()

        await ctx.guild.edit(icon=icon_data)
        await ctx.send("Server icon changed successfully!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

participants = set()

@bot.hybrid_command()
async def roulette(ctx: commands.Context):

    participants.clear()

    msg = await ctx.send("@here Be a man and join the roulette game! You have 15 seconds.")

    await msg.add_reaction("✅")

    await asyncio.sleep(15)

    msg = await ctx.channel.fetch_message(msg.id)
    participants.clear()

    for reaction in msg.reactions:
        if str(reaction.emoji) == "✅":
            async for user in reaction.users():
                if user != bot.user:
                    participants.add(user)

    if len(participants) >= 2:
        await ctx.send("The roulette game has started")
        await roulette_round(ctx)
    else:
        await ctx.send("Not enough players to start the game. You need at least 2 players.")

async def roulette_round(ctx: commands.Context):
    while len(participants) > 1:
        # Randomly select a participant
        loser = random.choice(list(participants))

        if random.randint(1, 6) == 1:
            asyncio.create_task(timeout_player(ctx, loser))
            participants.remove(loser)
            await ctx.send(f"BANG!!!!💥💥💥⚰️ {loser.mention}")

        if len(participants) == 1:
            winner = participants.pop()
            await ctx.send(f"{winner.mention} is the last one standing! The roulette game is over.")
            return

        await ctx.send("*Click*")

    if len(participants) == 1:
        winner = participants.pop()
        await ctx.send(f"{winner.mention} is the last one standing! The roulette game is over.")

async def timeout_player(ctx: commands.Context, player: discord.Member):
    await ctx.send(f"BANG!!!!💥💥💥⚰️ {player.mention}")

    overwrite = ctx.channel.overwrites_for(player)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(player, overwrite=overwrite)

    await asyncio.sleep(300)  # Wait for 5 minutes
    overwrite.send_messages = True
    await ctx.channel.set_permissions(player, overwrite=overwrite)
    await ctx.send(f'{player.mention}\'s timeout has ended.')

@bot.hybrid_command(name='fuckawake', help='Bans a player. Only executable by Lacking.')
@commands.check(lambda ctx: ctx.author.name == "lacking8008")
async def ban(ctx, player: discord.Member):
    await player.ban()
    await ctx.send(f"{player.display_name} has been banned.")

@bot.hybrid_command()
async def enable_invites(ctx: commands.Context):
    total_members = len(ctx.guild.members)
    min_yes_votes = 3

    msg = await ctx.send("@here Are you sure you want to enable server invites?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        default_role = ctx.guild.default_role
        perms = default_role.permissions
        perms.update(send_messages=True)
        await default_role.edit(permissions=perms)
        await ctx.send("Server invites have been enabled.")
    else:
        await ctx.send("Not enough votes to enable server invites.")

@bot.hybrid_command()
async def disable_invites(ctx: commands.Context):
    total_members = len(ctx.guild.members)
    min_yes_votes = 3

    msg = await ctx.send("@here Are you sure you want to disable server invites?👍 for Yes | 👎 for No.")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    vote_duration = 30
    yes_votes = 0

    for _ in range(vote_duration):
        await asyncio.sleep(1)
        msg = await ctx.channel.fetch_message(msg.id)

        for reaction in msg.reactions:
            if str(reaction.emoji) == "👍":
                yes_votes = reaction.count - 1

    if yes_votes >= min_yes_votes:
        default_role = ctx.guild.default_role
        perms = default_role.permissions
        perms.update(send_messages=False)
        await default_role.edit(permissions=perms)
        await ctx.send("Server invites have been disabled.")
    else:
        await ctx.send("Not enough votes to disable server invites.")



@bot.hybrid_command()
async def timer(ctx: commands.Context, duration: int):
    if duration <= 0:
        await ctx.send("Please provide a positive duration.")
        return

    await ctx.send(f"Timer set for {duration} seconds.")

    await asyncio.sleep(duration)
    await ctx.send(f"{ctx.author.mention}, your {duration} timer is up!")


@bot.hybrid_command()
async def sync(ctx: commands.Context):
    await ctx.send("Syncing...")
    await bot.tree.sync()


@bot.hybrid_command()
async def showuserid(ctx: commands.Context, user: discord.Member):
    await ctx.send(f"The user ID for {user.display_name} is: {user.id}")


@bot.hybrid_command()
async def commandhelp(ctx: commands.Context):
    await ctx.send("/sync (Resets bot commands)| /showuserid (Shows userID | /votetimeout (Timeout user with set time) | "
                   "/votemute (Server mutes user with set time) | /votegag (Removes chat messages with set time) | "
                   "/voteban (Bans User) | /voteunban (Unbans User) | /changeicon (Changes server icon) | "
                   "/coinflip (Challenge a player to a coinflip) | /nuke (Nukes the channel) /timer (Sets a timer) | /removeeffects (Removes mute/gag/timeout)")


@bot.hybrid_command()
async def credit(ctx: commands.Context):
    await ctx.send("lacking8008")


@bot.hybrid_command()
async def banlist(ctx: commands.Context):
    bans = ctx.guild.bans()
    banned_users = []
    async for ban_entry in bans:
        banned_users.append(f"{ban_entry.user} (ID: {ban_entry.user.id})")

    if not banned_users:
        await ctx.send("There are no users banned in this server.")
        return

    await ctx.send(f"List of banned users:\n{', '.join(banned_users)}")


SPAM_THRESHOLD = 3  # Number of @everyone mentions within SPAM_INTERVAL to trigger anti-spam
SPAM_INTERVAL = 10


@bot.event
async def on_message(message):
    if "@everyone" in message.content:
        author = message.author
        channel = message.channel

        if author.bot or isinstance(channel, discord.DMChannel):
            return

        if not message.author.guild_permissions.mention_everyone:
            return

        recent_messages = [msg async for msg in channel.history(limit=SPAM_THRESHOLD)]

        utc_now = datetime.datetime.utcnow().replace(tzinfo=None)
        spam_count = sum(1 for m in recent_messages if m.author == author and "@everyone" in m.content and (
                    utc_now - m.created_at.replace(tzinfo=None)).total_seconds() <= SPAM_INTERVAL)

        if spam_count >= SPAM_THRESHOLD:
            overwrite = channel.overwrites_for(author)
            overwrite.send_messages = False
            await channel.set_permissions(author, overwrite=overwrite)
            await channel.send(f"{author.mention} SHUT UP.")

            await asyncio.sleep(180)

            overwrite.send_messages = True
            await channel.set_permissions(author, overwrite=overwrite)
            await channel.send(f"{author.mention} dont spam again")

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await bot.tree.sync()


bot.run(os.getenv('DISCORD_TOKEN'))
# create a .env and use this line DISCORD_TOKEN=(Discord token here)

