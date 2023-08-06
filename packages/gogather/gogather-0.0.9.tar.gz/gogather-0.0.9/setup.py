from setuptools import setup, find_packages
  
# with open("requirements.txt", "r", encoding="utf-8") as f:
#    requirements = f.readlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
        name ='gogather',
        version ='0.0.9',
        author ='Rajiv Gupta',
        author_email ='rgupta@gene.com',
        url ='https://github.com/rantlabs/rant',
        description ='GatherDB - Go Forth and Gather',
        long_description=long_description,
        long_description_content_type ='text/markdown',
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'gather = src.gather:main'
            ]
        },
        classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords ='Very Fast Configuration Management and State Database',
        install_requires = ['netmiko','atpbar'],
#       install_requires = requirements,
        python_requires='>=3.6',
        zip_safe = False
)
