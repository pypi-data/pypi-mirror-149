from setuptools import find_packages, setup
setup(
    name='engine-function-extension',
    version='1.0.0',
    author='Jun Tu',
    author_email='jun@openlearning.com',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description='Python Worker Extension',
    include_package_data=True,
    long_description=open('readme.md').read(),
    install_requires=[
        'azure-functions >= 1.7.0, < 2.0.0',
        'python_hosts == 1.0.3'
        # Any additional packages that will be used in your extension
    ],
    extras_require={},
    license='MIT',
    packages=find_packages(where='.'),
    url='https://github.com/jarvinia',
    zip_safe=False,
)
