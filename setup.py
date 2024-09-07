from setuptools import setup

setup(
    name="markdown-img2fig",
    version="1.0.0",
    author="zetaloop",
    author_email="zetaloop@outlook.com",
    description="Convert markdown imgs into captioned <figure>s",
    keywords="markdown img figure caption",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zetaloop/markdown_img2fig",
    license="MIT",
    packages=["img2fig"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup :: HTML",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["Markdown>=3.0.1"],
    python_requires=">=3.8",
)
