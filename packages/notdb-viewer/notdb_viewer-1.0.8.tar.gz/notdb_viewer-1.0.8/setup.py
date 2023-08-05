from setuptools import setup, find_packages
from notdb_viewer import __version__ as v

# README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

packages = [
    # 'notdb_viewer/server',
    *find_packages(where='notdb_viewer')
]

setup(
    name='notdb_viewer',
    packages=packages,
    # include_package_data=True,
    package_data={
        'notdb_viewer.server.templates': ['viewer.html']
    },
    version=v,
    description='Viewer for NotDB Databases',
    author='Nawaf Alqari',
    author_email='nawafalqari13@gmail.com',
    keywords=['notdb', 'db', 'database', 'notdatabsae', 'simple database'],
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
    'console_scripts': [ 'notdb_viewer=notdb_viewer.__main__:main']
    },
    license='MIT',
    url='https://github.com/nawafalqari/notdb_viewer/',
    project_urls={
        'Documentation': 'https://github.com/nawafalqari/NotDB#readme',
        'Bug Tracker': 'https://github.com/nawafalqari/NotDB/issues',
        'Source Code': 'https://github.com/nawafalqari/NotDB/',
        'Discord': 'https://discord.gg/cpvynqk4XT'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)