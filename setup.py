from setuptools import setup

setup(
    name="hoshiri",
    version="0.1",
    py_modules=["hoshiri"],
    install_requires=[
        "anthropic",
        "python-dotenv",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hoshiri=hoshiri:main",
        ],
    },
)
