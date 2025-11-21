from setuptools import setup, find_packages

setup(
    name="bjj-digital",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "fpdf2>=2.7.4", 
        "Pillow>=10.0.0",
        "qrcode>=7.4.2",
        "bcrypt>=4.0.1",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "plotly>=5.15.0",
        "streamlit-option-menu>=0.3.6",
    ],
    python_requires=">=3.8",
)
