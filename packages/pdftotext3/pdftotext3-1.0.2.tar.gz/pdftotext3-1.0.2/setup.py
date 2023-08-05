import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdftotext3",
    version="1.0.2",
    author="Anish M",
    author_email="aneesh25861@gmail.com",
    description="Convert PDF Files to Text Files using Google's Tesseract OCR.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT LICENSE",
    keywords = ['student project'],
    url="https://github.com/Anish-M-code/pdftotext",
    packages=["pdftotext"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3',      
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
    ],
    entry_points={"console_scripts": ["pdftotext = pdftotext:main",],},
)
