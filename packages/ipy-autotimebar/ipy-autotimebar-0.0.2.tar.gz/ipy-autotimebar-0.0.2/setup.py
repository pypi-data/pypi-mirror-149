import io
from setuptools import setup


with io.open('README.md') as f:
    long_description = f.read()


setup(
    name='ipy-autotimebar',
    author='Alan Tetich',
    author_email='alan.tetich.project@gmail.com',
    description='Extend autotime to use in jupyter notebooks time bar per cell.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache',
    url='https://github.com/alien3211/ipy-autotimebar',
    use_scm_version={'write_to': 'autotimebar/_version.py'},
    setup_requires=['setuptools_scm'],
    install_requires=['ipython', 'ipywidgets', 'monotonic ; python_version < "3.3"'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
    ],
    packages=['autotimebar'],
)
