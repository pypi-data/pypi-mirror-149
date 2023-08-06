from setuptools import find_packages, setup
setup(
    name = 'actelink-variables',
    packages=find_packages(include=['actelink']),
    license='LICENSE.txt',
    install_requires=['requests']
)