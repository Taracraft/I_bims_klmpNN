# -*- coding: iso-8859-1 -*-
import asyncio
import logging.handlers
import discord
from discord.utils import get

#Token einfügen
token = ''
##################################
#AB HIER NICHTS MEHR ÄNDERN
##################################





intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.presences = True
client = discord.Client(intents=discord.Intents.all())
g = client.get_guild(1089909008867012701)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='../discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('Escape from Tarkov'),
                                     status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('Raft'), status=discord.Status.online)
        await asyncio.sleep(5)


# Assign the role when the role is added as a reaction to the message.
@client.event
async def on_raw_reaction_add(payload):
    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)
    # channel and message IDs should be integer:
    if payload.channel_id == 1244009070898315274:
        if str(payload.emoji) == '\N{wrench}':
            role = get(payload.member.guild.roles, name='TWITCH')
            await member.add_roles(role)
        if str(payload.emoji) == '\N{screwdriver}':
            role = get(payload.member.guild.roles, name='FRIENDS')
            await member.add_roles(role)
        if str(payload.emoji) == '\N{telescope}':
            role = get(payload.member.guild.roles, name='GAMER')
            await member.add_roles(role)
        else:
            role = get(guild.roles, name=payload.emoji)

        if role is not None:
            if not member.bot:
                await payload.member.add_roles(role)
                channel = client.get_channel(1089909009869451277)
                await channel.send(
                    f"{member.mention} hat die {role.name} Role hinzugefügt bekommen")

# Assign the role when the role is added as a reaction to the message.
@client.event
async def on_raw_reaction_remove(payload):
    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id=payload.user_id)
    undefined = discord.utils.get(member.guild.roles, name="-undefined-")
    if payload.channel_id == 1244009070898315274:
        if str(payload.emoji) == '\N{wrench}':
            role = get(guild.roles, name='TWITCH')
            await member.remove_roles(role)
        if str(payload.emoji) == '\N{screwdriver}':
            role = get(guild.roles, name='FRIENDS')
            await member.remove_roles(role)
        if str(payload.emoji) == '\N{telescope}':
            role = get(guild.roles, name='GAMER')
            await member.remove_roles(role)
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji)

        if role is not None:
            if not member.bot:
                await payload.member.add_roles(role)
                channel = client.get_channel(1089909009869451277)
                await channel.send(
                f"{member.mention} hat die {role.name} Role entfernt bekommen")

def main():
    @client.event
    async def on_ready():
        global g
        print("Bot is ready!")
        print("Logged in as: " + client.user.name)
        print("Bot ID: " + str(client.user.id))
        for guild in client.guilds:
            print("Connected to server: {}".format(guild))
        print("------")
        client.loop.create_task(status_task())
        channels = client.get_channel(1244009070898315274)
        print('Clearing messages...')
        await channels.purge(limit=1000)
        embed = discord.Embed(title='Wähle deine Rolle',
                              description='Entscheide dich :D')
        embed.set_author(name="https://www.bad-timing.eu",url="https://www.bad-timing.eu")
        embed.add_field(name='FRIENDS', value='\N{screwdriver}', inline=True)
        embed.add_field(name='TWITCH', value='\N{wrench}', inline=True)
        embed.add_field(name='GAMER', value='\N{telescope}', inline=True)
        embed.set_footer(text='Auswahl ist erforderlich, by @Taracraft#0762')
        mess = await channels.send(embed=embed)
        await mess.add_reaction('\N{screwdriver}')
        await mess.add_reaction('\N{wrench}')
        await mess.add_reaction('\N{telescope}')


if __name__ == '__main__':
    main()
if token == (''):
    print("Token clear")
    exit()
else:
    client.run(token)
