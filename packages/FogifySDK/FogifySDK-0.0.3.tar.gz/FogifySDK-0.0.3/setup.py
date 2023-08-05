import setuptools
import os
filepath = os.path.dirname(os.path.realpath(__file__))
requirementPath = f'{filepath}/requirements.txt'
with open("README.md", "r") as fh:
    long_description = fh.read()

reqs = []

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        reqs = f.read().strip().split('\n')

setuptools.setup(
    name="FogifySDK",
    version="0.0.3",
    author="Moysis Symeonides",
    author_email="symeonidis.moysis@cs.ucy.ac.cy",
    description="The fogify's SDK library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={'': 'src'},  # Optional
    python_requires='>=3.5',
    install_requires=reqs
)
