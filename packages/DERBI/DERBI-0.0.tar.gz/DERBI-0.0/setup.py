import setuptools

with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()

setuptools.setup(
    name='DERBI',
    version=0.0,
    author='Max Schmaltz',
    author_email='schmaltzmax@gmail.com',
    description='A simple rule-based automatic inflection model for German',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: German',
        'Programming Language :: Python :: 3',
        '',
        ''
    ],
    url='https://github.com/maxschmaltz/DERBI',
    license='Apache License, Version 2.0',
    install_requires=[
        'GitPython',
        'numpy',
        'spacy',
        'tqdm'
        ]
)