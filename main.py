import discord
import asyncpg
from discord.ext import commands

TOKEN_BOT = ""
DATABASE_URL = "postgresql://"


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            name="Talent Hub BOT",
            command_prefix="!",
            description="Bot Discord officiel de Talent Hub",
            intents=discord.Intents.all(),
        )

    async def reset_database(self):
        db = await asyncpg.connect(DATABASE_URL)
        tables = [
            "",
        ]
        for table in tables:
            try:
                await db.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            except:
                pass
        await db.close()

    async def setup_hook(self):
        # await self.reset_database()

        # Connexion et création des tables dans les bases de données nécessaires
        db = await asyncpg.connect(DATABASE_URL)
        await db.execute(
            """CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY NOT NULL,
            is_blocked BOOLEAN DEFAULT FALSE)"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS guilds (
            guild_id BIGINT PRIMARY KEY NOT NULL,
            is_levelsys_on BOOLEAN NOT NULL DEFAULT TRUE,
            is_blocked BOOLEAN DEFAULT FALSE)"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS members (
            guild_id BIGINT NOT NULL,
            user_id BIGINT NOT NULL,
            PRIMARY KEY (guild_id, user_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE RESTRICT ON DELETE RESTRICT,
            FOREIGN KEY (guild_id) REFERENCES guilds (guild_id) ON UPDATE RESTRICT ON DELETE RESTRICT)"""
        )

        await db.close()

        # Chargement des Cogs et des Views
        await bot.load_extension("cogs.moderation")
        await bot.load_extension("cogs.embedscreation")

    async def on_ready(self):
        await bot.wait_until_ready()

        await bot.tree.sync()  # Synchronisation des commandes slash au démarrage
        print(f"{bot.user} à correctement été connecté")


bot = Bot()


@bot.command()  # Commande pour synchroniser les commandes slash (doit être exécutée par Micha)
async def sync(ctx):
    if ctx.author.id == 1191481981226201141 or ctx.author.id == 938332094151655434:
        await bot.tree.sync()
        print("Les commandes ont été chargées.")
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")


@bot.command()  # Commande pour charger un cog (doit être exécutée par Micha)
async def load(ctx, name=None):
    if ctx.author.id == 1191481981226201141 or ctx.author.id == 938332094151655434:
        if name:
            await bot.load_extension(name)
            await bot.tree.sync()
            print(f"{name} a été load")
            print("Les commandes ont été chargées")
        else:
            print("Vous n'avez pas renseigné le cog à load.")
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")


@bot.command()  # Commande pour décharger un cog (doit être exécutée par Micha)
async def unload(ctx, name=None):
    if ctx.author.id == 1191481981226201141 or ctx.author.id == 938332094151655434:
        if name:
            await bot.unload_extension(name)
            await bot.tree.sync()
            print(f"{name} a été unload")
            print("Les commandes ont été retirées")
        else:
            print("Vous n'avez pas renseigné le cog à unload.")
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")


@bot.command()  # Commande pour recharger un cog (doit être exécutée par Micha)
async def reload(ctx, name=None):
    if ctx.author.id == 1191481981226201141 or ctx.author.id == 938332094151655434:
        if name:
            await bot.reload_extension(name)
            await bot.tree.sync()
            print(f"{name} a été reload")
            print("Les commandes ont été chargées")
        else:
            print("Vous n'avez pas renseigné le cog à reload.")
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")


# bot.run(TOKEN_BOT)  # Lancement du bot avec le token
bot.run(TOKEN_BOT)
