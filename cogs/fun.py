from discord.ext import commands
from datetime import timedelta
import discord

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # STFU Command 
    @commands.command(
      name="stfu",
      description="To shut the user's mouth",
      aliases=["shutup", "shut", "chup"],
    )
    @commands.bot_has_permissions(moderate_members=True)
    async def stfu(self, ctx, user: discord.Member):
        if not ctx.guild:
          return 
       
        duration = timedelta(seconds=10)
        await user.timeout(discord.utils.utcnow() + duration, reason=f"Command Executed by {ctx.author.name}")
        await ctx.send(f"> 🔇 | `{user}` has been shut up for 10 second's!", delete_after=20)
          
    # STFU Command Error Handle
    @stfu.error
    async def stfu_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ | Please mention a user to shut up!", delete_after=10)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ | I don't have permission to do that!", delete_after=10)
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("❌ | I can't timeout that user!", delete_after=10)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ | I can't find that user!" , delete_after=10)
        else:
            await ctx.send(f"❌ | An error occurred", delete_after=10)
            print(error)


async def setup(bot):
    await bot.add_cog(Fun(bot))