import disnake
from disnake.ext import commands

@commands.slash_command(name="verify-content")
def verifyContent(
    inter: disnake.CommandInter,
    link: str
):
    print(link)
