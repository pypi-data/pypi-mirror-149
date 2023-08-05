from setuptools import setup, find_packages
from notdb_viewer import __version__ as v

# README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

packages = [
    'notdb_viewer.server',
    *find_packages()
]

setup(
    name='notdb_viewer',
    packages=packages,
    install_requires=[
        'pyonr',
        'bcrypt',
        'flask',
        'flask_minify'
    ],
    version=v,
    description='Viewer for NotDB Databases',
    author='Nawaf Alqari',
    author_email='nawafalqari13@gmail.com',
    keywords=['notdb', 'db', 'database', 'notdatabsae', 'simple database'],
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['notdb_viewer=notdb_viewer.__main__:main']
    },
    license='MIT',
    zip_safe=False,
    url='https://github.com/nawafalqari/NotDB_Viewer/',
    project_urls={
        'Documentation': 'https://github.com/nawafalqari/NotDB_Viewer#readme',
        'Bug Tracker': 'https://github.com/nawafalqari/NotDB_Viewer/issues',
        'Source Code': 'https://github.com/nawafalqari/NotDB_Viewer/',
        'Discord': 'https://discord.gg/cpvynqk4XT'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)