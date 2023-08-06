from setuptools import setup
setup(
    name='APIConnect',
    packages=['EdelweissAPIConnect'],
    version='1.0.2',
    license='MIT',
    description='APIs to trade from Edelweiss',
    author='Edelweiss',
    author_email='support@edelweissfin.com',
    url='https://www.edelweiss.in/',
    download_url='https://www.edelweiss.in/ewwebimages/webfiles/download/Python_APIConnect/APIConnect-1.0.2.tar.gz', # change url as per new build location
    keywords=['Edelweiss', 'Open API', 'Trade', 'Edelweiss Python Library'],
    python_requires=">=3.7",
    install_requires=[
        'urllib3>=1.26.6',
        'requests>=2.26.0'
        ],
    data_files=[('conf',['conf/settings.ini'])],
    license_files = ['LICENSE.txt',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
    ],
)