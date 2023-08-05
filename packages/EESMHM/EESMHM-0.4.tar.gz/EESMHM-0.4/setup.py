from distutils.command.sdist import sdist as sdist_orig
from distutils.errors import DistutilsExecError

from setuptools import setup

class sdist(sdist_orig):

    def run(self):
        try:
            self.spawn(['./evoef_dowload.sh'])
        except DistutilsExecError:
            self.warn('listing directory failed')
        super().run()


if __name__ == '__main__':
    with open("ReadME_pypi.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(name='EESMHM',
        version="0.4",
        cmdclass={
        'sdist': sdist
        },
        description="Energy Evaluation of Single Mutant Homology Models",
        url='https://github.com/eved1018/EESMHM',
        author='Evan Edelstein',
        author_email='edelsteinevan@gmail.com',
        license='MIT',
        packages=['EESMHM'],
        data_files = [('', ['setup.py',"ReadME_pypi.md"])],
        install_requires=[
            'scipy',
            'numpy',
            "halo",
            "pandas",
            'intercaat',
            'pyhull'],
        long_description=long_description,
        long_description_content_type='text/markdown',
        entry_points = {
            'console_scripts': ['EESMHM=EESMHM.main:EESMHM'],
        })

#python setup.py sdist
#python3 -m twine upload dist/*
