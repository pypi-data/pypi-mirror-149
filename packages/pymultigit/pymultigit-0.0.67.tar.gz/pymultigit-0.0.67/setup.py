import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pymultigit",
    version="0.0.67",
    packages=[
        'pymultigit',
    ],
    # from here all is optional
    description="Help you deal with multiple git repositories",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'git',
        'python',
        'repositories',
        'multiple',
    ],
    url="https://veltzer.github.io/pymultigit",
    download_url="https://github.com/veltzer/pymultigit",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'gitpython',
        'pyfakeuse',
        'pytconf',
        'pylogconf',
        'venv-run',
    ],
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
        'pymultigit=pymultigit.main:main',
    ]},
    python_requires=">=3.10",
)
