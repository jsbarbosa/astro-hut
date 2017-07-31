from setuptools import setup
from setuptools.extension import Extension

module = Extension('astrohut/astrohutc',
                    sources = ['astrohut/core/box2d.c'], include_dirs=['astrohut'], extra_compile_args=["-fopenmp"],
                     extra_link_args=["-fopenmp"])

setup(
    name = "astrohut",
    version = "0.0.3",
    author = "Juan Barbosa",
    author_email = "js.barbosa10@uniandes.edu.co",
    description = ('Barnes-Hut NBody simulation library.'),
    license = "GPL",
    keywords = "example documentation tutorial",
    packages=['astrohut'],
    install_requires=['matplotlib', 'numpy'],
    ext_modules = [module],
    long_description="https://github.com/jsbarbosa/astro-hut/",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    headers = ["astrohut/box2d.h"],
)
