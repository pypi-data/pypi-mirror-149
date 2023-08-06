""" ./setup.py """
import setuptools

setuptools.setup(
    name='Automancy',
    version='0.5.9',
    author='Jonathan Craig',
    author_email='blurr@iamtheblurr.com',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf8').read(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Internet :: WWW/HTTP :: Browsers'
    ],
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    url='https://github.com/iamtheblurr/automancy',
    license='MIT',
    install_requires=[
        'chronomancy',
        'lxml',
        'pytest',
        'selenium',
        'webvtt-py',
    ],
)
