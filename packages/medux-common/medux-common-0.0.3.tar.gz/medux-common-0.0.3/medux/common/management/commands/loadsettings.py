import logging
from pathlib import Path

from django.apps import apps
from django.core.management import BaseCommand

from medux.settings.loaders import TomlSettingsLoader

logger = logging.getLogger(__file__)


class Command(BaseCommand):
    """Loads vendor settings.toml in each app into the database"""

    help = "DEV COMMAND: Load (VENDOR) settings from a file into the database."

    def handle(self, *args, **options):
        for app in apps.get_app_configs():
            filename = Path(app.path, "settings.toml")
            if filename.exists():
                from medux.settings import Scope

                loader = TomlSettingsLoader(filename, scope=Scope.VENDOR)
                loader.load()

                logger.info(f"Loaded settings from {filename} into database.")
