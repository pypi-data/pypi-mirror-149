from . import _version
from .QuestionnaireClient import QuestionnaireClient

__version__ = _version.get_versions()['version']

__all__ = ["QuestionnaireClient"]
