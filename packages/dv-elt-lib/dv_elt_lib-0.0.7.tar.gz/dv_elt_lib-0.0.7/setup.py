#!/usr/bin/env python
from setuptools import find_namespace_packages, setup

package_name = "dv_elt_lib"
package_version = "0.0.7"
description = """Python lib to work with databases Greenplum and Clickhouse"""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=description,
    author='Mark Poroshin',
    author_email='mark.poroshin@yandex.ru',
    packages=find_namespace_packages(include=['dv_elt_lib']),
    url="https://gitlab.com/dv_group/dv_elt_lib",
    include_package_data=True,
    install_requires=[
        "dvgroup-factory>=0.0.50",
        "pandas"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
)
