import discord 
import koreanbots
from discord.ext import commands
from lib import config

client = discord.Client()
koreanbots = koreanbots.Client(client, config.koreanbotstoken)

intents_list = discord.Intents(
    guilds=True,
    members=True,
    bans=True,
    integrations=True,
    presences=False,
    messages=True,
    reactions=True
)

bot = commands.Bot(command_prefix="경손아 ", intents=intents_list)
bot.remove_command("help")

bot.load_extension('Cogs.Events')
bot.load_extension('Cogs.General')
bot.load_extension('Cogs.Moderation')
bot.load_extension('jishaku')

bot.run(config.token)