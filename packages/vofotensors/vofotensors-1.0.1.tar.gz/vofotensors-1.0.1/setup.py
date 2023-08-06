import setuptools

setuptools.setup(
    name="vofotensors",
    version="1.0.1",
    author="Julian Karl Bauer",
    author_email="juliankarlbauer@gmx.de",
    description="V(ariety)O(f)F(iber)O(rientation)TENSORS "
    "contains selected contributions of "
    "Bauer JK, Böhlke T. Variety of fiber orientation tensors. "
    "Mathematics and Mechanics of Solids. December 2021. "
    "doi:10.1177/10812865211057602",
    url="https://github.com/JulianKarlBauer/fiber_orientation_tensors_2021",
    packages=["vofotensors"],
    package_dir={"vofotensors": "vofotensors"},
    install_requires=[
        "numpy",
        "sympy",
        "pandas",  # Required for example s003...
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
