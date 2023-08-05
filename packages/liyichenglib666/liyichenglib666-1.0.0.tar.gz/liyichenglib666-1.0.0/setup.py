from setuptools import setup

def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()

setup(
    name="liyichenglib666",
    version="1.0.0",
    description="this is a test lib for study",
    packages=["liyichenglib"],
    py_modules=["tools"],
    author="liyicheng",
    author_email="leeyc7@foxmail.com",
    long_description=readme_file(),
    url="https://www.baidu.com",
    license="MIT"
)