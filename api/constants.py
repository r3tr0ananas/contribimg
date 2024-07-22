from decouple import config

__all__ = ("GH_API_KEY",)

GH_API_KEY = config("GH_API_KEY", cast=str)