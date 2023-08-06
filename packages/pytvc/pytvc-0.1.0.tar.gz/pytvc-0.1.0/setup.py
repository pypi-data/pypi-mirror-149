import setuptools

setuptools.setup(
    name="pytvc",
    version="0.1.0",
    description="Python simulation tool for TVC",
    author="ZegesMenden",
    packages=["pytvc"],
    scripts=["pytvc/control.py", "pytvc/simulation.py", "pytvc/data.py", "pytvc/physics.py"]
)