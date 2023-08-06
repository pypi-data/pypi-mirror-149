from setuptools import find_packages, setup
import pathlib

with open(str(pathlib.Path(__file__).parent.absolute()) + "/fib_py/version.py", "r") as fh:
    version = fh.read().split("=")[1].replace("'", "")

setup(
    name="ssshikari_fib_py",
    version=version,
    author="ssshikari",
    author_email="ssshikari@gmail.com",
    description="Calculates a Fibonacci number",
    long_description="A basic library that calculates Fibonacci numbers",
    long_description_content_type="text/markdown",
    url="https://github.com/ValikMinak/fib",
    install_requires=[
        "PyYAML>=4.1.2",
        "dill>=0.2.8"
    ],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fib-number = fib_py.cmd.fib_numb:fib_numb',
        ],
    },
)
