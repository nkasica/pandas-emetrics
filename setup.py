from setuptools import setup, find_packages

setup(
    name='pandas_emetrics',
    version='1.0.0',
    description='A Python package integrating ethical considerations into Pandas DataFrame processing.',
    author='Noah Kasica',
    author_email='nkasica21@gmail.com',
    url='https://github.com/nkasica/pandas-emetrics',
    packages=find_packages(),
    keywords=['data science', 'ethics', 'pandas', 'numpy', 'python3'],
    classifiers=[
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