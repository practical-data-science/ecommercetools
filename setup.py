from setuptools import setup
from setuptools import find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ecommercetools',
    packages=find_namespace_packages(include=['ecommercetools.*']),
    version='0.36',
    license='MIT',
    description='EcommerceTools is a data science toolkit for ecommerce, marketing science, and technical SEO.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matt Clarke',
    author_email='matt@practicaldatascience.co.uk',
    url='https://github.com/practical-data-science/ecommercetools',
    download_url='https://github.com/practical-data-science/ecommercetools/archive/master.zip',
    keywords=['ecommerce', 'marketing', 'seo', 'seo testing', 'customers', 'products', 'rfm', 'abc',
              'operations', 'analytics', 'python', 'pandas', 'nlp', 'causal impact'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['pandas',
                      'gapandas',
                      'sklearn',
                      'requests',
                      'requests_html',
                      'httplib2 >= 0.15.0',
                      'lifetimes',
                      'transformers',
                      'torch',
                      'pycausalimpact',
                      'numpy']
)
