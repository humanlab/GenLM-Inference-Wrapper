from setuptools import setup, find_packages

NAME = 'genlm_wrapper'
VERSION = '0.0'
AUTHOR = "Adithya V Ganesan, Gourab Dey, Yash Kumar Lal, Salvatore Giorgi, Vivek Kulkarni and H. Andrew Schwartz"
AUTHOR_EMAIL = "avirinchipur@cs.stonybrook.edu, has@cs.stonybrook.edu"
DESCRIPTION = "GenLM-Inference-Wrapper is a tool built on top of huggingface transformers to perform Inference using Generative Language Models. It is written in Python 3.8 and developed by the World Well-Being Project at the University of Pennsylvania and Stony Brook University."
LONG_DESCRIPTION=open("README.md", "r", encoding="utf-8").read()
LONG_DESCRIPTION_CONTENT_TYPE="text/markdown"
KEYWORDS="NLP deep learning transformers pytorch huggingface"
LICENSE="Apache License 2.0"
URL = "https://github.com/humanlab/GenLM-Inference-Wrapper"
DOWNLOAD_URL = 'https://github.com/humanlab/GenLM-Inference-Wrapper'

INSTALL_REQUIRES = ['transformers==4.31.0', 'numpy==1.22', 'safetensors==0.3.1', 'huggingface-hub==0.14.1', 'regex==2023.10.3', 'requests==2.31.0', 'packaging==20.9', 'filelock==3.13.1', 'PyYAML==5.1', 'typing-extensions>=3.7.4.3', 'fsspec==2023.12.1']
PACKAGES_DIR = {
  'genlm_inference': 'src/genlm_inference',
  'data_connector': 'src/data_connector',  
}
# PACKAGES_DIR = {"": "src"}
PACKAGES = find_packages(where="src")
PACKAGE_DATA = {"": ["**/*.cu", "**/*.cpp", "**/*.cuh", "**/*.h", "**/*.pyx", "**/*.json"]}
INCLUDE_PACKAGE_DATA = True
EXTRAS_REQUIRE = {
  'data_connector': ['pymysql==1.1.0', 'SQLAlchemy>=0.9.9,<=1.4.39'],
  'all': ['pymysql==1.1.0', 'SQLAlchemy>=0.9.9,<=1.4.39', 'tqdm==4.66.1'],
}
PYTHON_VERSION = ">=3.8"
CLASSIFIERS=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
SCRIPTS = ['mysql_interface.py']


if __name__ == "__main__":

  setup(name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        keywords=KEYWORDS,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        install_requires=INSTALL_REQUIRES,
        package_dir=PACKAGES_DIR,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        include_package_data=INCLUDE_PACKAGE_DATA,
        extras_require=EXTRAS_REQUIRE,
        python_requires=PYTHON_VERSION,
        classifiers=CLASSIFIERS,
        # scripts=SCRIPTS
  )