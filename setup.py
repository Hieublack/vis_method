from setuptools import setup, find_packages


#setting up

setup(
    name= "vis_method",
    version= "2.8.2",
    author= "Hieu_black",
    author_email= "tranxuanhieuhust@gmail.com",
    description= "method of VIS",
    long_description_content_type= "text/markdown",
    packages= find_packages(), 
    install_requires= ['pandas', 'numpy'],
    keywords= ['vis'],
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)













