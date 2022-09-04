import os
import bot

os.environ["botToken"] = "OTY5MDEzODc0NTc1NjcxMjk4.GKyGX1.JE9e7IW8Ph1szFLtROgvWNT_HRRRzeJgee3bRw"
os.environ["steamAPIToken"] = "A575C8CB6C50F26CDBEBA4CF3E49AC05"
os.environ["youtubeAPIToken"] = "AIzaSyAjANOFUMGRg5AqfUsv2Y9nLBbjUKZ0wRo"
os.environ["twitchAPIToken"] = "xgqby2nhq6xbdlmkq6x5mt2f8153c1"

bot = bot.main()
bot.load_extensions("commands")
bot.run(os.environ["botToken"])