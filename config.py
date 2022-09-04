import disnake

twitchClientId = "x5ynyr26slxo1q7q9qbhm9bm9gu5yq"
testGuilds = [965358405252431885]
intents = disnake.Intents.default()
intents.members = True
channelIDs = {
    "1v1-chase": 968989047873749002,
    "3v1-scrim": 968989164034981888,
    "server-feedback": 976002301955309608,
    "find-teammates": 980973766534389772,
    "contentUploadRequests": 1006075098870071387,
    "communityLivestreams": 1013695463834275902,
    "communityContent": 1013695463834275902
}
youtubeWhitelistTags = ["propnight"]