from setuptools import setup

LIBRARY_NAME = 'eevend_libs.utils'


def get_version():
    with open('version') as version_file:
        return version_file.read()


def get_requirements():
    with open('requirements.txt') as requirements_file:
        return [dependency.strip() for dependency in requirements_file if dependency.strip()]


setup_args = {
    'name': LIBRARY_NAME,
    'version': get_version(),
    'author': 'EEVEND',
    'author_email': "info.eevend@gmail.com",
    'description': 'Houses the utils',
    'install_requires': get_requirements(),
    'namespace_packages': ['eevend_libs'],
    'packages': [LIBRARY_NAME],
}

setup(**setup_args)
