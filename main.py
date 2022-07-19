import discord
from discord.ext import commands
import os
import asyncio
import time
import datetime
import time
from discord.ext import commands
from discord.ext.commands.core import command
from Cogs.Antinuke import Antinuke
from keep_alive import keep_alive
import datetime
import requests
import json



def cls():
  os.system("clear")

verif = "<a:TICK:998127027871809646>"

color = 00000

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.webhooks = True
intents = intents

prefix = '-'

client = commands.Bot(command_prefix='-', case_insensitive=False, intents=intents)

client.remove_command('help')

client.add_cog(Antinuke(client))


with open('whitelisted.json') as f:
  whitelisted = json.load(f)





import tracemalloc

tracemalloc.start()

#for filename in os.listdir('./cogs'):
  #if filename.endswith('.py'):
    #client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
  print(f"Logged In As {client.user}")

def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 806519089144135720

def botowner(ctx):
  return ctx.message.author.id == 806519089144135720 or ctx.message.author.id == 806519089144135720

@client.listen("on_guild_join")
async def update_json(guild):
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(guild.id) not in whitelisted:
      whitelisted[str(guild.id)] = []


    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)

@commands.check(botowner)
@client.command()
async def gsetup(ctx):
  for guild in client.guilds:
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(guild.id) not in whitelisted:
      whitelisted[str(guild.id)] = []


    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)

@gsetup.error
async def gsetup_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("You Cant Use This Command")

      
#@client.command()
#async def g(ctx):
  #for guild in list(client.guilds):
   # with open ('whitelisted.json', 'r') as f:
       # whitelisted = json.load(f)


    #if str(guild.id) not in whitelisted:
      #*whitelisted[str(guild.id)] = []


    #with open ('whitelisted.json', 'w') as f: 
       # json.dump(whitelisted, f, indent=4)

@commands.check(is_server_owner)
@client.command(aliases = ['wld'])
async def whitelisted(ctx):

  embed = discord.Embed(title=f"Whitelisted users for {ctx.guild.name}", description="")

  with open ('whitelisted.json', 'r') as i:
        whitelisted = json.load(i)
  try:
    for u in whitelisted[str(ctx.guild.id)]:
      embed.description += f"<@{(u)}> - {u}\n"
    await ctx.reply(embed = embed)
  except KeyError:
    await ctx.reply("Nothing found for this guild!")

@client.command(aliases = ['wl'])
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
    if user is None:
        await ctx.reply("You must specify a user to whitelist.")
        return
    with open ('whitelisted.json', 'r') as f:
        whitelisted = json.load(f)


    if str(ctx.guild.id) not in whitelisted:
      whitelisted[str(ctx.guild.id)] = []
    else:
      if str(user.id) not in whitelisted[str(ctx.guild.id)]:
        whitelisted[str(ctx.guild.id)].append(str(user.id))
      else:
        await ctx.reply("That user is already in the whitelist.")
        return



    with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
    await ctx.reply(f"{user} has been added to the whitelist.")

@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can whitelist!")

@whitelisted.error
async def whitelisted_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can whitelisted!")

@client.command(aliases = ['uwl'])
@commands.check(is_server_owner)
async def unwhitelist(ctx, user: discord.User = None):
  if user is None:
      await ctx.reply("You must specify a user to unwhitelist.")
      return
  with open ('whitelisted.json', 'r') as f:
      whitelisted = json.load(f)
  try:
    if str(user.id) in whitelisted[str(ctx.guild.id)]:
      whitelisted[str(ctx.guild.id)].remove(str(user.id))
      
      with open ('whitelisted.json', 'w') as f: 
        json.dump(whitelisted, f, indent=4)
    
      await ctx.reply(f"{user} has been removed from the whitelist.")
  except KeyError:
    await ctx.reply("This user was never whitelisted.")
                             
#cls()

@unwhitelist.error
async def unwhitelist_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry but only the guild owner can unwhitelist!")    


