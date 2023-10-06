from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='countdown-numbers-solver',
    version='1.0',
    author='Daniel Davis',
    description='A brief synopsis of the project',
    long_description=long_description,
    url='https://github.com/DanielDavisEE/CountdownProblem',
    python_requires='>=3.10, <4',
    package_dir={'': 'src'},
    packages=['countdown_numbers_solver'],
    install_requires=[
    ],
    package_data={
    },
    entry_points={
    }
)
