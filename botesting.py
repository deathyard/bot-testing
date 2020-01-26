import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix = '&')

@client.event
async def on_ready():
	print('Bot is ready')

@client.command()
async def test(abc):
	await abc.send(f'**Fucntioning Properly...\nBot Ping is = {round(client.latency*1000)}ms**')

@client.command(aliases=['8ball', '8'])
async def _8ball(ctx, *, question):
      responses = ['It is certain.',
                  "It is decidedly so.",
                  "Without a doubt.",
                  "Yes - definitely.",
                  "You may rely on it.",
                  "As I see it, yes.",
                  "Most likely.",
                  "Outlook good.",
                  "Yes.",
                  "Signs point to yes.",
                  "Reply hazy, try again.",
                  "Ask again later.",
                  "Better not tell you now.",
                  "Cannot predict now.",
                  "Concentrate and ask again.",
                  "Don't count on it.",
                  "My reply is no.",
                  "My sources say no.",
                  "Outlook not so good.",
                  "Very doubtful."]
                        
      await ctx.send(f'**Question : {question}\nAnswer : {random.choice(responses)}**')

@client.command()
async def clear(cmd, amount=10):
      await cmd.channel.purge(limit=amount)

@client.command()
async def kick(cmd, member : discord.Member, *, reason = None):
      await member.kick(reason=reason)
      await cmd.send(f'Gave nikal laude to {member.mention}')

@client.command()
async def ban(cmd, member : discord.Member, *, reason = None):
      await member.ban(reason=reason)
      await cmd.send(f'Gave nikal laude to {member.mention}')

@client.command()
async def unban(cmd,member):
      banned_users = await cmd.guild.bans()
      mname,mtag = member.split('#')

      for eachban in banned_users:
            user = eachban.user

            if(user.name,user.discriminator) == (mname,mtag):
                  await cmd.guild.unban(user)
                  await cmd.send(f'Unbanned {user.mention}')
                  return

client.run('NjU2OTI3MDU0MTI1ODU4ODM2.Xfp0og.nYWB_S5pQhswE9Xg0VVChhMtCZk')