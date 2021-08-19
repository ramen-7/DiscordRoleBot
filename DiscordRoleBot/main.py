import discord
from discord.ext import commands
from discord.utils import get
import pandas as pd
from helper_functions import make_embed


df = pd.read_csv('teams2.csv')
df2 = pd.read_csv('individual.csv')
r = len(df)
c = len(df.columns)
r2 = len(df2)
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('creating channels'))
    print("Bot is ready.")

@client.command()
@commands.has_role("Moderator")
async def channel(ctx):
    idg = ctx.message.guild.id
    guild_name = ctx.guild.name
    idc = ctx.channel.category.id
    print(idc)
    idg = int(idg)
    guild = ctx.message.guild
    print(idg)
    print(guild_name)
    category = discord.utils.get(ctx.guild.categories, id=876013167375966288)
    print(category)
    for i in range(r):
        n=df.iloc[i, 0]
        print(n)
        await ctx.guild.create_role(name=df.iloc[i, 0])
        n1 = discord.utils.get(guild.roles, name="Moderator")
        n2 = discord.utils.get(guild.roles, name=n)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            n1: discord.PermissionOverwrite(read_messages=True),
            n2: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.guild.create_text_channel(df.iloc[i, 0], category=category, overwrites=overwrites)
        await ctx.guild.create_voice_channel(df.iloc[i, 0], category=category, overwrites=overwrites)


@client.command()
@commands.has_role("Moderator")  # This must be exactly the name of the appropriate role
async def addrole(ctx, user: discord.Member, role: discord.Role):
    print(type(user))
    print(user)
    await user.add_roles(role)
    guild = ctx.message.guild
    ro = discord.utils.get(guild.roles, name=role)
    emx = make_embed(text=f"{user.mention} has been given the role {role.mention}")
    await ctx.send(embed=emx)


@client.command()
@commands.has_role("Moderator")
async def autorole(ctx):
    idg = ctx.message.guild.id
    guild = client.get_guild(idg)
    for i in range(r):
        role = df.iloc[i, 0]
        roles = get(ctx.guild.roles, name=role)
        for j in range(1, c):
            name = df.iloc[i, j]
            if type(name) == float:
                continue
            else:
                member = guild.get_member_named(name)
                if member==None:
                    emb = make_embed(text=f"{name} was not found from team {roles.mention}", color=discord.Colour.red())
                    await ctx.send(embed=emb)
                else:
                    await member.add_roles(roles)
                    emx = make_embed(text=f"{member.mention} has been given the role {roles.mention}")
                    print(member.name)
                    await ctx.send(embed=emx)

@client.command()
async def rolerequest(ctx, email):
    channel = client.get_channel(id=876022750286848020)
    idg = ctx.message.guild.id
    guild = client.get_guild(idg)
    core = discord.utils.get(guild.roles, id=870685821957701662)
    for i in range(r2):
        if email == df2.iloc[i, 2]:
            name = df2.iloc[i, 3]
            member = guild.get_member_named(name)
            print(df2.iloc[i, 5])
            role = df2.iloc[i, 5]
            roles = roles = get(ctx.guild.roles, name=role)
            emx = make_embed(text=f"{core.mention} please assign {member.mention} the role {roles.mention}")
            print(member.name)
            await channel.send(embed=emx)

client.run('ODIyMTg4NzU2ODUzMDYzNzAw.YFOo8w.tlL4WN9nzg0u8XAGw6Fm90dGTM0')
