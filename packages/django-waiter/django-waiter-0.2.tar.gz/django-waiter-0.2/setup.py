import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-waiter',
    version='0.2',
    install_requires=[
        "Django>=1.11,<3.3"
    ],
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='Django useful tools for developments.',
    long_description=README,
    url='https://github.com/mrgaolei/django-waiter',
    author='mrgaolei',
    author_email='guafeng@fmit.cn',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
