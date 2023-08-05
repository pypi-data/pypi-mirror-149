from setuptools import setup, find_namespace_packages
import os


current = os.path.abspath(os.path.dirname(__file__))
os.chdir(current)


about = {}
with open(os.path.join(current, 'radware', 'alteon', '__init__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

with open('sdk_requirements.txt') as fh:
    required = [x for x in fh.read().splitlines() if not x.startswith('#')]

with open('alteon_software.txt', 'w') as f:
    f.write('#Supported Alteon Versions:')
    for ver in about['__minimum_supported_version__']:
        f.write('\n>={0}'.format(ver))
    f.close()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=['radware.*']),
    install_requires=required,
    url=about['__url__'],
    keywords=['radware', 'sdk', 'api', 'configurators', 'beans'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    python_requires='~=3.6',
    data_files=[('.', ['sdk_requirements.txt'])],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers'
    ]
)

