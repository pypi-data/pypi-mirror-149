import pathlib

import pkg_resources

from mopidy import config, ext
from tornado import locale


__version__ = pkg_resources.get_distribution(
    "Mopidy-Market"
).version

import logging
logger = logging.getLogger(__name__)

class Extension(ext.Extension):

    dist_name = "Mopidy-Market"
    ext_name = "market"
    version = __version__

    changes = []

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        return schema

    def setup(self, registry):
        self.extensions_data = ext.load_extensions()

        registry.add(
            "http:app", {"name": self.ext_name, "factory": self.factory}
        )

    def factory(self, config, core):
        from tornado.web import RedirectHandler
        from .web import IndexHandler, StaticHandler, MarketApiHandler

        path = pathlib.Path(__file__).parent / "static"
        return [
            (r"/", RedirectHandler, {"url": "index.html"}),
            (r"/(index.html)", IndexHandler, {"config": config, "path": path}),
            (r"/marketapi/(.*)", MarketApiHandler, {"config": config, "core": core, "path": path, "extensions": self.extensions_data, "changes": self.changes}),
            (r"/(.*)", StaticHandler, {"path": path}),
        ]
