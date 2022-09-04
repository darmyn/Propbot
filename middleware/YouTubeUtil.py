
from dataclasses import dataclass
from googleapiclient.discovery import build
import os
import urllib.parse as urlparse

youtube = build("youtube", "v3", developerKey=os.environ["youtubeAPIToken"])

@dataclass
class authorDetails:
    name: str
    iconUrl: str
    channelUrl: str

thumbnailHierarchy = ["maxres", "standard", "high", "medium", "default"]
def getBestThumbnail(thumbnails):
    print("ATTEMPTING TO GET BEST THUMBNAIL")
    print("HERE ARE THE THUMBNAILS")
    for thumbnailType in thumbnailHierarchy:
        print(thumbnailType)
        thumbnailData = thumbnails.get(thumbnailType)
        if thumbnailData:
            return thumbnailData.get("url")

def getAuthorDetails(channelId: str):
    request = youtube.channels().list(
        part="snippet",
        id=channelId
    )
    response = request.execute()
    error = response.get("error")
    if error:
        return False, error.message
    items = response.get("items")
    if items and len(items) > 0:
        snippet = items[0].get("snippet")
        authorName = snippet.get("title")
        authorIconUrl = getBestThumbnail(snippet.get("thumbnails"))
        result = authorDetails(
            name = authorName,
            iconUrl = authorIconUrl,
            channelUrl = "https://www.youtube.com/channel/" + items[0].get("id")
        )
        return True, result

@dataclass
class contentDetails:
    CID: str
    isLive: bool
    tags: list[str]
    title: str
    description: str
    thumbnail: str

def getContentDetails(contentId: str):
    request = youtube.videos().list(
        part="snippet",
        id=contentId
    )
    response = request.execute()
    error = response.get('error')
    print("HERE")
    print(response)
    if error:
        return False, error.message
    items = response.get("items")
    if items and len(items) > 0:
        snippet = items[0].get("snippet")
        isLivestream = False
        if snippet.get("liveBroadcastContent") == "live":
            isLivestream = True
        result = contentDetails(
            CID = snippet.get("channelId"),
            isLive = isLivestream,
            tags = snippet.get("tags"),
            title = snippet.get("title"),
            description = snippet.get("description"),
            thumbnail = getBestThumbnail(snippet.get("thumbnails"))
        )

        return True, result
    else:
        return False, "Could not find content"

def getContentId(youtubeLink: str):
    query = urlparse.urlparse(youtubeLink)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.path == '/watch':
        p = urlparse.parse_qs(query.query)
        return p['v'][0]
    if query.path[:7] == '/embed/':
        return query.path.split('/')[2]
    if query.path[:3] == '/v/':
        return query.path.split('/')[2]
    if query.path[:7] == "/shorts":
        return query.path.split("/")[2]
    return None
