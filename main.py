import discord
from discord.ext import commands

from environement import settings


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            name="Talent Hub BOT",
            command_prefix="!",
            description="Bot Discord officiel de Talent Hub",
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.embedscreation")

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
