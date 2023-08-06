# eevend-libraries
EEVEND Libraries

Based on the [Shazam Macrolib/Microlib pattern](https://medium.com/@jherreras/python-microlibs-5be9461ad979).

Macrolib:
* `eevend_lib`

Microlibs:
* `eevend_lib.micro_lib_template`: a template used to create a new micro library

## Adding a new micro library
* Copy the `demo` folder in `libraries`.
* Make your changes, remove the guff and create your new library.
* Add it to `setup.cfg`.
* Add it to this readme.


## Development
`make dev`

Installs requirements found in `dev-requirements.txt`. Installs `pre-commit` and all libraries.
> Please ensure you're in a virtual-env before running this command.

To ensure python 2 compatibility with namespaces, the `eevend_libs` directory in each micro lib should have

`__init__.py`:
```python
__import__('pkg_resources').declare_namespace(__name__)
```
Example: `libraries/demo/eevend_libs/__init__.py`

This must be the only content of the file.

## Linting
`make lint`

Runs linters and outputs results. May include side-effects. Linters in use:
* [isort](https://isort.readthedocs.io/en/latest/) sorts imports.
* [flake8](http://flake8.pycqa.org/en/latest/) runs [PEP8](https://www.python.org/dev/peps/pep-0008/) checks.

## Testing
`make test`

Runs tests for all libraries. To run tests for an individual library, `cd` into its directory (e.g. `cd libraries/demo`).

* [Pytest]() is the test runner.
* [Mock](https://docs.python.org/dev/library/unittest.mock.html) is the mocking library.

## Building
`make build`

Builds all libraries locally.

## Deployment
`Jenkinsfile` calls `scripts/build.sh` to build each library on merging to master. It also builds the main library and uploads all of them to our Pypi server.

## Issues/Todos
- Investigate why the micro libs are not building individually with the `make build` command.
- Add CI/CD and push to pypi
- Issue: 
  ```
  Error processing line 1 of /Users/manuellanouko/eevend_workspace/venv/lib/python3.7/site-packages/eevend-libs-nspkg.pth:
  Traceback (most recent call last):
    File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site.py", line 169, in addpackage
     exec(line)
    File "<string>", line 1, in <module>
    File "<frozen importlib._bootstrap>", line 580, in module_from_spec
  AttributeError: 'NoneType' object has no attribute 'loader'
  ```
  Solution:
  ```
  In vitual env, delete the .pth mentioned in the error.
  In k8s, delete the image and rebuild.
  ```