def clean_code(content):
    """Automatically removes code blocks from the code."""
     #remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


import datetime
import io
import contextlib
import textwrap

os.system("pip install buttons")

from discord.ext.buttons import Paginator




class Pag(Paginator):
    async def teardown(ctx):
        try:
            await ctx.page.clear_reactions()
        except discord.HTTPException:
            pass

from traceback import format_exception


@commands.check(botowner)
@client.command(name="eval", aliases=["exec", "execute", "codexe", "jsk"])
async def _eval(ctx, *, code):
    code = clean_code(code)

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": client,
        "token": token,
        "client": client,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",
                local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"

    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
        timeout=180,
        use_defaults=True,
        entries=[result[i : i + 2000] for i in range(0, len(result), 2000)],
        length=1,
        prefix="```py\n",
        suffix="```",
    )

    await pager.start(ctx)



@_eval.error
async def _eval_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("You Can't Use This Command")

@client.event
async def on_guild_channel_create(ch):
    try:
        with open('whitelisted.json') as f:
          whitelisted = json.load(f)
        async for i in ch.guild.audit_logs(limit = 1 , action = discord.AuditLogAction.channel_create):
          if str(i.user.id) in whitelisted[str(i.guild.id)]:
            return
          if ch.user.id == 916905573826560010:
            return
          await ch.guild.ban(i.user , reason = " ViRTUCY SECURITY | Anti Channel")
          await ch.delete()
    except Exception as e:
        print(e)

