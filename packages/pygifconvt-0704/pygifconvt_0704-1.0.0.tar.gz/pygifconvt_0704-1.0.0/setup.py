from setuptools import setup, find_packages

setup(
    name             = 'pygifconvt_0704',
    version          = '1.0.0',
    description      = 'Test package for distribution',
    author           = 'jungwooLEE',
    author_email     = 'skyj7126@gmail.com',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['GIFCONVERTER', 'gifconverter'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 