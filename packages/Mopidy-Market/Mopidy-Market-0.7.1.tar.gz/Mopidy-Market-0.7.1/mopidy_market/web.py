import json
import logging
import socket
import string
import urllib.parse
import configparser
import tornado.web
import tornado.locale
import subprocess
import sys
logger = logging.getLogger(__name__)
import json
import urllib.parse
from bs4 import BeautifulSoup
import requests
from configupdater import ConfigUpdater
import os


class StaticHandler(tornado.web.StaticFileHandler):
    def get(self, path, *args, **kwargs):
        version = self.get_argument("v", None)
        if version:
            logger.debug("Get static resource for %s?v=%s", path, version)
        else:
            logger.debug("Get static resource for %s", path)
        return super().get(path, *args, **kwargs)


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, config, path):

        url = urllib.parse.urlparse(
            f"{self.request.protocol}://{self.request.host}"
        )
        port = url.port or 80
        try:
            ip = socket.getaddrinfo(url.hostname, port)[0][4][0]
        except Exception:
            ip = url.hostname

        self.__dict = {
            "serverIP": ip,
            "serverPort": port,
        }
        self.__path = path
        self.__title = string.Template(f"Market on $hostname")

    def get(self, path):
        return self.render(path, title=self.get_title(), **self.__dict)

    def get_title(self):
        url = urllib.parse.urlparse(
            f"{self.request.protocol}://{self.request.host}"
        )
        return self.__title.safe_substitute(hostname=url.hostname)

    def get_template_path(self):
        return self.__path

