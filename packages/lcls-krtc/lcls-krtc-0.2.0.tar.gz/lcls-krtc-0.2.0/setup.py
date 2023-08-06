from setuptools import setup

import versioneer

with open('requirements.txt') as f:
    requirements = f.read().split()

setup(
    name="lcls-krtc",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=(
        "A small utility class for using Kerberos authentication with "
        "Python requests"
    ),
    url="https://github.com/pcdshub/krtc.git",
    author="Murali Shankar",
    author_email="mshankar@slac.stanford.edu",
    license="MIT",
    packages=["krtc"],
    install_requires=requirements,
    zip_safe=False,
)
