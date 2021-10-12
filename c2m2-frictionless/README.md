# c2m2-frictionless

The [C2M2 Documentation](https://docs.nih-cfde.org/en/latest/c2m2/draft-C2M2_specification/) links to the C2M2 JSON Frictionless Schema, currently <https://osf.io/vzgx9/>. We use the frictionless-dataclass package to update the c2m2-frictionless package.

## Installation
```bash
pip3 install "c2m2-frictionless @ git+https://github.com/nih-cfde/c2m2-frictionless-dataclass#egg=c2m2-frictionless&subdirectory=c2m2-frictionless"
```

## Usage
Given this package, the DCC datapackage preparation script can take the following form:

```python
import c2m2_frictionless
from c2m2_frictionless import C2M2

def c2m2_generator():
  ns = C2M2.id_namespace(
    id='my_ns',
    abbreviation='MYDCC',
    name='My DCC',
    description='My DCC is about things',
  )
  # emit records as they are generated in any order
  yield ns
  project = C2M2.project(
    id_namespace=ns.id,
    local_id='MYDCC',
    abbreviation='MYDCC',
    name='My DCC',
    description='My DCC is about things',
  )
  yield project
  # resolve any number of files, subjects, etc.. and map them to the C2M2 model from
  #  the DCC's internal database or API.
  for record in my_dcc_query():
    pass # emit files, subjects, etc..

if __name__ == '__main__':
  datapackage = 'datapackage'
  # construct a c2m2 datapackage directory using the generator above
  pkg = c2m2_frictionless.create_datapackage('C2M2', c2m2_generator(), datapackage)
  # automatically resolve ontological terms
  c2m2_frictionless.build_term_tables(datapackage)
  # ensure validity of the datapackage
  c2m2_frictionless.validate_datapackage(pkg)
  validate_id_namespace_name_uniqueness(pkg)
```
