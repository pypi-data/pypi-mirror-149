import io
import os

from setuptools import setup, find_packages


__version__ = None
with open("smtpcom/version.py") as f:
    exec(f.read())

dir_path = os.path.abspath(os.path.dirname(__file__))
readme = io.open(os.path.join(dir_path, 'README.md'), encoding='utf-8').read()


setup(
    name="smtpcom",
    version=str(__version__),
    packages=find_packages(exclude=["temp*.py", "test"]),
    url="https://github.com/smtpcom/smtpcom-python",
    license="MIT",
    include_package_data=True,
    author="Ruslan Khomenko",
    author_email="support@smtp.com",
    description="Smtp.com library for Python",
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
