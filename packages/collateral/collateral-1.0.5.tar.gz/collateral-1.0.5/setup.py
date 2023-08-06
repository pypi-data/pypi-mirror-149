import setuptools
import collateral

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "collateral",
    version = collateral.__version__,
    author = "Bruno Guillon",
    author_email = "bruno.guillon@uca.fr",
    url = "https://gitlab.limos.fr/brguillo/collateral",
    description = "parallel object manipulation",
    keyword = "parallel, manipulation, development, tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="MIT License",
    platforms=['any'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ],
    #python_requires=???
)

