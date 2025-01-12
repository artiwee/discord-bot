from discord import Interaction, app_commands
from discord.ext import commands

"""
 ________________________________________________
|                                                |
|                                                |
|     Le système de modération de Talent Hub     |
|                                                |
|________________________________________________|

"""


class CogModeration(commands.Cog):
    """
    Une classe de Cog pour gérer les commandes de modération dans un bot Discord.

    Attributes:
        bot (commands.Bot): L'instance du bot où le Cog est ajouté.
    """

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="clear", description="[🛠️] Supprimer des messages.")
    async def clear(
        self,
        interaction: Interaction,
        number: app_commands.Range[int, None, 100],
    ):
        """
        Commande slash pour supprimer un certain nombre de messages.

        Args:
            interaction (Interaction): L'objet interaction de Discord.
            number (int): Le nombre de messages à supprimer (entre 1 et 100).
        """
        # Vérifie si l'utilisateur a la permission de gérer les messages.
        if interaction.user.guild_permissions.manage_messages:
            await interaction.response.defer(
                ephemeral=True, thinking=True
            )  # Diffère la réponse de l'interaction.
            await interaction.followup.send(
                f"Les {number} messages vont être supprimés."
            )
            await interaction.channel.purge(limit=number)
        else:
            # Envoie un message d'erreur si l'utilisateur n'a pas les permissions nécessaires.
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
    await bot.add_cog(CogModeration(bot))


# Indique que le fichier a été chargé (utile pour le développement et le débogage).
print(f"{__file__} a été chargé")
