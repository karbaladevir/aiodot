"""aiodot - Async Python client for MyDot.one. Install with: pip install aiodot"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiodot",
    version="1.2.0",
    author="karbaladev.ir",
    author_email="karbaladev.ir@gmail.com",
    description="Async Python client for MyDot.one social platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karbaladevir/aiodot",
    project_urls={
        "Website": "https://karbaladev.ir",
        "Documentation": "https://samon-fs.github.io/aiodot-docsweb/",
        "Source": "https://github.com/karbaladevir/aiodot",
        "Issues": "https://github.com/karbaladevir/aiodot/issues",
        "License": "https://github.com/karbaladevir/aiodot/blob/main/LICENSE",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
    ],
    keywords="mydot, aiodot, mydot-bot, social-media, async, bot, user-bot",
)