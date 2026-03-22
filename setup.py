from setuptools import setup, find_packages

setup(
    name="olympic-data-analysis",
    version="1.0.0",
    author="Your Name",
    description="120 Years of Olympic History — Data Analysis",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
    ],
)
