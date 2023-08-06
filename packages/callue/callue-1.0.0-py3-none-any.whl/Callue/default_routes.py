import os
import bottle
from .util import minify, to_minify
from .routemap import overrides_default

def init(app, pages):  
  if not '/' in overrides_default:
    @app.route('/')
    def homepage():
      return pages['homepage']
  
  if not '/favicon.png' in overrides_default:
    @app.route('/favicon.png')
    def favicon():
      return pages['favicon']
  
  if not '/<filepath:path>' in overrides_default:
    @app.route('/<filepath:path>')
    def return_static(filepath):
      filepath = os.path.join(pages['frontend'], filepath)
      
      if os.path.isdir(filepath):
        try:
          return bottle.static_file(filepath, root=pages['frontend'])
        except FileNotFoundError:
          bottle.abort(404, 'File not found')
      
      if not '.' in filepath[1:]:
        filepath = filepath + '.html'
    
      if filepath.split('.')[-1] in to_minify:
        try:
          static_file = minify(filepath)
        except FileNotFoundError:
          bottle.abort(404, 'File not found')
      else:
        try:
          static_file = bottle.static_file(filepath, root=pages['frontend'])
        except FileNotFoundError:
          bottle.abort(404, 'File not found')

      return static_file