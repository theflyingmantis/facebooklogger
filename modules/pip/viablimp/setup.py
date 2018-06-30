from setuptools import setup,find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='viablimp',
		version='0.2.5',
		description='logging messages by facebook bot to your account',
		long_description=readme(),
		url='https://facebooklogger.herokuapp.com/',
		author='Abhinav Rai',
		author_email='rai.1@iitj.ac.in',
		license='MIT',
		packages=['viablimp'],
		install_requires=[
		'requests'
		],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Intended Audience :: Education',
		'Intended Audience :: Information Technology',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Programming Language :: Python :: 2',
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: System :: Logging',
		],
		zip_safe=False)
