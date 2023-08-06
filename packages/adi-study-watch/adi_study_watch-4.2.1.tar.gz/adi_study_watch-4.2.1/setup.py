import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adi_study_watch",
    version="4.2.1",
    author="Analog Devices, Inc.",
    author_email="healthcare-support@analog.com",
    license='Apache License, Version 2.0',
    description="ADI study watch python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/analogdevicesinc/study-watch-sdk",
    packages=["adi_study_watch",
              "adi_study_watch.core",
              "adi_study_watch.core.enums",
              "adi_study_watch.application",
              "adi_study_watch.core.packets",
              "adi_study_watch.core.data_types",
              "adi_study_watch.application.vsm_mb_sb",
              "adi_study_watch.application.study_watch",
              ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.6',
    install_requires=['pyserial==3.5', 'tqdm==4.61.0', 'libusb1==3.0.0'],
)
