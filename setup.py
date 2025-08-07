from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name='androidHustle',
    version='0.1.0',
    author='Aditya Blotra',
    author_email='mr.balotra4@gmail.com',
    description='Automate interaction with Android devices using ADB.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aditya7balotra/androidHustle',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.12,<3.14',
    entry_points={
        'console_scripts': [
            'ahustle=androidHustle.cli:cli',
        ],
    },
)
