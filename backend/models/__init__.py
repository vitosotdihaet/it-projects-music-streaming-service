# IMPORT ALL MODELS TO LOAD THEM INTO THE DB
from .user_activity import EventModel, UserActivityModel
from .base_model import create_tables

__all__ = [
    'create_tables'
]
