try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='alphaneural',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.0.5',
    description='A package for predicting buy and sell signals based on alphaneural for quants',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=58.1.0",
    	"wheel>=0.37.1",
    	"pandas>=1.4.2",
        "fire"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/alphaneural/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
