from setuptools import setup, find_packages

setup(
    name='jupyterhub-aks-util',
    version='0.1',
    license='MIT',
    author="Lucas Crownover",
    author_email='lcrownover127@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/lcrownover/jupyterhub-aks-util',
    keywords='jupyterhub aks utilities',
    install_requires=[
          'requests',
      ],

)
