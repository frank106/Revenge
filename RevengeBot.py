import discord
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import Bot as client
import random
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import asyncio
import json
import requests
import aiohttp
import youtube_dl
from aiohttp import ClientSession
from datetime import datetime
import os
from discord import TextChannel






def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]




client = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
client.remove_command('help')
client.launch_time = datetime.utcnow()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb , activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.users)} Users | -help"))
    print('Lets Do This Pussi!.')



@client.command()
async def ping(ctx):
    embed = discord.Embed(title='Pong?', color=0x000000)
    m = await ctx.send(embed=embed)
            
    await asyncio.sleep(1)
            
    embed = discord.Embed(title='My Connection', description=f'**My Ping Is {round(client.latency * 1000)}ms**', color=0x000000)
    await m.edit(embed=embed)




@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@client.command()
@commands.has_permissions(manage_messages=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix Changed! New Prefix ``{prefix}``', delete_after=3)


@setprefix.error
async def setprefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0x000000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}prefix <prefix wanted>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_messages``")
    	await ctx.send(embed=embed)
    else:
    	raise(error)        
        



#############################EVENTS######################


@client.event
async def on_guild_join(guild):
    names = ['gener', 'chat', 'welc', 'memb', 'bot', 'messa']

    channel = discord.utils.find(lambda channel: any(map(lambda w: w in channel.name, names)), guild.text_channels)

    embed = discord.Embed(color=0x000000, title=f"Hey! My Default Prefix Is `-`",
                          description=f"This can be changed using the command `-prefix <prefix>`\n\nIf you'd like the entire help list use `-help`\nIf you're having problems be sure to look at the `-faq` command.")
    await channel.send(embed=embed)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def servers(ctx):
    guilds = client.guilds
    gname = []
    for guild in guilds:
        gname.append(f'{guild.name}')
    gname = '\n'.join(gname)
    embed = discord.Embed(color=0x000000, title=f'Guild List.', description=f'**{gname}**', timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024")
    embed.set_footer(text=f"Developed by zrevxnge")
    await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
    embed = discord.Embed(color=0x000000, title=f"Welcome to {member.guild} {member.display_name}",
                          description=f"Do hope you enjoy your stay! You are member **{len(list(member.guild.members))}**")
    embed.set_thumbnail(url=member.avatar_url)
    await member.send(embed=embed)

    channel = discord.utils.get(member.guild.channels, name='join-leave')

    embed = discord.Embed(color=0x000000, title=f"Welcome to {member.guild}",
                          description=f"**{member}** Has entered the server.\n\n**Username** - {member}\n**ID** - `{member.id}`\n**Total Members** - {len(list(member.guild.members))}")
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    embed = discord.Embed(color=0x000000, title=f"Thanks For Visting {member.guild} {member.display_name}",
                          description=f"Hope you do come back, you'll be missed!")
    embed.set_thumbnail(url=member.avatar_url)
    await member.send(embed=embed)

    channel = discord.utils.get(member.guild.channels, name='join-leave')

    embed = discord.Embed(color=0x000000, title=f"Thanks for visting {member.guild}",
                          description=f"**{member}** Has exited the server.\n\n**Username** - {member}\n**ID** - `{member.id}`\n**Total Members** - {len(list(member.guild.members))}")
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

@client.event
async def on_message(message):

    if "discord.gg" in message.content:
        guild = message.guild

        await message.delete()

        await message.channel.send(f"{message.author.mention} You're not supposed to send discord links in here. Dont do it next time.")


        await asyncio.sleep(2)

        names = ['log']
        channel = discord.utils.find(lambda channel: any(map(lambda c: c in channel.name, names)),guild.text_channels)

        if not channel:
            await message.channel.send(f"Cant seem to find a logs channel, might wanna make one :/")


        embed = discord.Embed(timestamp=message.created_at, color=0x000000, title=f"Uh-oh someone tried to post a discord invite link.", description=f"{message.author.mention} tried posting a discord invite link. Might wanna warn them next time..")
        embed.set_thumbnail(url=message.author.avatar_url)
        await channel.send(embed=embed)
    await client.process_commands(message)

@client.event
async def on_message_delete(message):


    guild = message.guild

    names = ['log']
    channel = discord.utils.find(lambda channel: any(map(lambda c: c in channel.name, names)), guild.text_channels)



    embed = discord.Embed(title=f"Message Deleted", description=f"{message.author.mention} deleted a message.", color=0x000000, timestamp=message.created_at)
    embed.add_field(name=f"**Content Deleted**", value=message.content, inline = True)


    await channel.send(embed=embed)
    await client.process_commands(message)


#############################EVENTS######################


@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount:int):
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)
	embed = discord.Embed(color=0x000000, description=f"**{amount} Message(s) Purged**")
	await ctx.send(embed=embed, delete_after=7)




