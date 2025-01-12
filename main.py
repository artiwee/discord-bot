from pathlib import Path

import discord
from discord.ext import commands

from environement import settings
from infrastructure.services.cog_loader import CogLoader
from infrastructure.services.logger_service import LoggerService


class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

        logger_service = LoggerService()
        self.logger = logger_service.get_logger(
            name="bot", log_file=Path("logs/bot.log")
        )
        self.cog_loader = CogLoader(self)

    async def setup_hook(self) -> None:
        summary = await self.cog_loader.load_all_cogs()

        if summary.failed:
            failed_cogs = [name for name, _ in summary.failed]
            self.logger.warning(
                f"⚠️ Certains cogs n'ont pas pu être chargés: {', '.join(failed_cogs)}"
            )

    async def on_ready(self):
        await bot.wait_until_ready()

        await bot.tree.sync()
        print(f"{bot.user} à correctement été connecté")


bot = Bot()


@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    print("Les commandes ont été chargées.")


@bot.command()
async def load(ctx, name=None):
    if name:
        await bot.load_extension(name)
        await bot.tree.sync()
        print(f"{name} a été load")
        print("Les commandes ont été chargées")
    else:
        print("Vous n'avez pas renseigné le cog à load.")


@bot.command()
async def unload(ctx, name=None):
    if name:
        await bot.unload_extension(name)
        await bot.tree.sync()
        print(f"{name} a été unload")
        print("Les commandes ont été retirées")
    else:
        print("Vous n'avez pas renseigné le cog à unload.")


@bot.command()
async def reload(ctx, name=None):
    if name:
        await bot.reload_extension(name)
        await bot.tree.sync()
        print(f"{name} a été reload")
        print("Les commandes ont été chargées")
    else:
        print("Vous n'avez pas renseigné le cog à reload.")


if __name__ == "__main__":
    bot = Bot()
    bot.run(settings.DISCORD_TOKEN)
