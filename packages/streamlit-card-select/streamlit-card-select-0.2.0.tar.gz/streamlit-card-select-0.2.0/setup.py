import importlib
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    loc = dict()
    with open('streamlit_card_select/__version__.py') as f:
        exec(f.read(), loc, loc)
    return loc.get('__version__')

def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="streamlit-card-select",
    version=version(),
    author="Mirko Mälicke",
    author_email="mirko@hydrocode.de",
    description="Streamlit component to select a card from a grid",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=requirements(),
)
