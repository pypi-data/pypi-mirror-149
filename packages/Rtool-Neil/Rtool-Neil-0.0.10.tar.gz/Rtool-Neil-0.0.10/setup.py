import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rtool-Neil",
    version="0.0.10",
    author="Jianhong Gao",
    author_email="772962760@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
#python setup.py sdist bdist_wheel
# twine upload  -u JianhongGao -p  Gjh12345@  dist/*
#如果你更新了代码，记得更新setup.py中的版本号，重新构建你的代码，再次上传就好了。