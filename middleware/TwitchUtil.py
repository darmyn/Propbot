import twitch
import urllib.parse as urlparse
from dataclasses import dataclass

helix = twitch.Helix("x5ynyr26slxo1q7q9qbhm9bm9gu5yq", "xgqby2nhq6xbdlmkq6x5mt2f8153c1")
#print(helix.api.get("clips", "id=NiceObliqueDunlinPMSTwin-10BlHzegpA-LReOg"))
                                        #author/mediaTypei/d
#clip https://www.twitch.tv/penta/clip/NiceObliqueDunlinPMSTwin-10BlHzegpA-LReOg
#highlight https://www.twitch.tv/videos/1575283069
#livestream https://www.twitch.tv/d4rmyn
#vod https://www.twitch.tv/videos/1575283069 

@dataclass
class contentDetails:
    type: str
    title: str
    description: str
    thumbnail: str
    gameName: str

@dataclass
class authorDetails:
    name: str
    iconUrl: str
    channelUrl: str

def getContentDetails(twitchUrl: str):
    query = urlparse.urlparse(twitchUrl)
    splitQueryPath = query.path.split("/")
    if query.path.startswith("/videos/"):
        videoId = query.path[8:]
        try:
            video = helix.video(videoId)
            return contentDetails(type="video",
                title=video.title,
                description=video.description,
                thumbnail=video.thumbnail_url,
                gameName="none",
            ), authorDetails(
                name=video.user.display_name,
                iconUrl=video.user.profile_image_url,
                channelUrl="https://www.twitch.tv/"+video.user.display_name,
            ), False
        except:
            print("error")
    elif len(splitQueryPath) > 2 and splitQueryPath[2] == "clip":
        clipId = splitQueryPath[3]
        clip: list = helix.api.get("clips", "id="+clipId).get("data")
        if len(clip) > 0:
            clipData = clip[0]
            broadcasterId = clipData.get("broadcaster_id")
            broadcaster = helix.api.get("users", "id="+broadcasterId)
            broadcasterData = broadcaster.get("data")[0]
            authorId = clipData.get("creator_id")
            author = helix.api.get("users", "id="+ authorId)
            authorData = author.get("data")[0]
            return contentDetails(
                type="clip",
                title=clipData.get("title"),
                thumbnail=clipData.get("thumbnail_url"),
                description="",
                gameName=helix.api.get("games", "id="+clipData.get("game_id")).get("data")[0].get("name")
            ), authorDetails(
                name=clipData.get("broadcaster_name"),
                iconUrl=broadcasterData.get("profile_image_url"),
                channelUrl="https://www.twitch.tv/"+broadcasterData.get("display_name")
            ), authorDetails(
                name=clipData.get("creator_name"),
                iconUrl=authorData.get("profile_image_url"),
                channelUrl="https://www.twitch.tv/"+authorData.get("display_name")
            )
    elif len(splitQueryPath) == 2 and splitQueryPath[0] == "":
        broadcasterName = splitQueryPath[1]
        broadcast = helix.api.get("streams", "user_login="+broadcasterName).get('data')
        if broadcast:
            broadcastDetails = broadcast[0]
            print(broadcastDetails)
            caster = helix.api.get("users", "id="+broadcastDetails.get("user_id"))
            casterDetails = caster.get("data")[0]
            return contentDetails(
               type="livestream",
               title=broadcastDetails.get("title"),
               thumbnail=broadcastDetails.get("thumbnail_url"),
               description="",
               gameName = helix.api.get("games", "id="+broadcastDetails.get("game_id")).get("data")[0].get("name")
            ), authorDetails(
               name=casterDetails.get("display_name"),
               iconUrl=casterDetails.get("profile_image_url"),
               channelUrl="https://www.twitch.tv/"+casterDetails.get("display_name")
            ), False
    return False, False, False