import discord
from discord import Interaction
from discord.ext import commands
from discord import app_commands
from json import JSONDecodeError, loads

"""
 ________________________________________________
|                                                |
|                                                |
|       Le système d'embeds de Talent Hub        |
|                                                |
|________________________________________________|
"""

# ID du rôle ayant des permissions spéciales pour créer des embeds
ID_ROLE_ADMINISTRATEUR = 0000000000000000000


class CogEmbeds(commands.Cog):
    """
    Une classe de Cog pour gérer les commandes d'embed dans un bot Discord.

    Attributes:
        bot (commands.Bot): L'instance du bot où le Cog est ajouté.
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="create_embed", description="[🛠️] Créer un embed.")
    async def creatembed(self, interaction: Interaction, embed_content: str):
        """
        Commande slash qui envoie un embed grâce au code JSON fourni.

        Args:
            interaction (Interaction): L'objet interaction de Discord.
            embed_content (str): Le contenu JSON de l'embed.

        Note:
            Le code JSON est récupéré lors de la création d'un embed
            sur le site Discohook ou l'une des alternatives.
        """
        # Vérifie que l'utilisateur qui exécute la commande a les permissions administrateur
        # ou le rôle `@Administrateur`.
        if (
            interaction.user.guild_permissions.administrator
            or interaction.user.get_role(ID_ROLE_ADMINISTRATEUR)
        ):
            try:
                # Encode le contenu pour éviter les erreurs de caractères spéciaux
                embed_content.encode("unicode_escape")
                # Charge le contenu JSON en dictionnaire Python
                embed_content = loads(embed_content)

                # Crée un objet Embed à partir du dictionnaire
                embed_json = discord.Embed.from_dict(embed_content)

                # Diffère la réponse de l'interaction pour la rendre invisible aux autres utilisateurs
                await interaction.response.defer(ephemeral=True, thinking=True)
                # Envoie un message de confirmation
                await interaction.followup.send("L'embed va être envoyé.")
                # Envoie l'embed dans le canal
                await interaction.channel.send(embed=embed_json)
            except JSONDecodeError:
                # Envoie un message d'erreur si le décodage JSON échoue
                await interaction.response.send_message(
                    "Une erreur est survenue. Assurez-vous de rentrer un code JSON valide ou contactez le support.\n`JSONDecodeError`",
                    ephemeral=True,
                )
        else:
            # Envoie un message d'erreur si l'utilisateur n'a pas les permissions nécessaires
            await interaction.response.send_message(
                "Vous n'avez pas la permission d'exécuter cette commande.",
                ephemeral=True,
            )


async def setup(bot):
    """
    Fonction pour ajouter le Cog au bot.

    Args:
        bot (commands.Bot): L'instance du bot où le Cog est ajouté.
    """
    await bot.add_cog(CogEmbeds(bot))


# Indique que le fichier a été chargé (utile pour le développement et le débogage)
print(f"{__file__} a été chargé")
