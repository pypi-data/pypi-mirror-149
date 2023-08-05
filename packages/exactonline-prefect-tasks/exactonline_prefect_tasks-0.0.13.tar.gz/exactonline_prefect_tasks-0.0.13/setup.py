from setuptools import find_packages, setup

import versioneer

with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name='exactonline_prefect_tasks',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/aporacloudmobile/exactonline_prefect_tasks',
    license='',
    author='Carlos Paiva',
    author_email='carlospaiva87@gmail.com',
    description="",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,

)
