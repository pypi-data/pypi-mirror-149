import importlib
from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    cs = importlib.import_module('streamlit_card_select')
    return cs.__version__

def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="streamlit-card-select",
    version='0.0.1',
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