class MarketApiHandler(tornado.web.RequestHandler):


    icons = {
             'yamusic': 'icons/yamusic.svg',
             'mpd': 'icons/mpd.png',
             'musicbox_darkclient': 'icons/musicbox_darkclient.png',
             'emby': 'icons/emby.ico',
             'bandcamp': 'icons/bandcamp.png',
             'beets': 'icons/beets.png',
             'funkwhale': 'icons/funkwhale.png',
             'internetarchive': 'icons/internetarchive.png',
             'dleyna': 'icons/dleyna.png',
             'jellyfin': 'icons/jellyfin.svg',
             'mixcloud': 'icons/mixcloud.png',
             'orfradio': 'icons/orfradio.png',
             'jamendo': 'icons/jamendo.svg',
             'pandora': 'icons/pandora.jpg',
             'podcast-itunes': 'icons/podcast-itunes.png',
             'tunein': 'icons/tunein.svg',
             'radionet': 'icons/radionet.png',
             'somafm': 'icons/somafm.gif',
             'soundcloud': 'icons/soundcloud.png',
             'spotify': 'icons/spotify.png',
             'subidy': 'icons/subidy.png',
             'youtube': 'icons/youtube.png',
             'ytmusic': 'icons/ytmusic.png',
             'iris': 'icons/iris.jpg',
             'mobile': 'icons/mobile.jpg',
             'mopster': 'icons/mopster.png',
             'mowecl': 'icons/mowecl.png',
             'muse': 'icons/muse.jpg',
             'musicbox_webclient': 'icons/musicbox_webclient.jpg',
             'party': 'icons/party.jpg',
             'mpris': 'icons/mpris.png',
             'alsamixer': 'icons/alsamixer.png',
             'nad': 'icons/nad.png'
     }


    schemas = {
     "core" : { 'cache_dir': 'Path', 'config_dir': 'Path', 'data_dir': 'Path', 'max_tracklist_length': 'Integer', 'restore_state': 'Boolean'},
     "logging": {'verbosity': "Integer", 'format': 'String', 'color': 'Boolean'  },
     "audio": {'mixer': 'String', 'mixer_volume': 'Integer', 'output': 'String', 'buffer_time': 'Integer'},
     "proxy": {'scheme': 'String', 'hostname': 'String', 'port': 'String', 'username': 'String', 'password': 'Secret'}
    }

    cannot_remove = [
     "core","logging","audio","proxy","file","http","m3u","softwaremixer","stream","local"
    ]

    available = [ "bandcamp", "beets", "dleyna", "funkwhale", "internetarchive", "jamendo", "jellyfin", "local","mixcloud","orfradio","pandora","podcast","podcast-itunes",
                  "radionet", "somafm", "soundcloud", "spotify", "stream", "subidy", "tunein", "youtube","ytmusic","iris","mobile","mopster","mowecl","muse","musicbox_webclient","musicbox_darkclient","party",
                  "autoplay", "headless", "mpd", "mpris", "pidi", "raspberry-gpio", "scrobbler", "alsamixer", "nad", "softwaremixer" ]

    def initialize(self, config, core, path, extensions, changes):
        self.config = config
        self.extensions = extensions
        self.core = core
        self.changes = changes
        url = urllib.parse.urlparse(
            f"{self.request.protocol}://{self.request.host}"
        )
        port = url.port or 80
        try:
            ip = socket.getaddrinfo(url.hostname, port)[0][4][0]
        except Exception:
            ip = url.hostname


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


    def get_config_schema(self, module):
        for ext in self.extensions:
          logger.error(ext.extension.ext_name)

          if ext.extension.ext_name == module:
             return ext.config_schema

    def is_jsonable(self,x):
      try:
        json.dumps(x)
        return True
      except (TypeError, OverflowError):
        return False

    def options(self, path):
      logger.error('options')
      logger.error(path)
      if 'save/' in path:
         self.write({'name':path})

    def post(self, path):
      logger.error('post')
      logger.error(path)
      if 'save/' in path:
          params = path.split('/')
          module = params[1]
          config = ConfigUpdater()
          home = os.path.expanduser("~")
          configfile = os.path.join(home,'.config/mopidy/mopidy.conf')
          config.read(configfile)
          if not module in config.sections():
            config.add_section(module)
          logger.error(config.sections())
          logger.error(self.request.body)
          data = json.loads(self.request.body)
          result = 'saved'
          for c in data:
            logger.error(c)
            if data[c] != "" and data[c] != None:
              if isinstance(data[c],list):
                if ", ".join(data[c]) != config[module][c]:
                   result = 'changed'
                config[module][c] = ", ".join(data[c])
              else:
                if str(data[c]) != config[module][c]:
                   result = 'changed'
                config[module][c] = str(data[c])
          logger.error(config[module])
          if result == "changed":
            self.changes.append({"name":module,"changes":"configuration changed"})
          with open(configfile, 'w') as newini:
             config.write(newini)
          self.write(json.dumps({'name':module,'result':result}))


    def get(self, path):
        if 'config/' in path:
          params = path.split('/')
          module = params[1]
          result = {}
          if module in self.config:
            for c in self.config[module]:
              if self.is_jsonable(self.config[module][c]):
                result[c] = self.config[module][c]
              else:
                logger.error(type(self.config[module][c]))

          logger.error(result)
          self.write(json.dumps(result))
        elif 'configschema/' in path:
          params = path.split('/')
          module = params[1]
          if module in self.schemas:
            self.write(json.dumps(self.schemas[module]))
            return
          schema = self.get_config_schema(module)
          result = {}
          if schema != None:
            for c in schema:
              result[c] = schema[c].__class__.__name__
          self.write(json.dumps(result))
        elif path == 'installed':
           modules = []
           for module in self.config:
             if module == "market":
               continue
             if module in self.icons:
               icon = self.icons[module]
             else:
               icon = ""
             if 'enabled' in self.config[module]:
               enabled = self.config[module]['enabled']
             elif module in self.schemas:
               enabled = True
             else:
               enabled = False
             modules.append({"name":module, "image": icon, "enabled": enabled })
           self.write(json.dumps(modules))
        elif path == 'available':
           modules = []
           for module in self.available:
             if module in self.config:
               continue
             if module in self.icons:
               icon = self.icons[module]
             else:
               icon = ""
             modules.append({"name":module, "image": icon})
           self.write(json.dumps(modules))
        elif 'extinfo/' in path:
          params = path.split('/')
          module = params[1]
          webname = module.replace('_','-')
          url = f"https://mopidy.com/ext/{webname}/"
          r = requests.get(url, allow_redirects=True)
          if r.status_code == 200:
            html = r.content
            parsed_html = BeautifulSoup(html)
            parsed_html.find('nav', attrs={'class':"breadcrumb"}).decompose()
            if parsed_html.find('div', attrs={'class':"tabs"}) != None:
              parsed_html.find('div', attrs={'class':"tabs"}).decompose()
            for img in parsed_html.findAll('img'):
              if not 'http' in img['src']:
                img['src'] = 'https://mopidy.com'+img['src']
            content = parsed_html.body.find('section', attrs={'class':'section'})
            self.write(str(content))
          else:
            self.write("")
        elif "canremove/" in path:
          params = path.split('/')
          module = params[1]
          self.write(json.dumps({"result":(not (module in self.cannot_remove)) and (module in self.config)}))
        elif path == 'pending':
          self.write(json.dumps(self.changes))
        elif 'uninstall/' in path:
          params = path.split('/')
          module = params[1]
          subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", f"mopidy-{module}"])
          self.changes.append({"name":module,"changes":"uninstalled"})
          self.write(json.dumps({'name':module,'result':'uninstalled'}))
        elif 'install/' in path:
          params = path.split('/')
          module = params[1]
          subprocess.check_call([sys.executable, "-m", "pip", "install", f"mopidy-{module}"])
          self.changes.append({"name":module,"changes":"installed"})
          self.write(json.dumps({'name':module,'result':'installed'}))
        else:
          self.write(json.dumps({'error':'not found'}))
