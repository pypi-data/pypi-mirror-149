import setuptools

setuptools.setup(
    name="pytvc",
    version="0.1.2",
    description="Python simulation tool for TVC",
    author="ZegesMenden",
    packages=["pytvc"],
    scripts=["pytvc/control.py", "pytvc/core.py", "pytvc/data.py", "pytvc/physics.py"],
    include_package_data=True
)