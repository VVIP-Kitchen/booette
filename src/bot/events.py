import discord
from discord.ext import commands
from utils.logger import logger

class BotEvents(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self) -> None:
    logger.info(f"{self.bot.user} has connected to Discord!")

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message) -> None:
    print(message)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(BotEvents(bot))
