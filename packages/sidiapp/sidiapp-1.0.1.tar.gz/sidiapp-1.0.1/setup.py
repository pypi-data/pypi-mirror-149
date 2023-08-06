import setuptools




long_description = ''
requirements = ''

# with open('desc.txt', 'r') as desc_file:
#     long_description = desc_file.read()

# with open('req.txt', 'r') as req_file:
#     requirements = req_file.read()

setuptools.setup(
    name='sidiapp',
    version='1.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sd',
    author_email='sd@gmail.com',
    url="https://github.com/",
    packages=setuptools.find_packages(),
    include_package_data = True,
    entry_points={
        'console_scripts':['sidiappexec=sidilib:run'] 
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.7'
    ],
    keywords="Convert, Arabic, Image, Text",
    license="MIT",
    install_requires=requirements,
    python_requires='>=3.7',


)


#-----create wheel
#run: python setup.py bdist_wheel

#-----create package on pypi
#python stup.py sdist
#twine upload dist/*
#username= __token__
#password= ......................