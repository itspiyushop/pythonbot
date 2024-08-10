from discord.ext import commands
import discord 
import json


class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
      name="setprefix",
      description="Change the bot's prefix",
      alises=["chnage-prefix"],
      usage= "setprefix [prefix]"
    )
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix):

      if len(prefix) > 1:
        embed = discord.Embed(
          description="> `❌` | Prefix must be only one letter!",
          color=discord.Color.red(),
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        
        return await ctx.send(embed=embed, delete_after=10)
        
      else:
        try:
            with open("data/config.json", "r") as f:
                data = json.load(f)
                data["prefix"] = prefix
                self.bot.command_prefix = prefix
                with open("data/config.json", "w") as f:
                    json.dump(data, f, indent=4)
                    embed = discord.Embed()
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    embed.description = f"> `✅` | Bot Prefix Has Changed To `{prefix}`"
                    embed.color = discord.Color.green()
                    await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
              description=f"> `❌` | An Error Occurred: {e}",
              color=discord.Color.red()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed, delete_after=10)

    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
              description="> `❌` | You don't have permission to use this command!",
              color=discord.Color.red()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed, delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
              description="> `❌` | Please provide a prefix!",
              color=discord.Color.red()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed, delete_after=10)
        else:
            embed = discord.Embed(
              description=f"> `❌` | An Error Occurred: {error}",
              color=discord.Color.red()
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed, delete_after=10)


async def setup(bot):
    await bot.add_cog(Config(bot))