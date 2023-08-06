"""
Your licence goes here
"""

from setuptools import setup, find_packages

# See note below for more information about classifiers
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='htmltopdfy',
    version='1.0.1',
    description='Convert template html to pdf',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
    ],
    url='https://github.com/VolkenoMakers/htmlToPdf',  # the URL of your package's home page e.g. github link
    author='VOLKENO',
    author_email='contact@volkeno-tank.com',
    keywords='core package', # used when people are searching for a module, keywords separated with a space
    license='MIT', # note the American spelling
    packages=['htmltopdfy'],
    install_requires=find_packages(), # a list of other Python modules which this module depends on.  For example RPi.GPIO
    include_package_data=True,
    zip_safe=False
)