@client.command(description='Unmutes a specified user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get((ctx.guild.roles), name='RD SELF BOT MUTED')
    await member.remove_roles(mutedRole)
    await member.send(f" YOU HAVE BEEN UNMUTED: - {ctx.guild.name}")
    embed = discord.Embed(title='RD SELF BOT || discord.gg/rdop', description=f" UNMUTE-{member.mention}", colour=(discord.Colour.light_gray()))
    await ctx.send(embed=embed)


@client.command()
async def blue(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    bluerole = discord.utils.get((guild.roles), name='Blue')
    if not bluerole:
        bluerole = await guild.create_role(name='Blue')
        await bluerole.edit(colour=0xFFFF00)

    embed = discord.Embed(description=f"{member.mention} Gave You {bluerole.mention} Role and You have Blue Role Now!", colour=(discord.Colour.light_gray()))
    embed.add_field(name='REASON:', value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(bluerole, reason=reason)


@client.event
async def on_webhooks_update(webhook):
  try:
    with open('whitelisted.json') as f:
      whitelisted = json.load(f) 
    reason = "ViRTUCY SECURITY | Anti Webhook"
    guild = webhook.guild
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create).flatten()
    logs = logs[0]
    if str(logs.user.id) in whitelisted[str(logs.guild.id)]:
      return
    requests.delete(webhook)
    await logs.user.ban(reason=f"{reason}")
  except:
    pass

@client.event
async def on_message(message):
  await client.process_commands(message)
  member = message.author
  guild = message.guild
  if message.mention_everyone:
    if member == guild.owner or str(member.id) in whitelisted[str(guild.id)]:
      pass
    else:
      await message.delete()
      await member.ban(reason="ViRTUCY SECURITY | Mentioning everyone/here")
#  else:
    #if message.embeds:
      #if member.bot:
        #pass
      #else:
          #await member.kick(reason="Foxy Security | Anti Selfbot")
         # await message.delete()
          #await message.channel.send(f"**<@{member.id}> <a:CrossNo:891566375011745792> Selfbots Isn't Allowed**")
   # else:
     # role = "<@&"
      #if role in message.content:
      #  if member == guild.owner:
         # pass
       # else:
         # await message.delete()
         # await member.ban(reason="Foxy Security | Anti Role Ping")
          



@client.command()
async def invite(ctx):
        embed = discord.Embed(color=00000, description=f"** Invite  \n[Click Here](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot) To Invite Me!\n[Click Here](https://discord.gg/P864wDCZyx) discord To Join Support Server!**")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/RZ2prqSvT3OAmq3yoSdbJma3CsEZ8sUtwyQQz5lFWYA/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/861814656851378176/89e3d2d738dbe51b1890be62b8bbf3c3.png")
        await ctx.reply(embed=embed, mention_author=True)

@client.command()
async def help(ctx):
        embed = discord.Embed(color=000000, title="ViRTUCY SECURITY",description=f"**<a:16Crown:947457656434589706> Help Menu <a:16Crown:947457656434589706>\n[Invite](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)\n[Support](https://discord.gg/P864wDCZyx)**")
        embed.set_footer(text=f"Prasoon :c  | Ping {int(round(client.latency * 10))}ms!")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/RZ2prqSvT3OAmq3yoSdbJma3CsEZ8sUtwyQQz5lFWYA/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/861814656851378176/89e3d2d738dbe51b1890be62b8bbf3c3.png")
 
        embed.add_field(name=f"<:btannouncements:947449702457171989> Help", value="```Shows Help Command```")
        embed.add_field(name=f"<:btannouncements:947449702457171989> Features", value="```Shows Features Of Bot```")
        embed.add_field(name=f"<:btannouncements:947449702457171989> Commands", value="```Shows Commands Of Bot```")
        embed.add_field(name=f"<:btannouncements:947449702457171989> Ping", value="```Shows The Latency Of Bot```")
        embed.add_field(name=f"<:btannouncements:947449702457171989> Stats", value="```Shows The Stats Of Bot```")
        embed.add_field(name=f"<:btannouncements:947449702457171989> Invite", value="```Sends A Bot Invite Link```")
       
        await ctx.reply(embed=embed, mention_author=True)

@client.command(aliases=['commands'])
async def cmds(ctx):
        embed = discord.Embed(color=00000, title="ViRTUCY SECURITY")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/938370383885762620/e5df8212c678833c4b1b6a864988b65a.webp?size=2048")
        embed.set_footer(text="Note: These Commands Can Be Used By Server Owner Only")
        embed.add_field(name="<:emoji_4:928261897814409227> cc", value="```Deletes Channels With Given Name```")
        embed.add_field(name="<:emoji_4:928261897814409227> cr", value="```Deletes Role With Given Name```")
        embed.add_field(name="<:emoji_4:928261897814409227> massunban", value="```Unbans Everyone In Banlist Of Guild```")
        embed.add_field(name="<:emoji_4:928261897814409227> whitelist", value="```Whitelistes Given User```")
        embed.add_field(name="<:emoji_4:928261897814409227> whitelisted", value="```Shows The Whitelisted Members```")
        embed.add_field(name="<:emoji_4:928261897814409227> unwhitelist", value="```Unwhitelistes Given User```")
        await ctx.reply(embed=embed, mention_author=True)

@client.command()
async def features(ctx):
        embed = discord.Embed(color=00000, title="ViRTUCY SECURITY", description='<:features:947472512185413632>**Features**\n ```Anti Ban\n Anti Kick\n Anti Prune\ Anti Channel Create\n Anti Channel Update\ Anti Channel Delete\n Anti Role Create\n Anti Role Update\ Anti Role Delete\n Anti Guild Update\n Anti Everyone/Here\n Anti Invite Delete\n Anti Invite Update\n Anti Integration Create \n Anti Integration Update\n Anti Integration Delete\n Anti Bot Add\n Anti Community Spam\ Anti Webhook Create\n Anti Webhook Update\n Anti Webhook Delete\n Anti Unban```')
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/938370383885762620/e5df8212c678833c4b1b6a864988b65a.webp?size=2048")
        embed.add_field(name="Anti Nuke Features", value="Auto Recovery = <a:load:947455949935898674> Enabled")
        embed.set_footer(text="ViRTUCY SECURITY | Prasoon :c ")
        await ctx.reply(embed=embed, mention_author=True)


@client.event
async def on_command_error(ctx, error):
        embed = discord.Embed(color=0000, title='ViRTUCY SECURITY | Error!!', description=f"***__```Error: {error}```__***")
        embed.set_footer(text="Codex :p")
        await ctx.reply(embed=embed, mention_author=True)


@client.command()
async def stats(ctx):
        embed = discord.Embed(color=000000, title="ViRTUCY SECURITY", description=f"** __GUILDS__: {len(client.guilds)}\n __USERS__: {len(set(client.get_all_members()))}**")
        embed.set_footer(text="ViRTUCY SECURITY")
        await ctx.reply(embed=embed, mention_author=True)

@client.command()
async def ping(ctx):
	await ctx.reply(f"**Latency Is `{int(round(client.latency * 1000))}` ms!**")

@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanalll(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.reply('**Unbanning {} members**'.format(len(banlist)))
    for users in banlist:
            await ctx.guild.unban(user=users.user, reason=f"By {ctx.author}")

@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["cr"])
async def roleclean(ctx, roletodelete):
    for role in ctx.message.guild.roles:
            if role.name == roletodelete:
                try:
                    await role.delete()
                except:
                  pass

@commands.cooldown(3, 300, commands.BucketType.user)
@commands.check(is_server_owner)
@client.command(aliases=["cc"])
async def channelclean(ctx, channeltodelete):
    for channel in ctx.message.guild.channels:
            if channel.name == channeltodelete:
                try:
                    await channel.delete()
                except:
                  pass

@client.event
async def on_invite_delete(invite):
        guild = invite.guild
        logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.invite_delete).flatten()
        logs = logs[0]
        if str(logs.user.id) in whitelisted[str(guild.id)]:
          pass
        else:
          reason = "ViRTUCY SECURITY | Anti Invite Delete"
          await logs.user.ban(reason=reason)


	
	
@client.event
async def on_guild_emojis_update(before, after):
	guild = before
	logs = await after.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_update).flatten()
	logs = logs[0]
	await logs.user.ban(reason=f"ViRTUCY SECURITY | Anti Emoji Update")
	
	
