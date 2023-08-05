from setuptools import setup

setup(
    name='boman-cli',
    version='0.11',    
    description='python package for boman.ai',
    url='https://boman.ai',
    author='Sumeru Software Solutions Pvt. Ltd.',
    author_email='support@boman.ai',
    license='BSD 2-clause',
    packages=['bomancli'],
    entry_points = {
        'console_scripts': ['boman-cli=bomancli.main:default'],
    },
    install_requires=['docker',
                      'requests',
                      'pyyaml',
                      'coloredlogs','xmltodict'                     
                      ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: OS Independent',        
        'Programming Language :: Python :: 3 :: Only'
    ],
)