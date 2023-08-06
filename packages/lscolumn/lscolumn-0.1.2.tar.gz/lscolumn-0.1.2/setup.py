import setuptools


with open('README.md') as infile:
    readme = infile.read()


setuptools.setup(
    name='lscolumn',
    description=('Print a list of strings in columns like in `ls`.'),
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/kkew3/lscolumn',
    version='0.1.2',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.3',
    author='Kaiwen Wu',
    author_email='kps6326@hotmail.com',
    package_dir={'': 'src'},
    py_modules=['lscolumn'],
    install_requires=[
        'cjkjust>=0.1.4',
    ],
)
