# Ce fichier existe pour forcer le chargement des modèles
# au démarrage et éviter les migrations vides.

from app.db import models  # noqa: F401
