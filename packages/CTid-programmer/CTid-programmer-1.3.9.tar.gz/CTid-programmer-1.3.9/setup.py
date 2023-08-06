import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='CTid-programmer',
    version='1.3.9',
    packages=setuptools.find_packages(),
    package_data={
        '': ['resources/code/*.hex']
    },
    install_requires=['egauge-python>=0.5.9,!=0.21',
                      'importlib_resources', 'wheel'],
    entry_points={
        'console_scripts': [
            'CTid-programmer = ctid_programmer.programmer:main'
        ]
    },
    license='MIT License',  # example license
    description='A graphical user interface for programming CTid sensors.',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://bitbucket.org/egauge/CTid-programmer/',
    author='David Mosberger-Tang',
    author_email='davidm@egauge.net',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Hardware'
    ],
)