@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}purge <amount>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_messages``")
    	await ctx.send(embed=embed)
    else:
    	rasie(error)
        



@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("You're only able to kick people below you.")

    else:
        await ctx.message.delete()
        await member.kick(reason=reason)

        await member.send(f'You have been kicked from **{ctx.guild}** with the reason : `{reason}`')


        embed = discord.Embed(color=0x000000, title=f"Success.", description=f"{member} has been kicked.", timestamp=ctx.message.created_at)
        embed.add_field(name=f"**Executer**", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name=f"**Reason**", value=f"{reason}", inline=False)
        embed.add_field(name=f"**User ID**", value=f"{member.id}", inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)





@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}kick <user> <reason>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``kick_members``")
    	await ctx.send(embed=embed)
    else:
    	raise(error)    


@client.command(aliases=['gtfo'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("You're only able to ban people below you.")

    else:
        await ctx.message.delete()
        await member.ban(reason=reason)

        await member.send(f'You have been banned from **{ctx.guild}** with the reason : `{reason}`')


        embed = discord.Embed(color=0x000000, title=f"Success.", description=f"{member} has been banned.", timestamp=ctx.message.created_at)
        embed.add_field(name=f"**Executer**", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name=f"**Reason**", value=f"{reason}", inline=False)
        embed.add_field(name=f"**User ID**", value=f"{member.id}", inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)







@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}ban <user> <reason>`` or ``{ctx.prefix}gtfo <user> <reason>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``ban_members``")
    	await ctx.send(embed=embed)
    else:
    	raise(error)


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user=None):
	

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        embed = discord.Embed(description="Error: user could not be found!",color=0x000000)
        await ctx.send(embed=embed)
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Unbanned by "+ str(ctx.author))
        else:
            embed1 = discord.Embed(description="User not banned!",color=0x000000)
            await ctx.send(embed=embed1)
            return

    except discord.Forbidden:
        embed2 = discord.Embed(description="I do not have permission to unban!", color=0x000000)
        await ctx.send(embed=embed2)
        return

    except:
        embed3 = discord.Embed(description="Unbanning failed!", color=0x000000)
        await ctx.send(embed=embed3)
        return

    embed4 = discord.Embed(description=f"Successfully unbanned {user.mention}!", color=0x000000)
    await ctx.send(embed=embed4)



@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
    	embed = discord.Embed(color=0x000000, title=f"Missing Arguments.", description=f"Usage: ``{ctx.prefix}unban <user>``")
    	await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``ban_members``")
    	await ctx.send(embed=embed)
    else:
    	raise(error)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        await ctx.send(f"No muted role found, creating one now.")
        try:
            muted = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role")

        await member.add_roles(muted)
        embed = discord.Embed(color=0x000000, title=f"Success.", description=f"{member} has been muted.",
                              timestamp=ctx.message.created_at)
        embed.add_field(name=f"**Executer**", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name=f"**Reason**", value=f"{reason}", inline=False)
        embed.add_field(name=f"**User ID**", value=f"{member.id}", inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
    else:
        await member.add_roles(role)
        embed = discord.Embed(color=0x000000, title=f"Success.", description=f"{member} has been muted.",
                              timestamp=ctx.message.created_at)
        embed.add_field(name=f"**Executer**", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name=f"**Reason**", value=f"{reason}", inline=False)
        embed.add_field(name=f"**User ID**", value=f"{member.id}", inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)




@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}mute <user> ``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_roles``")
    	await ctx.send(embed=embed)
    else:
    	raise error



@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):

    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Muted":
            muted = role

    await member.remove_roles(muted)
    embed = discord.Embed(color=0x000000, title=f"Success.", description=f"{member} has been muted.",
                          timestamp=ctx.message.created_at)
    embed.add_field(name=f"**Executer**", value=f"{ctx.author.mention}", inline=False)
    embed.add_field(name=f"**User ID**", value=f"{member.id}", inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}unmute <user>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_roles``")
    	await ctx.send(embed=embed)
    else:
    	raise error





###############################################HELP#########################################################




