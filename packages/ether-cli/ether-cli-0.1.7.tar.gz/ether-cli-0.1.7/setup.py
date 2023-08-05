from setuptools import setup
import pathlib

file_path = pathlib.Path(__file__).parent.resolve()
readme = (file_path/"README.md").read_text()

setup(
  name="ether-cli",
  version="0.1.7",
  description="Minimalistic wallet CLI for Ethereum",
  long_description=readme,
  long_description_content_type="text/markdown",
  url="https://github.com/0xver/ether",
  author="Sam Larsen",
  license="MIT",
  packages=["ether"],
  entry_points = {
    "console_scripts": ["ether=ether.cli:main"],
  },
  install_requires=[
      "cryptography", "mnemonic", "hdwallet", "web3", "requests",
  ],
  python_requires=">=3.9"
)
