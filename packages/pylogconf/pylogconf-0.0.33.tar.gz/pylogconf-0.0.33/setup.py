import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pylogconf",
    version="0.0.33",
    packages=[
        'pylogconf',
    ],
    # from here all is optional
    description="correctly configure python logging",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'python',
        'logging',
        'configuration',
        'easy',
        'yaml',
        'json',
        'debug',
    ],
    url="https://veltzer.github.io/pylogconf",
    download_url="https://github.com/veltzer/pylogconf",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'pyfakeuse',
        'logging_tree',
        'pyyaml',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
    ]},
    python_requires=">=3.9",
)
