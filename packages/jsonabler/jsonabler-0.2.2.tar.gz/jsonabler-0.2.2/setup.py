from setuptools import setup


def get_version():
    with open("jsonabler/__init__.py") as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                return line.split('"' if '"' in line else "'")[1]

        else:
            raise RuntimeError("Unable to find version string.")


def get_requirements():
    with open("requirements.txt") as f:
        return [
            line.split('#', 1)[0].strip() for line in f.read().splitlines()
            if not line.strip().startswith('#')
        ]


def get_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="jsonabler",
    version=get_version(),
    author="webfucktory",
    author_email="root@webfucktory.com",
    description="Python package for making your classes easy encodable to JSON string and vice-versa",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/webfucktory/python-jsonabler",
    packages=['jsonabler'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.8',
    install_requires=get_requirements(),
)
