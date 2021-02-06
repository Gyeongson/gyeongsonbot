import discord
import asyncio
from discord.ext import commands
from lib import config

class CommandsEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("봇이 준비되었어요.")

        channel = self.bot.get_channel(config.terminal)
        await channel.send("```봇이 준비되었어요.```")
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('경손아 도움'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        perm = {
            "administrator": "관리자",
            "manage_guild": "서버 관리하기",
            "manage_roles": "역할 관리하기",
            "manage_permissions": "권한 관리하기",
            "manage_channels": "채널 관리하기",
            "kick_members": "멤버 추방하기",
            "ban_members": "멤버 차단하기",
            "manage_nicknames": "별명 관리하기",
            "manage_webhooks": "웹훅 관리하기",
            "manage_messages": "메시지 관리하기"
        }
        if isinstance(error, discord.NotFound):
            return

        elif isinstance(error, discord.Forbidden):
            await ctx.send(f"{ctx.author.mention} 권한 부족 이유로 명령어 실행에 실패했어요.")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("해당 명령어를 찾을 수 없어요. `경손아 도움` 으로 명령어를 확인해보세요.")

        elif isinstance(error, commands.MissingPermissions):
            mp = error.missing_perms
            p = perms[mp[0]]
            await ctx.send(f"{ctx.author.mention} 이 명령어를 실행하기 위해서는 다음과 같은 권한이 필요합니다. : `{p}`")

        elif isinstance(error, commands.BotMissingPermissions):
            mp = error.missing_perms
            p = perms[mp[0]]
            await ctx.send(f"{ctx.author.mention} 이 명령어를 실행하기 위해서는 봇에게 다음과 같은 권한이 필요합니다. : `{p}`")

        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
                await ctx.send(f"{ctx.author.mention} 해당 유저를 찾을 수 없어요, 유저를 다시 확인해주세요.")

            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f"{ctx.author.mention} 채널을 찾을 수 없었어요, 채널을 다시 확인해주세요.")

            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"{ctx.author.mention} 해당 채널을 봇이 읽거나 볼 수 없어요, 권한을 다시 확인해주세요.")

            elif isinstance(error, commands.RoleNotFound):
                await ctx.send(f"{ctx.author.mention} 역할을 찾을 수 없었어요, 역할을 다시 확인해주세요.")
            
            elif isinstance(error, commands.NotOwner):
                await ctx.send("해당 명령어는 개발자 전용 커맨드에요.")
            
            elif isinstance(error, commands.MissingRole):
                await ctx.send(f"해당 명령어는 특정 역할 전용 커맨드에요.")
            else:
                usage = ctx.command.help.split("\n")[0]
                await ctx.send(f"{ctx.author.mention} `{usage}`(이)가 올바른 명령어에요!")
        else:
            channel = self.bot.get_channel(config.errorterminal)
            await channel.send(f"```예기치 못한 오류가 발생했어요. {ctx.command.name} : {error}```")
            await ctx.send(f"{ctx.author.mention} 명령어 실행 도중 오류가 발생했어요.\n\n이 오류가 지속될 경우 Discord 지원 서버로 문의해주세요. https://discord.gg/4uwv3UVEwv")
    
def setup(bot):
    bot.add_cog(CommandsEvent(bot))