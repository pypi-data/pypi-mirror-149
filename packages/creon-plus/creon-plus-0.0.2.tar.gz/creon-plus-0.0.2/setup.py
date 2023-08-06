from setuptools import setup, find_packages

setup(
    name                          = 'creon-plus',
    version                       = '0.0.2',
    description                   = '대신증권 Creon Plus API',
    long_description              = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    author                        = 'jihogrammer',
    author_email                  = 'jihogrammer@gmail.com',
    license                       = 'MIT',
    packages                      = find_packages(),
    install_requires              = ['pywin32'],
    classifiers                   = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
)
