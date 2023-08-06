import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scale_lidar_io_debug",
    version="0.1.52",
    author="Scale AI",
    author_email="rodrigo.belfiore@scale.com, ivan.roumec@scale.com",
    description="Lidar data conversion helpers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['scale_lidar_io_debug'],
    install_requires=[
        'scale-lidar-io',
        'scaleapi>=2.0.3',
        'pytest',
        'pymongo',
        'open3d',
        'cryptography',
        'requests',
        'awscli',
        'smart_open',
        'boto3',
        'dataclasses',
        'laspy',
        'matplotlib',
        'numpy',
        'opencv-python',
        'open3d',
        'pandas',
        'Pillow',
        'PyYAML',
        'transforms3d',
        'ujson',
        'pyquaternion',
        'pyntcloud',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