@client.group()
async def help(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if ctx.invoked_subcommand is None:
        embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at, description=f"**Use `-faq` to get more info**")
        embed.add_field(name="<:700418662259228682:743388670052270163> **View Mod/Admin Commands**",
                        value="`help mod`",
                        inline=False)

        embed.add_field(name="<:724777639092682782:743388648539684913> **View Fun Commands**",
                        value="`help fun` ",
                        inline=False)
        embed.add_field(name=f":gear: **View Other Commands**", value="`help other`", inline=False)
        embed.add_field(name=f":link: **View Links**", value=f"`help links`")
        embed.add_field(name=f"<a:check:729584596924235897> **Uptime**", value=f"`{days} days {hours} hours {minutes} minutes and {seconds}s`", inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024')
        await ctx.send(embed=embed)



@help.command()
async def links(ctx):
    embed4 = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
    embed4.add_field(name=f"**LINKS (3)**",
                     value=f"**[Support Server](https://discord.com/invite/qdJMaus)**\n"
                     "**[Vote](https://glennbotlist.xyz/bot/704452467995312139/vote)**\n"
                     "**[Invite](https://discord.com/oauth2/authorize?client_id=704452467995312139&permissions=8&scope=bot)**")
    embed4.set_thumbnail(url='https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024')
    await ctx.send(embed = embed4)


@help.command()
async def fun(ctx):
    embed1 = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
    embed1.add_field(name="**FUN COMMANDS (10)**",
                    value="**`Joke`, "
                          "`Avatar`, "
                          "`Howgay`, "
                          "`8ball`, "
                          "`IQ`,"
                          "`Hack`,"
                          "`Meme`,"
                          "`Insta`,"
                          "`Randomfact`**",

                    inline=False)
    embed1.set_thumbnail(url='https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024')
    await ctx.send(embed = embed1)


@help.command()
async def other(ctx):
    embed2 = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
    embed2.add_field(name="**OTHER COMMANDS (6)**",
                    value="`Ping`,"
                          "`Invite`,"
                          "`Userinfo`,"
                          "`Serverinfo`,"
                          "`Botinfo`,"
                          "`Quote`,"
                          "`Nsfw`,"
                          "`Faq`",
                    inline=False)
    embed2.set_thumbnail(url='https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024')
    await ctx.send(embed = embed2)


@help.command()
async def mod(ctx):
    embed3 = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
    embed3.add_field(name=f"**MOD/ADMIN COMMANDS (14)**",
                     value=f"`Ban`,"
                            "`Unban`,"
                            "`Kick`,"
                            "`Mute`,"
                            "`Unmute`,"
                            "`Purge`,"
                            "`Setprefix`,"
                            "`Addrole`,"
                            "`Derole`,"
                            "`Lock`,"
                            "`Unlock`,"
                            "`DM`,"
                            "`Warn`,"
                            "`Poll`,"
                            "`channelinfo`,"
                            "`slowmode`,",
                     inline=False)
    embed3.set_thumbnail(url='https://cdn.discordapp.com/icons/733866630236602402/c8c712b7e321aa02344dfdd730442fc7.webp?size=1024')
    await ctx.send(embed = embed3)


    message = await ctx.send(embed=embed)
    await message.add_reaction('<a:lick:729060118603497482>')




#############################HELP######################################################


@client.command()
async def invite(ctx):
	embed = discord.Embed(title="**Want Me In Your Server?**", color=0x000000)
	embed.add_field(name="**Heres An Invite Link**", value="[Click Here!](https://discord.com/api/oauth2/authorize?client_id=704452467995312139&permissions=8&scope=bot)", inline=True)
	embed.set_footer(text=f"Requested By {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)



@client.command()
async def avatar(ctx, member: discord.Member = None):

	member = ctx.author if not member else member

	embed = discord.Embed(color=0x000000, title=f"**{member.display_name}'s avatar.**")
	embed.set_image(url=member.avatar_url)

	await ctx.send(embed=embed) 








@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def userinfo(ctx, member: discord.Member = None):
    embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at, title=f"UserInfo")

    member = ctx.author if not member else member


    roles = [role for role in member.roles]

    embed.add_field(name=f"**User**", value=f"{member}", inline=False)
    embed.add_field(name=f"**User ID**", value=member.id, inline=False)
    embed.add_field(name=f"**Account Created On**", value=member.created_at.strftime("%a, %B %#d %Y "), inline=False)
    embed.add_field(name=f"**Joined Server On**", value=member.joined_at.strftime("%a, %B %#d %Y "), inline=False)
    embed.add_field(name=f"**Roles**", value=" ".join([role.mention for role in roles]), inline=False)
    embed.add_field(name=f"**Status**", value=member.status, inline=False)
    embed.add_field(name=f"**Playing**", value=member.activity, inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)




@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Youre on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error	



@client.command()
async def serverinfo(ctx):




	embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at, title="**Server Info.**")
	embed.add_field(name=f"**Name**", value=ctx.guild.name)
	embed.add_field(name=f"**ID**", value=ctx.guild.id, inline=False)
	embed.add_field(name=f"**Owner**", value=ctx.guild.owner.mention, inline=False)
	embed.add_field(name=f"**Region**", value=ctx.guild.region, inline=False)
	embed.add_field(name=f"**Created On**", value=ctx.guild.created_at.strftime("%a, %B %#d %Y"), inline=False)
	embed.add_field(name=f"**Member Count**", value=len(ctx.guild.members), inline=True)
	embed.add_field(name=f"**Role Amount**", value=len(ctx.guild.roles), inline=True)
	embed.add_field(name=f'**Banned Members**', value=f'{len(await ctx.guild.bans())}', inline=True)
	embed.set_thumbnail(url=ctx.guild.icon_url)
	embed.set_footer(text=f"Requested By {ctx.author.display_name}")
	await ctx.send(embed=embed)







