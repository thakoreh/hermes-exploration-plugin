"""Include the canonical repository registry in built Python distributions."""

from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildWithRegistry(build_py):
    def run(self):
        super().run()
        if getattr(self, "editable_mode", False):
            # Editable installs read the canonical registry beside the source.
            return
        target = Path(self.build_lib) / "hermes_exploration" / "registry.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        self.copy_file("registry.json", str(target))


setup(cmdclass={"build_py": BuildWithRegistry})
