from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyframes",
    version='0.0.13',
    author="Darryn Anton Jordan",
    author_email="<darryn@sensorit.io>",
    description='Python interface for the frames.ai database.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'pillow', 'requests'],
    keywords=['python', 'frames.ai', 'sensorit'],
    url="https://github.com/Sensoritio/pyframes",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
