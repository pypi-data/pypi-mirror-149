from setuptools import find_packages, setup

VERSION=0.1

setup(
    name="feng_libs",
    requires=[
    ],
    version=0.1,
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "fire", 
        "PyPDF2",
        "opencv-python"
    ],
    scripts=[],
    author="jim",
    author_email="zhengwenfeng37@gmail.com",
    url="https://github.com/tenqaz/feng_libs",
    license="jims Licence",
    description="自己写的工具库",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts':[
            'feng_libs=feng_libs.__main__:main'
        ]
    }
)
