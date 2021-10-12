import click
import jinja2
import importlib
from pathlib import Path
from datapackage import DataPackage

def _jinja2_env(root):
  ''' Setup jinja2 environment from directory
  /templates/*  => .j2 templates
  /filters/*.py => .py filters
  '''
  env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(root / 'templates'),
    keep_trailing_newline=True,
  )
  for filter_py in (root / 'filters').glob('[!_]*.py'):
    mod = importlib.import_module(f".filters.{filter_py.stem}", __package__)
    filter_func = getattr(mod, filter_py.stem)
    env.filters[filter_py.stem] = filter_func
  return env

@click.command()
@click.option('-i', '--input', type=click.File('r'), default='-', help='Datapackage specification')
@click.option('-o', '--output', type=click.File('w'), default='-', help='Python dataclass file')
def cli(input, output):
  # prepare datapackage
  pkg = DataPackage(input)
  # prepare jinja2 environment
  env = _jinja2_env(Path(__file__).parent)
  # render template
  (env.get_template('dataclass.py.j2')
    .stream(pkg=pkg)
    .dump(output))

if __name__ == '__main__':
  cli()
