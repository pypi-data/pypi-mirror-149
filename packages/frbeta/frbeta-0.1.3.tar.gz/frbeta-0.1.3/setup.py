from setuptools import find_packages, setup
setup(
    name='frbeta',
    packages=find_packages(),
    version='0.1.3',
    description='return in a fraction format',
    author='resdon',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
    url = 'https://pypi.org/project/frbeta/0.1.3/#files'
)