@client.command()
async def howgay(ctx, member: discord.Member = None):
	member = ctx.author if not member else member

	gay = random.randint(1, 100)
	embed = discord.Embed(color=0x000000, title=f"Look At This Faggot.", description=f"{member.mention} Is {gay}% Gay.")
	message = await ctx.send(embed=embed)
	await message.add_reaction("🏳️‍🌈")

    










#######################NSFW COMMANDS#######################################
@client.command()
async def nsfw(ctx):
    embed = discord.Embed(color=0x000000, title=f"NSFW Commands.",
                          description=f"**All NSFW Commands Are Only Usable In NSFW Marked Channels.**")
    embed.add_field(name=f"Anime NSFW", value=f"**Pussy** - Generates Random Pussy Gif \n"
                                              "**Boobs** -  Generates Random Boobs Gif \n"
                                              "**Hentai** -  Generates Random Hentai Gif \n"
                                              "**Lesbian** - Generates Random Lesbian Gif \n", inline=False)
    embed.add_field(name=f"Non Anime NSFW", value=f"**nPussy** - Generates Random Pussy Photo \n"
                                                  "**Thigh** - Generates Random Thigh Photo \n"
                                                  "**nAnal** - Generates Random Anal Gif/Photo \n"
                                                  "**n4k** - Generates Random 4k Photo \n"
                                                  "**ass** Generates Random Booty Picture \n")
    await ctx.send(embed=embed)


@client.command()
async def hentai(ctx):
    if ctx.channel.is_nsfw():
        r = requests.get('https://nekos.life/api/v2/img/Random_hentai_gif')
        res = r.json()
        embed = discord.Embed()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Please use an NSFW channel.", color=0x000000)
        await ctx.send(embed=embed)


@client.command()
async def boobs(ctx):
    if ctx.channel.is_nsfw():
        r = requests.get('https://nekos.life/api/v2/img/boobs')
        res = r.json()
        embed = discord.Embed()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Please use an NSFW channel.", color=0x000000)
        await ctx.send(embed=embed)


@client.command()
async def lesbian(ctx):
    if ctx.channel.is_nsfw():
        r = requests.get('https://nekos.life/api/v2/img/les')
        res = r.json()
        embed = discord.Embed()
        embed.set_image(url=res['url'])
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Please use an NSFW channel.", color=0x000000)
        await ctx.send(embed=embed)


@client.command()
async def pussy(ctx):
    if ctx.channel.is_nsfw():
        await ctx.message.delete()
        r = requests.get('https://nekos.life/api/v2/img/pussy')
        pussy = r.json()
        embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
        embed.set_image(url=pussy['url'])
        await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')


@client.command()
async def npussy(ctx):
    if ctx.channel.is_nsfw():

        await ctx.send(f'<a:loading:742950213630689454> | Gimme a second please.', delete_after=3)

        await asyncio.sleep(3)

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://nekobot.xyz/api/image?type=pussy') as r:
                res = await r.json()
                embed = discord.Embed(color=0x000000)
                embed.set_image(url=res['message'])
                await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')


