from setuptools import setup, find_packages

setup(
    name="pyxploitdb",
    version="1.0",
    description="An exploit-db.com python API using advanced search with all possible filters.",
    url="https://github.com/nicolasmf/pyxploit-db",
    author="Nicolas MF",
    author_email="nikolamf@hotmail.com",
    license="MIT",
    keywords="api exploit exploit-db",
    packages=find_packages(),
    install_requires=["rich"],
)
