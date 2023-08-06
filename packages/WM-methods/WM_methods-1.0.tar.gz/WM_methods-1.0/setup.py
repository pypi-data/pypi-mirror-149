from setuptools import setup, find_packages


setup(
    name='WM_methods',
    version='1.0',
    license='UNSW',
    author="Taimoor Sohail",
    author_email='taimoorsohail@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/txs156/WM_Methods',
    keywords='WM_Methods',
    install_requires=[
          'cvxpy', 'numpy', 'matplotlib', 'tqdm','xarray','xesmf', 'warnings'
      ],

)
