import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drift_anomaly_evaluator",
    version="0.0.1",
    author="Bardh Prenkaj",
    author_email="prenkaj@di.uniroma1.it",
    description="An initial evaluation of drift anomaly detection models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://iim.di.uniroma1.it/index.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy'
        'shapely'
    ],
    keywords='drift anomaly detection evaluation precision recall',
    project_urls={
        'Homepage': 'http://iim.di.uniroma1.it/index.html',
    }
)