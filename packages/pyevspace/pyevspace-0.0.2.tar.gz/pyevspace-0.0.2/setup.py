from setuptools import setup, find_packages, Extension

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'pyevspace',
    version = '0.0.2',
    author="Quinton Barnes",
    author_email="devqbizzle68@gmail.com",
    description="A Euclidean vector space module.",
    package = find_packages(),
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url="https://github.com/qbizzle68/pyevspace",
    license = 'MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        ],
    ext_modules=[
        Extension(
            'pyevspace',
            include_dirs = ['pyevspace/include'],
            sources = ['pyevspace/src/evspacemodule.c'],
        ),
    ],
    python_requires=">=3.6",
)
