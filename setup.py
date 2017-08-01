from setuptools import setup
from setuptools.extension import Extension

module = Extension('astrohut/core/astrohutc',
                    sources = ['astrohut/core/box2d.c'], include_dirs=['astrohut'], extra_compile_args=["-fopenmp", "-O2"],
                     extra_link_args=["-fopenmp", "-O2"])

setup(
    name = "astrohut",
    version = "0.0.5",
    author = "Juan Barbosa",
    author_email = "js.barbosa10@uniandes.edu.co",
    description = ('Barnes-Hut NBody simulation library.'),
    license = "GPL",
    keywords = "example documentation tutorial",
    packages=['astrohut', 'astrohut/core', 'astrohut/data', 'astrohut/testing'],
    install_requires=['matplotlib', 'numpy'],
    ext_modules = [module],
    long_description="https://github.com/jsbarbosa/astro-hut/",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    headers = ["astrohut/core/box2d.h"],
)
