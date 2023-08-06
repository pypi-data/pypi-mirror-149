from setuptools import setup, find_packages
from pathlib import Path


def read_requirements(filename):
    path = Path(__file__).parent / "requirements"
    with (path / filename).open("r") as f:
        return tuple(line.strip() for line in f if line.strip())


publish_requirements = read_requirements("publish_requirements.txt")
test_requirements = read_requirements("test_requirements.txt")
doc_requirements = read_requirements("doc_requirements.txt")
dev_requirements = read_requirements("dev_requirements.txt")

EXTRAS_REQUIRE = {
    "dev": dev_requirements,
    "publish": publish_requirements,
    "test": test_requirements,
    "doc": doc_requirements,
}

EXTRAS_REQUIRE["all"] = set(value for tup in EXTRAS_REQUIRE.values() for value in tup)

setup(
    packages=find_packages(include=["clease_gui", "clease_gui.*"]),
    extras_require=EXTRAS_REQUIRE,
)
