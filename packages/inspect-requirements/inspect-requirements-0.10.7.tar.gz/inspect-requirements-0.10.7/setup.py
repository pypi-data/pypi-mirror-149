from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

requirements = (
    'requirements-parser==0.5.0',
    'setuptools',
)

VERSION = '0.10.7'

setup(
    name='inspect-requirements',
    zip_safe=False,
    version=VERSION,
    description='Inspect requirements.txt files of multiple repositories.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[],
    keywords=['requirements', 'pip'],
    author='Teemu Husso',
    author_email='teemu.husso@gmail.com',
    url='https://github.com/Raekkeri/inspect-requirements',
    download_url=f'https://github.com/raekkeri/inspect-requirements/tarball/{VERSION}',
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'inspect-requirements = inspect_requirements.inspect_requirements:console_command',
        ]
    },
)
