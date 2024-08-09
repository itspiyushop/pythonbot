from discord.ext import commands
from data.config import dev_id
import discord
import time 

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Ping Command
    @commands.command(
        name="ping",
        description="Check the bot's latency",
        aliases=["latency", "pong"],
        usage="ping"
    )
    async def ping(self, ctx):
        start_time = time.time()
        m = await ctx.send("🏓 Pong!")  
        latency = (time.time() - start_time) * 1000
        await m.edit(content=f"🏓 WS: {round(self.bot.latency * 1000)}ms  |  API: {round(latency)}ms")

    # Help Command
    @commands.command(
        name="help",
        description="Shows all the commands of the bot",
        aliases=["h"],
        usage="help [command-name]"
    )
    async def help(self, ctx, command_name=None):
        
        if command_name is None:
            all_commands = ", ".join([command.name for command in self.get_commands()])
            format = (
                f"```md\n# {self.bot.user.name} - Commands List\n```"
                f"```md\n{all_commands}\n```"
                f"```md\n> Use {self.bot.prefix}help [command-name] For More Information\n```")
            
            await ctx.send(format, delete_after=30)
            
        elif command_name == self.bot.get_command(str(command_name).lower()).name:
            cmd_name = str(command_name).lower()
            command = self.bot.get_command(cmd_name)
            format = (
                f"```md\n< {self.bot.prefix}{command.usage} >\n```"
                f"```md\n# Aliases\n{', '.join(command.aliases) or None}\n"
                f"# Description\n{command.description}\n```"
                "```md\n> Remove brackets when typing commands\n"
                "> [] = optional arguments\n> {} = optional user input\n```")
            await ctx.send(format, delete_after=30)
            
    # Help Command Error Handle
    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("❌ | That command doesn't exist!")


    # Dev Info Command
    @commands.command(
        name="developer",
        description="Shows the developer info",
        aliases=["dev", "devinfo"],
        usage="developer"
    )
    async def developer(self, ctx):
        dev = await self.bot.fetch_user(dev_id)
        embed = discord.Embed(
            title="Developer Information",
            description="Here is some information about the developer of this bot",
            color=discord.Color.default()
        )
        embed.set_thumbnail(url=dev.avatar.url)
        embed.add_field(name="Display Name", value=dev.display_name)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.add_field(name="Username", value=dev.name)
        embed.add_field(name="Mention", value=dev.mention)
        embed.add_field(name="ID", value=dev.id)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Profile Link", value=f"[Click Here](https://discord.com/users/{dev.id})")

        await ctx.send(embed=embed, delete_after=30)


async def setup(bot):
    await bot.add_cog(Info(bot))