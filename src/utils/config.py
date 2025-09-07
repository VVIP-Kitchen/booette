import os
import sys
from utils.logger import logger
from dotenv import load_dotenv

PREFIX = "!@"
load_dotenv()

### Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-4-maverick")

for var_name in [
  "DISCORD_TOKEN",
]:
  if not globals()[var_name]:
    logger.error(f"{var_name} environment variable is not set.")
    sys.exit(1)
