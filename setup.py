import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

requirements = ['django-imagekit==4.1.0', 'Pillow==9.1.1']

setup(
    name='django-starcross-gallery',
    version='1.0.14',
    packages=find_packages(),
    include_package_data=True,
    license='GNU LGPLv3',
    description='A streamlined Django gallery app with justified layout, infinite scrolling, and drag & drop uploading',
    long_description=README,
    url='https://starcross.dev',
    author='Alex Luton',
    author_email='gallery@starcross.dev',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=requirements,
)
