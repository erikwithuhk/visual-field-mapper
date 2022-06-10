from importlib.metadata import entry_points
from setuptools import setup

test_requirements = ["faker>=13.13.0", "pytest>=7.1.2"]

dev_requirements = [*test_requirements, "black>=22.3.0"]

requirements = ["colorama>=0.4.4"]

extra_requirements = {"dev": dev_requirements}

setup(
    name="visual-field-mapper",
    version="0.1",
    description="",
    url="https://github.com/erikwithuhk/visual-field-mapper",
    author="Erik Jönsson",
    author_email="efjonsson@gmail.com",
    license="BSD-3-Clause",
    packages=["visual_field_mapper"],
    install_requires=requirements,
    extras_require=extra_requirements,
    zip_safe=False,
)
