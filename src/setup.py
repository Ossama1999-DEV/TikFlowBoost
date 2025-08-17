from setuptools import setup, find_packages 

setup(
    name="TikFlowBoost",
    version="0.1.0",
    description="Web boost tube",
    author="DBBIH Oussama",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "click",
        "openpyxl",
        "pytube",
        "yt-dlp"
    ],
    python_requires=">=3.7",
)
