from discord.ext import commands


class AdminCommands(commands.Cog):
  """
  Cog for administrative commands.
  """

  def __init__(self, bot: commands.Bot) -> None:
    """
    Initialize the AdminCommands cog.

    Args:
      bot (commands.Bot): The Discord bot instance.
    """
    self.bot = bot

  @commands.command()
  async def sync(self, ctx: commands.Context) -> None:
    """
    Synchronize the command tree for slash commands.

    This command can only be used by users in the ADMIN_LIST.

    Args:
      ctx (commands.Context): The invocation context.
    """

    await self.bot.tree.sync()
    await ctx.reply("Command Tree is synced, slash commands are updated ✔️")


async def setup(bot: commands.Bot) -> None:
  """
  Setup function to add the AdminCommands cog to the bot.

  Args:
    bot (commands.Bot): The Discord bot instance.
  """
  await bot.add_cog(AdminCommands(bot))
