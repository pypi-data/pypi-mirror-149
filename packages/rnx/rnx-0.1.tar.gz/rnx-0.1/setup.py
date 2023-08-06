from setuptools import setup, find_packages

setup(
    name='rnx',
    version='0.1',
    license='MIT',
    author="David Woodburn",
    author_email="david.woodburn@icloud.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://gitlab.com/davidwoodburn/rnx",
    keywords="RINEX",
    install_requires=["numpy"],
)
