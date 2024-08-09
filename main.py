import discord
from discord.ext import commands
from alive import keep_alive
import traceback
import json
import sys
import os


class DiscordBot(commands.Bot):
  def __init__(self, prefix, intents):
    super().__init__(
        command_prefix=prefix,
        help_command=None,
        intents=intents,
    )

  async def load_extensions(self):
    """ Load Extensions from file """
    for ext in os.listdir("./cogs"):
      try:
        if ext.endswith(".py"):
          await self.load_extension(f"cogs.{ext[:-3]}")
          print(f"Extension Loaded: {ext}")
      except:
        print(f"Load Error: {ext}\n{traceback.format_exc()}")
 
  @staticmethod
  def run_wizard():
    """ Run the wizard """
    print('------------------------------------------')
    print('Welcome To The Discord Bot Wizard!')
    print('------------------------------------------')
    store_token = input(f'Enter Your Bot Token: \n> ')
    print('------------------------------------------')
    store_prefix = input(f'Enter Your Bot Prefix: \n> ')

    data = {"token": store_token, "prefix": store_prefix}

    with open('data/config.json', 'w') as f:
      f.write(json.dumps(data, indent=4))
      print('------------------------------------------')
      print('Wizard Finished!, Please Restart Bot Again.')
      print('------------------------------------------')

  @classmethod
  def init(cls):
    """ Init Bot """   
    with open('data/config.json') as f:
      config = json.load(f)
      if config.get('token') is None or config.get('prefix') is None:
        if not os.environ.get('TOKEN'):
          cls.run_wizard()     
        else:
          my_bot = cls(prefix=os.environ.get('PREFIX'), intents=discord.Intents.all())
          my_bot.run(os.environ['TOKEN'], reconnect=True)
      else:
        token = config['token']
        my_bot = cls(prefix=config.get('prefix'), intents=discord.Intents.all())
        my_bot.run(token, reconnect=True)
  
  async def on_ready(self):
    """ Ready Event """
    print('------------------------------------------')
    print(f"Logged in as {self.user}")
    print(f"Bot ID: {self.user.id}")
    print(f"Discord Version: {discord.__version__}")
    print(f"Python Version: {sys.version}")
    print(f"Prefix: {self.prefix}")
    print('------------------------------------------')
    await self.load_extensions()
    
  @property
  def prefix(self):
    with open("./data/config.json") as f:
      config = json.load(f)
      self.config = config
      return config.get('prefix').strip('\"')
    
  def restart(self):
    """ Restart Bot """
    os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == "__main__":
  discord_bot = DiscordBot
  discord_bot.init()
  keep_alive()