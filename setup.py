import os
from distutils.core import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='clico',
    packages=find_packages(),
    python_requires='>=3.7',
    version='0.2',
    license='Apache Software License',
    description='The library implements create short links via https://cli.com (Ex. cli.co) service.',
    long_description=README,
    author='pixel365',
    author_email='pixel.365.24@gmail.com',
    url='https://github.com/pixel365/clico',
    download_url='https://github.com/pixel365/clico/archive/master.zip',
    keywords=['cli.com', 'cli.co', 'clico', 'short link'],
    install_requires=[
        'requests >=2.22.0',
        'pydantic >=1.7.3',
        'validators >=0.18.2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
