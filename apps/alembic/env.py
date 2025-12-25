from apps.app.db.base import Base
from apps.app.db import models  # noqa: F401  (force l'import de tous les modèles)

target_metadata = Base.metadata
