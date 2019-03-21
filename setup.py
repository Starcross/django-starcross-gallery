import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = ['django-imagekit==4.0.2', 'Pillow==5.0.0']

setup(
    name='django-starcross-gallery',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='GNU LGPLv3',
    description='A streamlined Django gallery app.',
    long_description=README,
    url='http://starcross.eu',
    author='Alex Luton',
    author_email='gallery@starcross.eu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=requirements,
)
