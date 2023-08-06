import re
import setuptools


# Grab the readme
try:
    with open("README.md", "r") as a:
        long_description = a.read()
except Exception:
    long_description = ""


# Here are the requirements
requirements = [
    "aiohttp",
]


# Here are some MORE requirements
extras = {
    "docs": [
        "sphinx",
        "sphinx_rtd_theme",
    ]
}


# Let's get the version
version = None
regex = re.compile(r"""["']((?:[\d.]+)(?:a|b)?)["']""", re.MULTILINE)
with open("upgradechat/__init__.py") as a:
    text = a.read()
version = regex.search(text).group(1)


setuptools.setup(
    name="upgradechatpy",
    version=version,
    author="Kae Bartlett",
    author_email="kae@voxelfox.co.uk",
    description="A wrapper around Upgrade.Chat's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Voxel-Fox-Ltd/UpgradeChat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require=extras,
)
