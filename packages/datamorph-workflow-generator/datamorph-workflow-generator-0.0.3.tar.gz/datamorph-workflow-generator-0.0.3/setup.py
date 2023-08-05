# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command

VERSION = '0.0.3'
DESCRIPTION = 'DataMorph Workflow Package'
LONG_DESCRIPTION = 'DataMorph Airflow DAG generator using JSON configuration file.'
REQUIRES_PYTHON = ">=3.6.0"

about = {"__version__": VERSION}
here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()

# Setting up
setup(
    name="datamorph-workflow-generator",
    version=VERSION,
    author="Annapurna Annadatha",
    author_email="sowmya@kwartile.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    install_requires=[], # add any additional packages that
    # needs to be installed along with your package.

    keywords=['python', 'datamorph', 'workflow', 'airflow'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
