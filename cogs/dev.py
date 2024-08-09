from discord.ext import commands
from data.config import dev_id
import discord
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
            await ctx.send(f"{a}py\n{src}\n{a}", delete_after=30)
      
    # View Command File Error Handle
    @source.error
    async def source_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ | That command doesn't exist!", delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ | Please provide a command name!", delete_after=10)
        else:
            await ctx.send(f"❌ | An error occurred", delete_after=10)
            
            
    # Activity Change Command
    @commands.command(
        name="activity",
        description="Change the bot's activity",
        usage="activity [activity-type] [activity-text]",
        aliases=["act"]
    )
    async def activity(self, ctx, activity_type: str, *, activity_text: str):
        dev = await self.bot.fetch_user(dev_id)

        if ctx.author.id != dev.id:
            await ctx.send("❌ | You are not the developer of this bot!", delete_after=10)
            return

        valid_types = {"playing", "listening", "watching", "streaming"}
        activity_type = activity_type.lower()
        if activity_type not in valid_types:
            await ctx.send("❌ | Invalid activity type. Valid options are: " + ", ".join(valid_types), delete_after=10)
            return

        try:
            activity_type = getattr(discord.ActivityType, activity_type)
        except AttributeError:

            await ctx.send("❌ | An unexpected error occurred while setting the activity type.", delete_after=10)
            return

        try:
            await self.bot.change_presence(activity=discord.Activity(type=activity_type, name=activity_text))
            await ctx.send(f"> ✅ | Successfully changed the bot's activity to `{activity_type.name}` `{activity_text}`!", delete_after=10)
        except discord.HTTPException as e:
            await ctx.send(f"❌ | An error occurred while setting the activity: {e}", delete_after=10)

    # Activity Change Error Handle
    @activity.error
    async def activity_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ | Please provide the activity type and text.", delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ | Invalid activity type. Valid options are: " + ", ".join(valid_types), delete_after=10)
        else:
            await ctx.send(f"❌ | An error occurred while changing the activity: {error}", delete_after=10)


    # Change Bot Status Command
    @commands.command(
        name="status",
        description="Change the bot's status",
        usage="status [status-type]",
        aliases=["st"]
    )
    async def status(self, ctx, status_type: str):
        dev = await self.bot.fetch_user(dev_id)

        if ctx.author.id != dev.id:
            await ctx.send("❌ | You are not the developer of this bot!", delete_after=10)
            return

        valid_types = {"online", "idle", "dnd", "invisible"}
        status_type = status_type.lower()
        if status_type not in valid_types:
            ex = ", ".join(valid_types)
            await ctx.send(f"❌ | Invalid status type. Valid options are: `{ex}`", delete_after=10)
            return
        try:
            status_type = getattr(discord.Status, status_type)
        except AttributeError:
            await ctx.send("❌ | An unexpected error occurred while setting the status type.", delete_after=10)
            return
        try:
            await self.bot.change_presence(status=status_type)
            await ctx.send(f"> ✅ | Successfully changed the bot's status to `{status_type.name}`!", delete_after=10)
        except discord.HTTPException as e:
            await ctx.send(f"❌ | An error occurred while setting the status: {e}", delete_after=10)


    # Change Bot Status Error Handle
    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ | Please provide the status type.", delete_after=10)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ | Invalid status type. Valid options are: " + ", ".join(valid_types), delete_after=10)
        else:
            await ctx.send(f"❌ | An error occurred while changing the status: {error}", delete_after=10)


            
        
async def setup(bot):
    await bot.add_cog(DevCommands(bot))