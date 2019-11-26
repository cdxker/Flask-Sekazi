from setuptools import setup

setup(
    name='Flask-Sekazi',
    version='0.0.3',
    url='https://github.com/fastfists/Flask-Sekazi',
    license='MIT',
    author='Denzell Ford',
    author_email='fdenzell@gmail.com',
    description='Flask Template blocks with extra functionality',
    long_description=__doc__,
    py_modules=['flask_sekazi'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
