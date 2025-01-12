import logging
from typing import Optional
from pathlib import Path

class LoggerService:
    """
    Service centralisé pour la gestion des logs.
    
    Cette classe suit le pattern Singleton pour assurer une configuration
    cohérente des logs à travers l'application.
    
    Attributes:
        default_format (str): Format par défaut des logs
        default_level (int): Niveau de log par défaut
    """
    _instance = None
    
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DEFAULT_LEVEL = logging.INFO
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        self.default_format = self.DEFAULT_FORMAT
        self.default_level = self.DEFAULT_LEVEL
        
    def get_logger(
        self,
        name: str,
        level: Optional[int] = None,
        format: Optional[str] = None,
        log_file: Optional[Path] = None
    ) -> logging.Logger:
        """
        Récupère ou crée un logger configuré.
        
        Args:
            name (str): Nom du logger
            level (Optional[int]): Niveau de log
            format (Optional[str]): Format des logs
            log_file (Optional[Path]): Chemin du fichier de log
            
        Returns:
            logging.Logger: Logger configuré
        """
        logger = logging.getLogger(name)
        
        if not logger.handlers:  
            formatter = logging.Formatter(
                format or self.default_format
            )
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            
            logger.setLevel(level or self.default_level)
        
        return logger