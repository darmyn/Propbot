from disnake.ext import commands
import config

class main(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=config.intents,
            help_command=None,  # type: ignore
            sync_commands_debug=True,
            sync_permissions=True,
            test_guilds=config.testGuilds,
            strict_localization=True,
        )

    async def on_ready(self):
        print(f"\n"
              f"The bot is ready.\n"
              f"User: {self.user}\n"
              f"ID: {self.user.id}\n")
