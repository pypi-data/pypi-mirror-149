import setuptools

setuptools.setup(
    name='pysap_macro',
    version='0.1',
    author='Mateus Lima Silva',
    author_email='mateusls.personal@gmail.com',
    description='Library to run SAP scripts with Python',
    long_description=open('README.md').read(),
    long_description_type='text/markdown',
    url='https://github.com/teusinLS/sapy_script',
    packages=setuptools.find_packages(),
    install_requires=['pywin32==304', 'WMI==1.5.1'],
    keywords='SAP Script Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows 8',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python'
    ]
)