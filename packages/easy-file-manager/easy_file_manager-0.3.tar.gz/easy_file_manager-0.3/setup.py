import setuptools

with open('README.md', 'r') as fh:
    long_desc = fh.read()

setuptools.setup(
    name='easy_file_manager',
    version='0.3',
    author='Lukas Stockmann',
    author_email='g.lstuma@gmail.com',
    description='Package to easily let a user select multiple files for further use',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/lstuma/easy_file_selector',
    packages=setuptools.find_packages(),
    install_requires=['setuptools',
                      'tk',
                      'TCL'
                      ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'easy_file_manager=easy_file_manager.easy_file_manager:main',
        ]
    }
)