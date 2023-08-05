from setuptools import setup, find_packages

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

packages = find_packages(where="src")
for p in packages:
    print(f"Found {p}")

setup(
    name="wolfpackutil",
    version="0.1.5",
    author="Kalka",
    author_email="kalka2088@gmail.com",
    description="Python util library for WolfpackMC packages. https://github.com/WolfpackMC",
    url="https://github.com/WolfpackMC/wolfpackutil",
    project_urls={
        "Bug Tracker": "https://github.com/WolfpackMC/wolfpackutil/issues",
    },
    package_dir={"": "src"},
    packages=packages,
    python_requires=">=3.10",
    install_requires=[
        "owoify-py",
        "pyfiglet",
        "python-dateutil",
        "rich",
        "tinydb"
    ]
)
