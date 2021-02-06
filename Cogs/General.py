import discord
from discord.ext import commands
import asyncio
import aiohttp
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
            await ctx.send(" - ")
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
        
    @commands.command(name="번역")
    async def translate(self, ctx, *, arg):
        """
        경손아 번역 < 문장 또는 단어 >

        
        < 문장 또는 단어 > 를 영어로 자동번역합니다. 현재는 한국어만 지원됩니다.
        """
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.winsub.kr/kakao/?key={config.winsubapi}&target=kr&input={arg}") as response:
                data = await response.json(content_type=None)
                embed = discord.Embed(title="카카오 번역기를 통해 번역한 결과에요!", color=0x428bff)
                embed.add_field(name="번역문장", value=f"```{arg}```", inline=False)
                embed.add_field(name="번역결과", value=f"```{data['result']['output']}```", inline=False)
                embed.set_footer(text="번역 시스템은 https://api.winsub.kr/ 를 이용하였습니다.")
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

def setup(bot):
    bot.add_cog(GeneralCommand(bot))    