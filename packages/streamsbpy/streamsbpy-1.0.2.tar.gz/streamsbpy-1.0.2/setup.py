import setuptools

setuptools.setup(
    name="streamsbpy",
    version="1.0.2",
    author="code_xed",
    author_email="prernanayak001@gmail.com",
    description="An unoffcial API wrapper for streamsb.com",
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",
    url="https://github.com/code_xed/streamsbpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'requests'
    ],
)
