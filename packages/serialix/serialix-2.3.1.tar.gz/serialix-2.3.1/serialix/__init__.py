"""
Here is the main initialization code that makes
it easier to access the main features of the
other submodules and subpackages
"""
from .meta import version as __version__, author as __author__
from .serialix import Serialix
from .langs.json import JSON_Format


try:
    from .langs.yaml import YAML_Format
except ImportError:
    pass

try:
    from .langs.toml import TOML_Format
except ImportError:
    pass
