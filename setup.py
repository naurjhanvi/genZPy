from setuptools import setup, find_packages

setup(
    name='genzpy',
    version='0.1.0',
    description='An interpreter for the GenZPy programming language.',
    author='Jhanvi', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'genzpy=genzpy.interpreter:main',
        ],
    },
)