@client.command()
async def thigh(ctx):
    if ctx.channel.is_nsfw():

        await ctx.send(f'<a:loading:742950213630689454> | Gimme a second please.', delete_after=3)

        await asyncio.sleep(3)

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://nekobot.xyz/api/image?type=thigh') as r:
                res = await r.json()
                embed = discord.Embed(color=0x000000)
                embed.set_image(url=res['message'])
                await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')


@client.command()
async def nanal(ctx):
    if ctx.channel.is_nsfw():

        await ctx.send(f'<a:loading:742950213630689454> | Gimme a second please.', delete_after=3)

        await asyncio.sleep(3)

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://nekobot.xyz/api/image?type=anal') as r:
                res = await r.json()
                embed = discord.Embed(color=0x000000)
                embed.set_image(url=res['message'])
                await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')


@client.command()
async def ass(ctx):
    if ctx.channel.is_nsfw():

        await ctx.send(f'Gimme a second please.', delete_after=3)

        await asyncio.sleep(3)

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://nekobot.xyz/api/image?type=ass') as r:
                res = await r.json()
                embed = discord.Embed(color=0x000000)
                embed.set_image(url=res['message'])
                await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')


@client.command()
async def n4k(ctx):
    if ctx.channel.is_nsfw():

        await ctx.send(f'Gimme a second please.', delete_after=3)

        await asyncio.sleep(3)

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://nekobot.xyz/api/image?type=4k') as r:
                res = await r.json()
                embed = discord.Embed(color=0x000000)
                embed.set_image(url=res['message'])
                await ctx.send(embed=embed)
    else:
        await ctx.send('Please use an NSFW channel.')

##############################OTHER##################################################################



@client.command()
async def botinfo(ctx):


	embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at, title="__**Revenge Info**__")
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/704452467995312139/22002c22ce1f34977aa6091629fc2f3e.webp?size=1024")
	embed.add_field(name="**Created**", value="**4/27/2020**")
	embed.add_field(name="**Developer**", value="``zrevxnge#0999``")
	embed.add_field(name="**Discord Library**", value="Discord.py", inline=True)
	embed.add_field(name="**Language**", value="Python", inline=True)
	embed.add_field(name="**Users**", value=f"{len(client.users)}")
	embed.add_field(name="**Servers**", value=f"{len(client.guilds)}")
	embed.add_field(name="__**Instagram**__", value="[Click Here](https://www.instagram.com/zrevxnge/)")
	embed.add_field(name="__**Twitter**__", value="[Click Here](https://twitter.com/zrevxnge)", inline=True)


	await ctx.send(embed=embed)


  

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: TextChannel, *, message):

    embed = discord.Embed(color=0x000000, title='Announcement', description=f'{message}', timestamp=ctx.message.created_at)

    await channel.send(embed=embed)
    await ctx.message.delete()

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}announce <#channel> <message>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``Administrator``")
    	await ctx.send(embed=embed)
    else:
    	raise(error)



###########################MUSIC#############################

@client.command(pass_context=True, aliases=['j'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await ctx.send(f"Ay, Wassup! I Joined {channel}")


@client.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'I Left {channel} :(')
    else:
        await ctx.send('Im Not In A Voice Channel.')


   
###########################MUSIC#############################



@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don’t count on it",
                 "It is certain",
                 "It is decidedly so",
                 "Most likely",
                 "My reply is no",
                 "My sources say no",
                 "Outlook good",
                 "Outlook not so good",
                 "Reply hazy try again",
                 "Signs point to yes",
                 "Very doubtful",
                 "Without a doubt",
                 "Yes",
                 "Yes, definitely",
                 "You may rely on it"]
    embed = discord.Embed(color=0x000000, title=f"8Ball")
    embed.add_field(name=f'**Question:**', value=(f"``{question}`` \n \n"
    	                                      f"**Answer**: \n"
    	                                      f"{random.choice(responses)}"))
    embed.set_thumbnail(url='https://www.vippng.com/png/full/0-3078_download-png-image-report-8-ball-icon-png.png')
    await ctx.send(embed=embed)


@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}8ball <question>``")
        await ctx.send(embed=embed)          
    






@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
	await member.add_roles(role)
	embed = discord.Embed(color=0x000000, title=f"Role Given.", description=f":white_check_mark: {member.mention}, Has been given the {role.mention} Role!")
	await ctx.send(embed=embed)

    



@addrole.error
async def addrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}addrole <user> <role name>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_roles``")
    	await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Role not found.")
    else:
    	raise(error)






