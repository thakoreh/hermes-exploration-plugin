"""Include the canonical repository registry in built Python distributions."""

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWithRegistry(build_py):
    def run(self):
        super().run()
        target = Path(self.build_lib) / "hermes_exploration" / "registry.json"
        self.copy_file("registry.json", str(target))


setup(cmdclass={"build_py": BuildWithRegistry})
