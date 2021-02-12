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
            await ctx.send(f"봇이 권한이 부족해요.\n\nDM 등 개인에게 전송해야 하는 커맨드를 사용하신 경우 DM 차단 여부를 확인해주세요.")

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("알 수 없는 커맨드 에요, `경손아 도움` 에서 찾아보세요.")

        elif isinstance(error, commands.MissingPermissions):
            missingpermission = error.missing_perms
            permission_korean = perms[missingpermission[0]]
            await ctx.send(f"이 명령어를 실행하기 위해서는 다음 권한이 필요해요. : `{permission_korean}`")

        elif isinstance(error, commands.BotMissingPermissions):
            missingpermission = error.missing_perms
            permission_korean = perms[missingpermission[0]]
            await ctx.send(f"이 명령어를 실행하기 위해서 봇에게 다음 권한이 필요해요. : `{permission_korean}`")

        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):
                await ctx.send(f"알 수 없는 유저에요.")

            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f"알 수 없는 채널이에요.")

            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"채널을 봇이 읽거나 볼 수 없어요.")
            else:
                usage = ctx.command.help.split("\n")[0]
                await ctx.send(f"`{usage}` 가 올바른 사용방법 이에요.")   
        
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("알 수 없는 커맨드에요, `경손아 도움` 으로 확인해보세요.")
        elif isinstance(error, commands.CommandNotFound) or isinstance(error, commands.MissingRole) or isinstance(error, commands.NotOwner) or isinstance(error, commands.CheckFailure):
            await ctx.send("이 커맨드는 귀하의 권한으로 사용할 수 없어요.")
        else:
            channel = self.bot.get_channel(config.errorterminal)
            await channel.send(f"```예기치 못한 오류가 발생했어요.\n\n오류가 발생한 명령어: {ctx.command.name}\n오류: {error}```")
            embed = discord.Embed(title="예기치 못한 오류가 발생했어요.", description="명령어를 실행하던중 오류가 발생해 사용이 취소되었어요.\n\n[이곳](https://discord.gg/4uwv3UVEwv) 에서 도움을 요청할 수 있어요.", color=0x428bff)
            await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(CommandsEvent(bot))