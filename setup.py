from setuptools import find_packages, setup

import versioneer

with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="act_dr6_mflike",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="ACT DR6 multi-frequency likelihood for cobaya",
    long_description=readme,
    long_description_content_type="text/x-rst",
    zip_safe=True,
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "mflike>=0.8.2",
    ],
    package_data={"act_dr6_mflike": ["*.yaml"]},
)
