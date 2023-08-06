import setuptools
from os.path import join

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ampscz_anonymize_dicom", # Replace with your own username
    version="0.0.1",
    author="Kevin Cho",
    author_email="kevincho@bwh.harvard.edu",
    description="AMP-SCZ Dicom anonymizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AMP-SCZ/ampscz_anonymize_dicom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.7',
    install_requires=['tk>=0.1.0',
                      'pydicom>=2.1.2',
                      'tkinterdnd2>=0.3.0'],
    scripts=['scripts/ampscz_anonymize_dicom']
)


