import logging
import pathlib

import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-RadioWorld").version

logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = "Mopidy-RadioWorld"
    ext_name = "radioworld"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        #schema["username"] = config.String()
        #schema["password"] = config.Secret()
        return schema

    def setup(self, registry):
        from .backend import RadioWorldBackend
        registry.add('backend', RadioWorldBackend)

        # TODO: Edit or remove entirely
        registry.add(
            "http:static",
            {
                "name": self.ext_name,
                "path": str(pathlib.Path(__file__).parent / "static"),
            },
        )
