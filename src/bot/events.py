import discord
from discord.ext import commands
from utils.logger import logger
from utils.llm import generate_response

class BotEvents(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self) -> None:
    logger.info(f"{self.bot.user} has connected to Discord!")

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message) -> None:
    #Log the message, print also works but we have logger module
    print(message)
    if message.author.bot and message.mention_everyone:
        return

    if self.bot.user.mentioned_in(message):
        reply = await generate_response(message.content)
        await message.channel.send(f"{message.author.mention} {reply}")

    await self.bot.process_commands(message)

    # Check if the author of the message is a bot, if yes return, unless you want boo to interact with booette
    # Then make the check so that, it doesn't respond to itself, but yeah can lead to a feedback loop between boo and booette.

    # Prep the contents of the message to be prompt compliant for the llm.

    # Based on server load the system prompt, this corresponds server_lore, or maybe for now hardcode if you plan to only have it in VVIP server.

    # OPTIONAL: reset chat check, could be a slash command too.

    # OPTIONAL: Image processing

    # Set up the actual query to send to the llm api, and then call the llm api.

    # OPTIONAL: Process the llm api output

    # Pass the message back to the chat, preferrably as a reply.

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(BotEvents(bot))
