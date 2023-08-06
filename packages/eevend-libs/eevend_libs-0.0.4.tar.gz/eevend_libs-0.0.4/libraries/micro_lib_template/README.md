# Business Systems Template library
This is a template library to ease the creation of a new micro library

## Usage
Add the dependency to your project: `eevend_libs.micro_lib_template`. In code:
```python
>>> # Import the micro lib template helper from the lib
>>> from eevend_libs.micro_lib_template.micro_lib_template import MicroLibTemplate
>>> micro_lib_template = MicroLibTemplate()
>>> greeting = micro_lib_template.greeting("Bob") # Examples of this call below...
>>> print(greeting)
'Hello Bob'
```
