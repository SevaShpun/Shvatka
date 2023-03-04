from src.core.models.dto import scn
from .level import LevelSchema

__all__ = ["LevelSchema", "schemas"]


schemas = {
    scn.LevelScenario: LevelSchema(),
}