@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def derole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)

    embed = discord.Embed(color=0xFF0000, title=f"Role Taken.", description=f":white_check_mark: {member.mention}, Has had the Role {role.mention} taken!")
    await ctx.send(embed=embed)

    


@derole.error
async def derole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}derole <user> <role name>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_roles``")
    	await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Role not found.")
    else:
    	raise(error)





@client.command()
async def quote(ctx):
    results = requests.get('https://type.fit/api/quotes').json()
    num = random.randint(1, 1500)
    content = results[num]['text']

    await ctx.send(content)




@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"Channel Locked!")

@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_channels``")
        await ctx.send(embed=embed)





@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"Channel Unlocked!")


@unlock.error
async def unlock_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
	    embed = discord.Embed(title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_channels``", color=0x000000)
	    await ctx.send(embed=embed)





@client.command()
async def randomnumber(ctx):
    embed = discord.Embed(title= "Here Is Your Random Number.", description=(random.randint(1, 150)), color=0x000000, timestamp=ctx.message.created_at)
    await ctx.send(embed=embed)



@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def dm(ctx,  member: discord.Member, *, message):
    await ctx.message.delete()
    await member.send(message)
    embed = discord.Embed(color=0x000000, title=f"Success", description=f"Direct Message Sent!", timestamp=ctx.message.created_at)
    embed.add_field(name=f"**Sent By**", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name=f"**Message**", value=f"{message}", inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)



@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Youre on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_messages``")
    	await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
    	embed = discord.Embed(color=0x000000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}dm <user> <message>``")
    	await ctx.send(embed=embed)
    else:
    	rasie(error)
    	







@client.command()
async def dmowner(ctx, *, content):
    guild = ctx.guild
    channel = await guild.owner.create_dm()
    embed = discord.Embed(color=0x000000, description=f"**Message from {ctx.author.display_name}**\n{content}")
    await channel.send(embed=embed)
    await ctx.send(f"Message sent to {ctx.guild.owner.mention}")



@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, content):
    await ctx.message.delete()
    embed = discord.Embed(color=0x000000, title=f"Woah, Chill. You've Just Got Warned.", timestamp=ctx.message.created_at)
    embed.add_field(name=f"**Reason**", value=f"{content}", inline=False)
    embed.add_field(name=f"**Warned By**", value=f"{ctx.author.display_name}", inline=False)
    embed.add_field(name=f"**Server**", value=f"{ctx.guild.name}", inline=False)
    await member.send(embed=embed)

    embed = discord.Embed(color=0x000000, title=f"Success", description=f"{member.mention} Has Been Warned!", timestamp=ctx.message.created_at)
    embed.add_field(name=f"**Warned By**", value=f"{ctx.author.mention}", inline=True)
    embed.add_field(name=f"**Reason**", value=f"``{content}``", inline=True)
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}warn <user> <warning>``")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_messages``")
    	await ctx.send(embed=embed)
    else:
    	rasie(error)









@client.command()
async def iq(ctx, member: discord.Member = None):
	member = ctx.author if not member else member

	iq = random.randint(1, 200)
	await ctx.send(f"{member.mention}'s IQ Is {iq}.")

@iq.error
async def iq_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}iq <user>``")
        await ctx.send(embed=embed)





@client.command()
async def hack(ctx, member: discord.Member = None):


    passwords=['imnothackedlmao','sendnoodles63','ilovenoodles','icantcode','christianmicraft','server','icantspell','hackedlmao','WOWTONIGHT','69', 'ilovefn123']
    fakeips=['154.2345.24.743','255.255.255.0','356.653.56','101.12.8.6053','255.255.255.0']

    embed = discord.Embed(title=f"{member.display_name} info ", description=f"Email `{member.display_name}@gmail.com` Password `{random.choice(passwords)}`  IP `{random.choice(fakeips)}`", color=0x000000)
    embed.set_footer(text="You've totally been hacked ")
    await ctx.send(embed=embed)

@hack.error
async def hack_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}hack <user>``")
        await ctx.send(embed=embed)


@client.command()
async def thot(ctx, member: discord.Member = None):
	member = ctx.author if not member else member

	thot = random.randint(1, 200)
	embed = discord.Embed(color=0x000000, title=f"THOT DETECTED!", description=f"{member.mention} Is {thot}% A Thot. \n\n BE GONE THOT!", timestamp=ctx.message.created_at)
	await ctx.send(embed=embed)