@client.event
async def on_guild_emojis_create(emoji):
	guild = emoji.guild
	logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.emoji_create).flatten()
	logs = logs[0]
	await logs.user.ban(reason=f"ViRTUCY SECURITY | Anti Emoji Create")



@client.event
async def on_member_remove(member):
  guild = member.guild
  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.member_prune).flatten()
  logs = logs[0]
  reason = "ViRTUCY SECURITY | Anti Prune"
  await logs.user.ban(reason=f"{reason}")





@client.event
async def on_invite_update(invite):
        guild = invite.guild
        logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.invite_update).flatten()
        logs = logs[0]
        if str(logs.user.id) in whitelisted[str(guild.id)]:
          pass
        else:
          reason = "ViRTUCY SECURITY | Anti Invite Delete"
        await logs.user.ban(reason=reason)

@client.event
async def on_guild_integrations_update(integration):
  guild = integration.guild
  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.integration_update).flatten()
  logs = logs[0]
  reason = "ViRTUCY SECURITY | Anti Integration Update"
  await logs.user.ban(reason=reason)



@client.event
async def on_guild_integrations_create(integration):
  guild = integration.guild
  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.integration_create).flatten()
  logs = logs[0]
  reason = "ViRTUCY SECURITY | Anti Integration Create"
  await logs.user.ban(reason=reason)

@client.event
async def on_guild_integrations_delete(integration):
  guild = integration.guild
  logs = await guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.integration_delete).flatten()
  logs = logs[0]
  reason = "ViRTUCY SECURITY | Anti Integration Delete"
  await logs.user.ban(reason=reason)




                            
@client.event
async def on_connect():
    play = discord.Game(
        name=f"{prefix}help | {len(client.guilds)} Guilds!")
    await client.change_presence(activity=play)


keep_alive()
client.run("OTk4ODUxMzQ2Mzk0NTEzNDMx.G1rvZS.Hf1tHKw3OJwZwOHhmjsG0eXcvwp3EoiJA74wZQ")