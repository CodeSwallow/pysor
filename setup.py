from setuptools import setup, find_packages

setup(
    name="Pysor",
    version="0.1",
    packages=find_packages(),
    description="A Python package for sensor simulations",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CodeSwallow/pysor",
    author="Isai Ramirez",
    author_email="isai.ramirez.stamaria15@gmail.com",
    license="MIT",
    install_requires=[
        "paho-mqtt",
    ],
    extras_require={
        ':python_version<"3.11"': ['toml==0.10.2'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="mqtt sensor simulation",
    package_data={
        "sensor_simulation": ["*"],
    },
    python_requires=">=3.9, <4",
)
