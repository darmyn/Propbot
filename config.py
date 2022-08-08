import disnake

testGuilds = [965358405252431885]
intents = disnake.Intents.default()
intents.members = True
listOfMaps = ["House", "Castle", "School", "Abbey", "Camp", "Village"]
channelIDs = {
    "1v1-chase": 968989047873749002,
    "4v1-scrim": 968989164034981888,
    "server-feedback": 976002301955309608,
    "find-teammates": 980973766534389772,
    "content-upload-requests": 1006075098870071387,
    "community-livestreams": 1006017776625909760,
    "community-content": 1006018008285720596
}
fflags = {"acceptingFeedback": True}
feedbackSettings = {
    "minimumTitleLength": 10,
    "minimumDescriptionLength": 20,
}