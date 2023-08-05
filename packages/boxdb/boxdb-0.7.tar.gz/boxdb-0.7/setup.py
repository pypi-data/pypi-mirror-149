import setuptools

from filemod import reader


classifiers=[
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"
]
setuptools.setup(
    name="boxdb",
    version="0.7",
    author="kshitij jathar",
    author_email="kshitijjathar7@gmail.com",
    description="Make Your own personal database liter than others",
    long_description=reader('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/kshitij1235/boxdb",
    project_urls={
        "Bug Tracker": "https://github.com/kshitij1235/boxdb/issues",
    },
    license='MIT',
    classifiers=classifiers,
    keywords='database',
    packages=setuptools.find_packages(),
    install_requires=['tabulate','filemod']

)