from bot.bot import DiscordBot
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")


def main() -> None:
  """
  Main entry point for the Discord bot.
  Initializes and runs the DiscordBot instance.
  """
  bot = DiscordBot()
  bot.run()


if __name__ == "__main__":
  main()
