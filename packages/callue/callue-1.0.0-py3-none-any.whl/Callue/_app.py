import os
import bottle
from . import default_routes
from .util import EnableCors, minify
from .routemap import _execute_routemap

_app = bottle.app()

callue_route = _app.route
callue_get = _app.get
callue_post = _app.post

_app.install(EnableCors())
pages = {
  'frontend': '',
  'homepage': '',
  'favicon': None
}

def setup(*, frontend='./frontend', homepage='index.html', favicon='favicon.png'):
  pages['frontend'] = frontend
  
  _execute_routemap(_app, pages['frontend'])
  default_routes.init(_app, pages)
  
  pages['homepage'] = minify(os.path.join(frontend, homepage))
  pages['favicon']  = bottle.static_file(favicon, root=frontend)

def run(port=80, quiet=True):
  """
  Launch the HTTP server in a blocking function.
  """

  _app.run(host='0.0.0.0', port=port, server='paste', quiet=True)