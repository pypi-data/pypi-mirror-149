import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vkmini",
    version="0.3.2",
    author="Elchin Sarkarov",
    author_email="elchin751@gmail.com",
    description="VK API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elchinchel/vkmini",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['aiohttp>=3.6.2'],
    python_requires='>=3.6',
)
