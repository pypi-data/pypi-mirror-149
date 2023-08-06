from setuptools import setup
from setuptools.command.install import install

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='aaei',
      version='1.2.0',
      description='Air Adverse Effect Index',
      long_description=long_description,
      long_description_content_type="text/markdown",
      include_package_data=True,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education'
      ],
      keywords='trace gas compound toxicity read-across statistics health index',
      url='http://github.com/Kwabratseur/AAEI',
      author='Jeroen van \'t Ende',
      author_email='jeroen.vantende@outlook.com',
      license='MIT', # mit should be fine, looking at the deps.. only those BSD-3
      packages=['AAEI'],
      extras_require={
      'Viz': ['matplotlib', 'plotly', 'seaborn'] #BSD, #MIT, #MIT
      },
      install_requires=[
        'pandas', # BSD-3
        'numpy', # BSD-3
        'pivottablejs' # MIT license
      ],
      entry_points = {
        'console_scripts': ['AEI=AAEI.AAEI:main'],
      },
      zip_safe=False)
