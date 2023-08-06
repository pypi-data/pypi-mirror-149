import setuptools

import readycheck


with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name="readycheck",
    version=readycheck.__version__,
    author=readycheck.__author__,
    author_email="loic.simon@espci.org",
    description="Run custom checks on classes attributes when accessing them",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/loic-simon/readycheck",
    py_modules=["readycheck"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.10',
)

# python3 setup.py sdist bdist_wheel
# twine upload dist/*
