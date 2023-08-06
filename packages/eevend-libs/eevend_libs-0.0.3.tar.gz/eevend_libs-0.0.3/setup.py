import pprint

import setuptools

LIBRARY_NAME = 'eevend_libs'
LIBRARIES = {
    'micro_lib_template': 'libraries/micro_lib_template',
    'service': 'libraries/service',
    'client': 'libraries/client',
    'flask_service_exceptions': 'libraries/flask_service_exceptions',
    'utils': 'libraries/utils',
    'constants': 'libraries/constants',
}


def get_requirements():
    requirements = []
    for lib in LIBRARIES.values():
        with open('%s/requirements.txt' % lib) as f:
            required = f.read().splitlines()
        requirements += required
    return requirements


def get_package_dirs():
    dirs = {}
    for lib in LIBRARIES:
        dirs['%s.%s' % (LIBRARY_NAME, lib)] = 'libraries/%s/eevend_libs/%s' % (lib, lib)
    return dirs


def get_version():
    with open('version') as version_file:
        return version_file.read()


package_dirs = get_package_dirs()
print('Building the following libraries:')
pprint.pprint(package_dirs)
setup_args = {
    'name': LIBRARY_NAME,
    'version': get_version(),
    'author': 'EEVEND',
    'author_email': "info.eevend@gmail.com",
    'package_dir': package_dirs,
    'packages': package_dirs.keys(),
    'namespace_packages': ['eevend_libs'],
    'install_requires': get_requirements()
}

setuptools.setup(**setup_args)
