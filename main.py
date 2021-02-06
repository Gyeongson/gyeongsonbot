import discord 
import koreanbots
from discord.ext import commands
from lib import config

client = discord.Client()
koreanbots = koreanbots.Client(client, config.koreanbotstoken)

intents = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    emojis=True,
    integrations=True,
    invites=True,
    presences=False,
    messages=True,
    reactions=True, 
    typing=True
)

bot = commands.Bot(command_prefix="경손아 ", intents=intents)
bot.remove_command("help")

bot.load_extension('Cogs.Events')
bot.load_extension('Cogs.General')
bot.load_extension('Cogs.Moderation')

@bot.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.private:
        return

    if message.author.bot:
        return

    if message.content.startswith("경손아 "):
        if "'" in message.content or '"' in message.content or "\\" in message.content or ";" in message.content:
            channel = bot.get_channel(config.terminal)
            await channel.send(f"```Command Denied : {message.author} ( {message.author.id} ) - {message.content} / Guild : {message.guild.name} ( {message.guild.id} )```")
            await message.channel.send(f"{message.author.mention} 특수문자를 제외하고 다시 시도해주세요.")
        else:
            channel = bot.get_channel(config.terminal)
            await channel.send(f"```Command Processed : {message.author} ( {message.author.id} ) - {message.content} / Guild : {message.guild.name} ( {message.guild.id} )```")
            await bot.process_commands(message)

bot.run(config.token)