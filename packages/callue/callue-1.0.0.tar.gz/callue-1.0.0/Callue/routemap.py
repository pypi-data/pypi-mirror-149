import re
import os
import bottle
from pathlib import Path

TOKENS = {
  'COMMENT': re.compile('#(.*?)$', re.MULTILINE),
  'DUPLICATE_WHITESPACE': re.compile('\s{2,}', re.MULTILINE),
  'NEW_ROUTE': ';'
}

routemap_variables = {}

overrides_default = []

class Route:
  def __init__(self, target, destination, is_template=False, template_params={}):
    self.target = target
    self.destination = destination
    self.is_template = is_template
    self.template_params = template_params

def strip_comments(code):
  return re.sub(TOKENS['COMMENT'], '', code)

def strip_whitespace(code):
  return re.sub(TOKENS['DUPLICATE_WHITESPACE'], ' ', code)

def split_routes(code):
  return code.split(TOKENS['NEW_ROUTE'])[:-1]

def make_route(code):
  code = code.split('->')
  target = code[0].strip()
  code = list(map(lambda x: x, code[1].split(' ')))
  code = [token for token in code if token]
  is_template = {
    'serves': False,
    'renders': True
  }[code[0]]
  # We do not want the / at the beginning of the path
  destination = code[1][1:]
  if is_template:
    raw_template_params = ' '.join(code[3:]).split(' and ')
    template_params = {}
    for param in raw_template_params:
      param = param.split(' is ')
      if param[1].startswith('{') and param[1].endswith('}'):
        param[1] = eval(param[1][1:-1], routemap_variables)
      template_params[param[0]] = param[1]
    return Route(target, destination, True, template_params)
    
  return Route(target, destination, False)

def _execute_routemap(app, frontend_dir):
  routemap = Path(os.path.join(frontend_dir, '.routemap')).read_text('utf-8')
  routemap = strip_comments(routemap)
  routemap = strip_whitespace(routemap)
  routemap = split_routes(routemap)
  for route in routemap:
    route = make_route(route)
    overrides_default.append(route.target)
    @app.route(route.target)
    def routemap_route():
      if route.is_template:
        return bottle.template(os.path.join(frontend_dir, route.destination), route.template_params)
      else:
        return bottle.static_file(route.destination, root=frontend_dir)