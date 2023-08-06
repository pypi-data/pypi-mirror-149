from setuptools import setup

if __name__ == '__main__':
    with open("ReadMe_pypi.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(name='pericaat',
        version="0.9",
        description="The Interface Extension program was developed to identify pharmacologically relevant residues at the periphery of a protein’s interface from a known three-dimensional structure",
        url='https://github.com/eved1018/InterfaceExtension',
        author='Evan Edelstein',
        author_email='edelsteinevan@gmail.com',
        license='MIT',
        packages=['pericaat'],
        data_files = [('', ['ReadMe.md', 'setup.py',"ReadMe_pypi.md"])],
        install_requires=[
            'scipy',
            'numpy',
            'intercaat',
            'pyhull'],
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points = {
            'console_scripts': ['pericaat=pericaat.main:pericaat'],
        })

#python setup.py sdist
#python3 -m twine upload dist/*
