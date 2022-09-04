import disnake
from disnake.ext import commands
from middleware import TwitchUtil, YouTubeUtil
import urllib.parse as urlparse
import config

class uploadContent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="post-content")
    async def postContent(
        self, 
        inter: disnake.ApplicationCommandInteraction,
        url: str
    ):
        query = urlparse.urlparse(url) 
        if query.hostname == "www.twitch.tv":
            await inter.response.defer(ephemeral=True, with_message=True)
            channel = inter.guild.get_channel(config.channelIDs["communityLivestreams"])
            contentDetails, broadcasterDetails, authorDetails = TwitchUtil.getContentDetails(url)
            if contentDetails:
                if contentDetails.gameName != "none" and contentDetails.gameName.lower() != "propnight":
                    await inter.followup.send(content="Unrelated to Propnight!!")
                else:
                    embed = disnake.Embed()
                    embed.set_author(
                        name=broadcasterDetails.name,
                        url=broadcasterDetails.channelUrl,
                        icon_url=broadcasterDetails.iconUrl
                    )
                    print(contentDetails)
                    embed.set_image(url=contentDetails.thumbnail)
                    embed.title = contentDetails.title
                    embed.description = contentDetails.description
                    embed.color = disnake.Color.purple()
                    embed.url = url
                    if authorDetails:
                        embed.set_footer(text="Clipped by "+authorDetails.name, icon_url=authorDetails.iconUrl)
                    if contentDetails.type == "clip" or contentDetails.type == "video":
                        channel = inter.guild.get_channel(config.channelIDs.get("communityContent"))
                        await channel.send(embed=embed)
                    elif contentDetails.type == "livestream":
                        channel = inter.guild.get_channel(config.channelIDs.get("communityLivestreams"))
                        await channel.send(embed=embed)
                    await inter.followup.send(content="Your post has been accepted", ephemeral=True)
            else:
                await inter.followup.send(content="Unable to find content")
        elif query.hostname in ("www.youtube.com", "youtube.com", "youtu.be"):
            await inter.response.defer(ephemeral=True, with_message=True)
            contentId = YouTubeUtil.getContentId(url)
            success, contentRequestResult = YouTubeUtil.getContentDetails(contentId)
            if success:
                isPropnightRelated = False
                if contentRequestResult.tags:
                    for tag in config.youtubeWhitelistTags:
                        if tag in contentRequestResult.tags:
                            isPropnightRelated = True
                            break
                if "propnight" in contentRequestResult.title.lower() or "propnight" in contentRequestResult.description.lower():
                    isPropnightRelated=True
                if not isPropnightRelated:
                    await inter.followup.send(content="Unrelated to Propnight", ephemeral=True)
                else:
                    success, authorRequestResult = YouTubeUtil.getAuthorDetails(contentRequestResult.CID)
                    if success:
                        embed = disnake.Embed()
                        embed.set_author(
                            name=authorRequestResult.name, 
                            url=authorRequestResult.channelUrl, 
                            icon_url=authorRequestResult.iconUrl
                        )
                        embed.set_image(url=contentRequestResult.thumbnail)
                        embed.title = contentRequestResult.title
                        embed.url = url
                        embed.description = contentRequestResult.description
                        embed.color = disnake.Color.red()
                        if contentRequestResult.isLive:
                            channel = inter.guild.get_channel(config.channelIDs.get("communityLivestreams"))
                            await channel.send(embed=embed)
                        else:
                            channel = inter.guild.get_channel(config.channelIDs.get("communityContent"))
                            await channel.send(embed=embed)
                        await inter.followup.send(content="Your post has been accepted")
                    else:
                        await inter.followup.send(content=authorRequestResult)
            else:
                await inter.followup.send(content=contentRequestResult)
        else:
            await inter.send(content="Unrecognized domain!")

def setup(bot: commands.Bot):
    bot.add_cog(uploadContent(bot))