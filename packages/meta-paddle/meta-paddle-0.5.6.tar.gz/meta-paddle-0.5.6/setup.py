from setuptools import setup, find_packages

requirements = [
    'setuptools',
    'opencv-python',
    'yaml',
    'pyyaml',
    'numpy',
    'pillow',
    'scipy'
]

__version__ = 'V0.05.06'

setup(
    name='meta-paddle',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/cvpaddle',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Meta Paddle Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
