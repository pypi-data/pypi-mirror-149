import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements/prod_lib.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="mylassi-xyz",  # Replace with your own username
    version="0.25.6",
    author="Christoph Laßmann",
    author_email="csharplassi@posteo.de",
    description="API for https://api.mylassi.xyz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mylassi.xyz",
    packages=[
        'mylassi_xyz_lib',
        'mylassi_xyz_lib/schemas',
        'mylassi_xyz_lib/services'
    ],
    package_dir={'': 'src'},
    install_requires=required,
    entry_points={
        'console_scripts': [],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
