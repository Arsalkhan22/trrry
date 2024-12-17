from setuptools import setup, find_packages

setup(
    name="staticwordpress",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "pyyaml",
        "requests",
        "beautifulsoup4",
        "lxml",
        "GitPython",
        "PyGithub",
        "PyYAML",
    ],
    python_requires=">=3.8",
)