@client.command()
async def penis(ctx, member: discord.Member):
    slap = ['8=D',
             '8==D',
             '8====D',
             '8=========D',
             '8===================D']
    await ctx.send(f"{member.mention}'s Penis Size Is {random.choice(slap)}")         

@penis.error
async def penis_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}penis <user>``")
        await ctx.send(embed=embed)




@client.command()
async def insta(ctx, username):
	await ctx.send(f'Gathering Info On {username}', delete_after=2)

	await asyncio.sleep(2)




	url = f"https://apis.duncte123.me/insta/{username}"
	async with ClientSession() as session:
		async with session.get(url) as response:
			r = await response.json()
			data = r['user']
			username = data['username']
			followers = data['followers']['count']
			following = data['following']['count']
			uploads = data['uploads']['count']
			biography = data['biography']
			private = data['is_private']
			verified = data['is_verified']

			embed = discord.Embed(color=0x000000, description=f"{ctx.author.mention} Requested Info On ``{username}``", timestamp=ctx.message.created_at)
			embed.add_field(name='Bio', value=biography + '\u200b', inline=False)
			embed.add_field(name='Private Status', value=private)
			embed.add_field(name='Verified Status', value=verified)
			embed.add_field(name='Followers', value=followers)
			embed.add_field(name='Following', value=following)
			embed.add_field(name='Posts', value=uploads)
			embed.set_thumbnail(url=f'http://clipart-library.com/image_gallery2/Instagram-PNG-Picture.png')
			await ctx.send(embed=embed)

@insta.error
async def insta_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0xFF0000, title=f"**Missing Arguments!**", description=f"Usage: ``{ctx.prefix}insta <instagram handle>``")
        await ctx.send(embed=embed)      

@client.command()
async def meme(ctx):
    embed = discord.Embed(color=0x000000, title=f"Fetching Meme From Reddit.")
    fetch = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    req = requests.get("https://apis.duncte123.me/meme")
    meme = req.json()
    embed = discord.Embed(color=0x000000, description=f"**[{meme['data']['title']}]({meme['data']['url']})**", timestamp=ctx.message.created_at)
    embed.set_image(url=meme['data']['image'])
    await fetch.edit(embed=embed)


@client.command()
async def randomfact(ctx):
	url = f'https://uselessfacts.jsph.pl/random.json?language=en'
	async with ClientSession() as session:
		async with session.get(url) as response:
			r = await response.json()
			fact = r['text']
			embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at)
			embed.add_field(name=f"**Random Fact**", value=fact)
			await ctx.send(embed=embed)



@client.command()
async def joke(ctx):
    embed = discord.Embed(color=0x000000, title=f"Fetching Joke From Reddit.")
    fetch = await ctx.send(embed=embed)
    await asyncio.sleep(2)
    req = requests.get("https://apis.duncte123.me/joke")
    joke = req.json()
    embed = discord.Embed(color=0x000000, title=f"Random Reddit Joke.", timestamp=ctx.message.created_at, description=f"{joke['data']['title']} \n{joke['data']['body']}")
    await fetch.edit(embed=embed)





@client.command()
async def suggest(ctx, *, sug):
    await ctx.message.delete()

    embed = discord.Embed(title=f"Success.", description=f"**Your Suggestion Has Been Sumbitted.**", color=0x000000)
    embed.add_field(name=f"**Suggestion**", value=f"{sug}", inline=False)
    embed.add_field(name=f"**Sumbitted By**", value=f"{ctx.author.mention}", inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"React To Leave Your Opinion.")
    channel = ctx.guild.get_channel(735327449545441292)
    message = await channel.send(embed=embed)
    await message.add_reaction("☑")
    await message.add_reaction("🚫")




@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.delete()
    await ctx.send("Im Shutting Down :(", delete_after=5)
        
    await asyncio.sleep(1)
        
    await client.logout()


@client.command(pass_context=True)
@commands.is_owner()
async def restart(ctx):
    try:
        await ctx.send("Give me a second daddy.")
        await client.close()
    except:
        pass
    finally:
        os.system("py -3 RevengeBot.py")


@shutdown.error
async def shutdown_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		embed = discord.Embed(color=0x000000, title=f"You're Not Allowed To Use This Command!")
		await ctx.send(embed=embed, delete_after=2)


