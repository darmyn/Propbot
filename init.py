import os
import bot

bot = bot.main()
bot.load_extensions("commands")
bot.run(os.environ["botToken"])