import os
from setuptools import setup, find_packages

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="django-mem0-client",
    version="0.1.2",
    author="Xavier Jodoin",
    author_email="xavier@jodoin.me",
    description="A Django implementation of the mem0 memory system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xjodoin/django-mem0-client",
    packages=find_packages(include=['mem0client', 'mem0client.*']),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0.0",
        "mem0ai>=0.1.58",
        "pytz>=2022.1",
        "pydantic>=1.9.0",
    ],
    keywords="django, mem0, memory, ai",
)