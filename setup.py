from setuptools import setup

setup(
    name='pandas_emetrics',
    version='0.1.0.dev1',
    description='A Python package integrating ethical considerations into Pandas DataFrame processing.',
    author='Noah Kasica',
    author_email='nkasica21@gmail.com',
    url='https://github.com/nkasica/pandas-emetrics',
    packages=[
        'pandas_emetrics',
        'pandas_emetrics.metrics',
        'pandas_emetrics.processing'
    ],
    keywords=['data science', 'ethics', 'pandas', 'python3'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License'
    ],
    license='MIT',
    install_requires=['pandas', 'numpy']
)