from setuptools import setup, find_packages

setup(
    author="Yannis Kalfas",
    description="Functions and tools I have found useful through the years",
    name="pyanis",
    version="0.1.1",
    packages=find_packages(include=["pyanis", "pyanis.*"]),
    install_requires=['pandas','matplotlib','scikit-learn','scipy', 'numpy', 'opencv-contrib-python','tqdm'],
    python_requires='>=3.5',
)