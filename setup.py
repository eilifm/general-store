from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()


setup(
    name='general-store',
    packages=['generalstore'],
    include_package_data=True,
    install_requires=install_requires,
)