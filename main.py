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

bot.run(config.token)