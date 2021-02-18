import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
from lib import config

class GeneralCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="도움")
    async def help(self, ctx):
        """
        경손아 도움


        명령어를 확인해보세요.
        """
        
        embed = discord.Embed(title="봇 도움말을 제공해드릴게요!", description="< > 는 필수를, [ ] 는 선택을 의미합니다.\n사용시 < > 와 [ ] 특수문자는 제거해주세요.\n모든 커맨드 앞에는 `경손아` 가 필요합니다.", color=0x428bff)
        for command in self.bot.commands:
            dev = ["Jishaku"]
            if command.cog.qualified_name in dev:
                pass
            else:
                command1 = command.help.split("\n")[3:]
                command2 = ""
                for arg in command1:
                    command2 += f"{arg}\n"
                embed.add_field(name=command.help.split("\n")[0], value=command2, inline=False)
        try:
            await ctx.author.send(embed=embed)
        except:
            await ctx.send("도움말을 DM 으로 전송하는것에 실패했어요, DM 이 열려있는지 확인해주세요.")
        else:
            await ctx.message.add_reaction("✅")

    @commands.command(name="핑")
    async def ping(self, ctx):
        """
        경손아 핑


        봇의 핑을 확인해보세요.
        """
        await ctx.send(f"현재 핑은, {round(self.bot.latency * 1000)}ms 에요.")

    @commands.command(name="한강")
    async def hangangriver(self, ctx):
        """
        경손아 한강

        
        현재 한강물 온도를 확인해보실 수 있어요.
        """
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://hangang.dkserver.wo.tc/") as response:
                data = await response.json(content_type=None)
                embed = discord.Embed(description=f"현재 한강물의 온도는 `{data['temp']}도` 입니다.", color=0x428bff)
                embed.set_footer(text=f"측정: {data['time']}")
                await ctx.send(embed=embed)
    
    @commands.command(name="아바타")
    async def profile(self, ctx, *, user: discord.User = None):
        """
        경손아 아바타 < 유저 >


        < 유저 또는 명령어 사용자 > 의 프로필을 업로드합니다.
        """
 
        if user is None:
            user = ctx.author

        embed = discord.Embed(title=f"{user} 님의 프로필이에요.", color=0x428bff)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text="기본 프로필일 경우 사진이 나오지 않아요.")
        await ctx.send(embed=embed)
    
    @commands.command(name="랜덤")
    async def random(self, ctx, *args):
        """
        경손아 랜덤 < 선택지1 > < 선택지2 > < 선택지3 > ...


        선택지중 랜덤으로 선택합니다, 띄어쓰기를 기준으로 판단합니다.
        """

        if not args or len(args) <= 1:
            await ctx.send(f"`경손아 랜덤 < 선택지1 > < 선택지2 > < 선택지3 > ...` 가 올바른 사용방법 이에요.")
        else:
            randomsl = random.choice(args)
            await ctx.send(f"{ctx.author.name} 님의 선택은 `{randomsl}` 에요!")
    
def setup(bot):
    bot.add_cog(GeneralCommand(bot))    