@client.command()
@commands.has_permissions(administrator=True)
async def poll(ctx, *, poll):
	await ctx.message.delete()

	embed = discord.Embed(title=f"Poll Created By {ctx.author.display_name}", description=f"**{poll}**", color=0x000000, timestamp=ctx.message.created_at)
	embed.set_footer(text=f"React To Leave Your Opinion.")
	message = await ctx.send(embed=embed)
	await message.add_reaction('☑️')
	await message.add_reaction('🚫')



@client.command()
@commands.is_owner()
async def changelog(ctx, *, text=None):

	embed = discord.Embed(color=0x000000, title='Change-Logs', description=f'{text}', timestamp=ctx.message.created_at)
	channel = ctx.guild.get_channel(735603324073672834)
	await channel.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def channelinfo(ctx, channel: discord.TextChannel):



    embed = discord.Embed(title=f"Info for {channel}",description=f"**Name -** {channel.mention}\n**ID -** {channel.id}\n**Topic -** {channel.topic}\n**Position -** {channel.position}\n**Slowmode Delay -** {channel.slowmode_delay}\n**NSFW?** {channel.is_nsfw()}\n**Under Category -** {channel.category}\n**Created At -** {channel.created_at.strftime('%m/%d/%Y')}",color=0x000000)


    await ctx.send(embed=embed)


@client.command()
async def geolook(ctx, *, ipaddr: str = '1.3.3.7'):

    await ctx.send(f'<a:yessir:740086915315007519> |Searching..', delete_after=3)

    await asyncio.sleep(3)

    r = requests.get(f'https://extreme-ip-lookup.com/json/{ipaddr}')
    geo = r.json()
    country = geo['countryCode']
    embed = discord.Embed(color=0x000000, title=f"IP Lookup.", timestamp=ctx.message.created_at)
    fields = [
        {'name': 'IP', 'value': geo['query']},
        {'name': 'ipType', 'value': geo['ipType']},
        {'name': 'Country', 'value': geo['country']},
        {'name': 'City', 'value': geo['city']},
        {'name': 'ISP', 'value': geo['isp']},
        {'name': 'Region', 'value': geo['region']},
        {'name': 'Status', 'value': geo['status']},
        {'name': 'Longitude', 'value': geo['lon']},
        {'name': 'Latitude', 'value': geo['lat']}
    ]

    for field in fields:
        if field['value']:
            embed.add_field(name=field['name'], value=field['value'], inline=True)
            embed.set_thumbnail(url=f"https://www.countryflags.io/{country}/flat/64.png")
            embed.set_footer(text=f"Revenge Bot")
    return await ctx.send(embed=embed)


@client.command()
async def faq(ctx):
    embed = discord.Embed(color=0x000000, title=f"FAQ")
    embed.add_field(name=f"**Why arent the moderation commands working?**",
                    value=f"Make sure that the bots role, is above any other roles. That way, all moderation/administrator commands will work.",
                    inline=False)
    embed.add_field(name=f"**How do i see join/leave messages?**",
                    value=f"Indeed make sure that you have a channel called `join-leave` for the bot to send welcome messages. Please note that i am trying to make these messages, more customizable.",
                    inline=False)
    embed.add_field(name=f"**How can i change the bots prefix?**",
                    value=f"The prefix can be changed by using the command `-prefix <prefix>`", inline=False)
    embed.add_field(name=f"**Further support here.**", value=f"[Support Discord](http://discord.gg/qdJMaus)")
    await ctx.send(embed=embed)



@client.group()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx):
    if ctx.invoked_subcommand is None:

        embed = discord.Embed(color=0xFF0000, title=f"Missing Arugments.", description=f"Usage: `{ctx.prefix}slowmode <on/off> <time>`")
        await ctx.send(embed=embed)

@slowmode.command()
async def on(ctx, slowmode: int):
    await ctx.channel.edit(slowmode_delay=slowmode)
    await ctx.send(f"Slowmode delay set to {slowmode}'s")


@slowmode.command()
async def off(ctx):
    await ctx.channel.edit(slowmode_delay=0)
    await ctx.send(f"Slowmode delay disabled.")


async def slowmode_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
    	embed = discord.Embed(color=0xFF0000, title=f"You're Not Allowed To Use This.", description=f"Permissions Needed \n ``manage_channels``")
    	await ctx.send(embed=embed)





@client.command()
async def guildicon(ctx):
    embed = discord.Embed(title=ctx.guild.name, color=0x000000)
    embed.set_image(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)







@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(color=0x000000, title=f"**🚫 Command Not Found!**")
        await ctx.send(embed=embed)





client.run(Token)
