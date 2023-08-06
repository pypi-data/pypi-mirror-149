from pathlib import Path

from setuptools import find_packages, setup

setup(
    name='SmartParams',
    version='0.16.0',
    author='Mateusz Baran',
    author_email='mateusz.baran.sanok@gmail.com',
    maintainer='Mateusz Baran',
    maintainer_email='mateusz.baran.sanok@gmail.com',
    license='MIT',
    url='https://gitlab.com/mateusz.baran/smartparams',
    description='The tool for advanced project configuration with python object injection.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'dvc>=2.10.1',
        'GitPython>=3.1.27',
        'PyYAML>=5.4.1',
        'typeguard>=2.13.3',
    ],
    extras_require=dict(
        dev=[
            'bump2version==1.0.1',
            'pytest==6.2.5',
            'pytest-black==0.3.12',
            'pytest-cov==3.0.0',
            'pytest-flakes==4.0.5',
            'pytest-isort==2.0.0',
            'pytest-mypy==0.9.0',
        ],
    ),
)
