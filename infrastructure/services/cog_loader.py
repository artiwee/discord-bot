from typing import List, Tuple, Optional
import logging
from dataclasses import dataclass
from pathlib import Path
from discord.ext import commands
from infrastructure.services.logger_service import LoggerService

# Constantes de configuration
COGS_DIRECTORY = "./cogs"
IGNORED_FILES = {"__init__.py", "__pycache__"}

@dataclass
class CogLoadResult:
    """
    Structure de données pour stocker les résultats du chargement d'un cog.
    
    Attributes:
        name (str): Nom du cog
        success (bool): Si le chargement a réussi
        error (Optional[Exception]): Exception si échec
    """
    name: str
    success: bool
    error: Optional[Exception] = None

class CogLoadingSummary:
    """
    Classe pour résumer les résultats du chargement des cogs.
    
    Attributes:
        total (int): Nombre total de cogs trouvés
        successful (List[str]): Liste des cogs chargés avec succès
        failed (List[Tuple[str, Exception]]): Liste des cogs en échec avec leurs erreurs
    """
    def __init__(self):
        self.total: int = 0
        self.successful: List[str] = []
        self.failed: List[Tuple[str, Exception]] = []

    @property
    def success_rate(self) -> float:
        """Calcule le taux de réussite du chargement."""
        return len(self.successful) / self.total if self.total > 0 else 0

    def __str__(self) -> str:
        """Représentation string du résumé pour le logging."""
        return (
            f"Chargement des cogs terminé:\n"
            f"- Total: {self.total}\n"
            f"- Succès: {len(self.successful)}\n"
            f"- Échecs: {len(self.failed)}\n"
            f"- Taux de réussite: {self.success_rate:.1%}"
        )

class CogLoader:
    """
    Service responsable du chargement des extensions (cogs) Discord.
    
    Cette classe suit le principe de responsabilité unique (SRP) en ne gérant
    que le chargement des cogs.

    Attributes:
        bot (commands.Bot): Instance du bot Discord
        logger (logging.Logger): Logger dédié pour le service
        cogs_dir (Path): Chemin vers le dossier des cogs
    """

    
    def __init__(self, bot: commands.Bot, cogs_dir: str = COGS_DIRECTORY):
        """
        Initialise le service de chargement des cogs.

        Args:
            bot (commands.Bot): Instance du bot Discord
            cogs_dir (str, optional): Chemin vers le dossier des cogs
        """
        self.bot = bot
        self.cogs_dir = Path(cogs_dir)
        
        logger_service = LoggerService()
        self.logger = logger_service.get_logger(
            name=__name__,
            log_file=Path("logs/cog_loader.log")
        )

    def _setup_logging(self) -> None:
        """Configure le logging pour le service."""
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    async def load_all_cogs(self) -> CogLoadingSummary:
        """
        Charge tous les cogs valides du dossier configuré.
        
        Returns:
            CogLoadingSummary: Résumé détaillé du processus de chargement
        
        Example:
            ```python
            summary = await cog_loader.load_all_cogs()
            print(f"Cogs chargés: {summary.successful}")
            ```
        """
        self.logger.info(f"Début du chargement des cogs depuis {self.cogs_dir}")
        
        summary = CogLoadingSummary()
        cog_files = self._get_cog_files()
        summary.total = len(cog_files)

        for cog_file in cog_files:
            result = await self._load_cog(cog_file)
            
            if result.success:
                summary.successful.append(result.name)
            else:
                summary.failed.append((result.name, result.error))

        self.logger.info(str(summary))
        return summary

    def _get_cog_files(self) -> List[Path]:
        """
        Récupère tous les fichiers Python valides du dossier cogs.
        
        Returns:
            List[Path]: Liste des chemins vers les fichiers cogs valides
        """
        try:
            return [
                f for f in self.cogs_dir.glob("*.py")
                if f.name not in IGNORED_FILES and not f.name.startswith("_")
            ]
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du dossier cogs: {e}")
            return []

    async def _load_cog(self, cog_path: Path) -> CogLoadResult:
        """
        Charge un cog spécifique.
        
        Args:
            cog_path (Path): Chemin vers le fichier cog
            
        Returns:
            CogLoadResult: Résultat du chargement avec succès/erreur
        """
        cog_name = cog_path.stem
        try:
            self.logger.debug(f"Tentative de chargement de {cog_name}")
            await self.bot.load_extension(f"cogs.{cog_name}")
            self.logger.info(f"✅ Cog {cog_name} chargé avec succès")
            return CogLoadResult(cog_name, True)
            
        except Exception as e:
            self.logger.error(f"❌ Échec du chargement de {cog_name}: {str(e)}")
            return CogLoadResult(cog_name, False, e)

    async def reload_cog(self, cog_name: str) -> bool:
        """
        Recharge un cog spécifique.
        
        Args:
            cog_name (str): Nom du cog à recharger
            
        Returns:
            bool: True si rechargé avec succès, False sinon
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog_name}")
            self.logger.info(f"♻️ Cog {cog_name} rechargé avec succès")
            return True
        except Exception as e:
            self.logger.error(f"❌ Échec du rechargement de {cog_name}: {str(e)}")
            return False