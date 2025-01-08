from setuptools import find_packages, setup


# Read requirements files
def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Project metadata
PROJECT_NAME = "password-cli"
VERSION = "0.1.0"
AUTHOR = "Umut Topalak"
AUTHOR_EMAIL = "umuttopalak@hotmail.com"
DESCRIPTION = "A secure command-line password manager with sudo authentication"
GITHUB_URL = "https://github.com/umuttopalak/pass-cli"

# Dependencies
INSTALL_REQUIRES = read_requirements("requirements.txt")
EXTRAS_REQUIRE = {
    "dev": read_requirements("requirements-dev.txt"),
}

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={
        "Bug Tracker": f"{GITHUB_URL}/issues",
        "Documentation": f"{GITHUB_URL}#readme",
        "Source Code": GITHUB_URL,
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "pass-cli=pass_cli.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "password-manager",
        "security",
        "cryptography",
        "cli",
        "command-line",
        "sudo",
    ],
)
