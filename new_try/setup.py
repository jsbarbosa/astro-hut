from setuptools import setup
from setuptools.extension import Extension

module1 = Extension('astrohut/astrohutc',
                    sources = ['astrohut/box2d.c'], include_dirs=['astrohut'], extra_compile_args=["-fopenmp"],
                     extra_link_args=["-fopenmp"])

setup(
    name = "astrohut",
    version = "0.0.2",
    author = "Juan Barbosa",
    author_email = "js.barbosa10@uniandes.edu.co",
    description = ('Barnes-Hut NBody simulation library.'),
    license = "GPL",
    keywords = "example documentation tutorial",
    packages=['astrohut'],
    install_requires=['matplotlib', 'numpy'],
    ext_modules = [module1],
    long_description="https://jsbarbosa.github.io/rippleTank/",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    headers = ["astrohut/box2d.h"],
)
