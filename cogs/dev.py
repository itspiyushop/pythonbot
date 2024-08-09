from discord.ext import commands
from data.config import dev_id
import inspect

class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # View Command File Command
    @commands.command(
      name="source",
      description="Shows the source code of the command",
      usage="source [command-name]",
      aliases=["src"]
    )
    async def source(self, ctx, command_name: str):    
        dev = await self.bot.fetch_user(dev_id)
        if ctx.author.id != dev.id:
            return await ctx.send("❌ | You are not the developer of this bot!", delete_after=10)
        else:
            name = str(command_name).lower()
            if name == "source" or name == "help":
                return await ctx.send("❌ | You can't get the source code of that command!", delete_after=10)
              
            a = "`" * 3
            src = inspect.getsource(self.bot.get_command(name).callback)
            await ctx.send(f"{a}py\n{src}\n{a}" , delete_after=30)
      
    # View Command File Error Handle
    @source.error
    async def source_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ | That command doesn't exist!", delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ | Please provide a command name!", delete_after=10)
        else:
            await ctx.send(f"❌ | An error occurred", delete_after=10)
            print(error)


async def setup(bot):
    await bot.add_cog(DevCommands(bot))