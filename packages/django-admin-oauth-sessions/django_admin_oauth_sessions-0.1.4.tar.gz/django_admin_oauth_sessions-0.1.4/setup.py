#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Django >= 3.1',
                'django-allauth ~= 0.45.0']

test_requirements = [ ]
setup_requirments = ['setuptools >= 40.8']

setup(
    author="Samyak Jain",
    author_email='samyak.jain@agrevolution.in',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A django Project for custom authentication for sso tokens",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='django_admin_oauth_sessions',
    name='django_admin_oauth_sessions',
    packages=find_packages(include=['django_admin_oauth_sessions', 'django_admin_oauth_sessions.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/samyakjain224/django_admin_oauth_sessions',
    version='0.1.4',
    zip_safe=False,
    setup_requires=setup_requirments

)
