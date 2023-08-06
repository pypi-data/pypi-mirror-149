from setuptools import find_packages, setup


def load_requirements(filename):
    with open(filename) as fd:
        return fd.readlines()


requirements = load_requirements("requirements.txt")
test_requirements = load_requirements("requirements-dev.txt")


setup(
    name="datappkit",
    description="datapp team kit wrapper library",
    version="0.0.5",
    author="datapp",
    author_email="baojiarui@megvii.com",
    url="https://git-core.megvii-inc.com/brain/label/infrastructure/data-service-sdk",
    packages=find_packages(exclude=("tests")),
    classifiers=[
        "License :: Other/Proprietary License",
    ],
    tests_require=test_requirements,
    install_requires=requirements,
    python_requires=">=3.5",
)
