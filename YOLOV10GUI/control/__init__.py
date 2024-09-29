# control/__init__.py

from .control_deploy import router as control_deploy
from .control_train import router as control_trainer

__all__ = [
    "control_trainer",
    "control_deploy"
]
