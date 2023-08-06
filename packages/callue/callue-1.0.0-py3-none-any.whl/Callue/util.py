import bottle
from jsmin import jsmin
from pathlib import Path
from rcssmin import cssmin
from htmlmin import minify as htmlmin

to_minify = ['css', 'js', 'html']

code_cache = {}
code_cache_max_length = 64

class EnableCors(object):
  name = 'enable_cors'
  api = 2
  
  def apply(self, fn, context):
    def _enable_cors(*args, **kwargs):
      bottle.response.headers['Access-Control-Allow-Origin'] = '*'
      bottle.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
      bottle.response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
      if bottle.request.method != 'OPTIONS':
        return fn(*args, **kwargs)
    return _enable_cors

def minify(path, language=None):
  if path in code_cache:
    return code_cache[path]
  if language is None:
    language = path.split('.')[-1]
  code = Path(path).read_text()
  
  if language == 'js':
    minified = jsmin(code)
  elif language == 'css':
    minified = cssmin(code)
  elif language == 'html':
    minified = htmlmin(code)
  else:
    return code
  
  code_cache[path] = minified
  if len(code_cache.keys()) > code_cache_max_length:
    del code_cache[next(iter(code_cache))]

  return minified