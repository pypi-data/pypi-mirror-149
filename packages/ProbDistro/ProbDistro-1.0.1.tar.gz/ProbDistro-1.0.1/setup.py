from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

packages = find_packages(where=".")

if "tests" in packages:
    packages.remove("tests")

setup(
    name='ProbDistro',
    version='1.0.1',
    packages=['ProbDistro', 'ProbDistro.discrete_distributions', 'ProbDistro.continuous_distributions'],
    url='https://github.com/CPSuperstore/ProbDistro',
    license='MIT',
    author='Christopher',
    author_email='cpsuperstoreinc@gmail.com',
    description='A Python package for handeling various continous and discrete randcom variables, including normal/gauss, binomial, poisson, and more',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/CPSuperstore/ProbDistro/issues",
        "Documentation": "https://github.com/CPSuperstore/ProbDistro"
    },
    keywords=[
        'PROBABILITY', 'DISTRIBUTION', 'NORMAL', 'UNIFORM', 'GAUSS', 'POISSON', 'BINOMIAL', 'BERNOULLI', 'GEOMETRIC',
        'HYPERGEOMETRIC'
    ],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ]
)
