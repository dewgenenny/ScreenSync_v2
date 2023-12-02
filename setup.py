from setuptools import setup, find_packages

setup(
    name='ScreenSync',  # Replace with your package name
    version='0.0.1',  # Initial version
    author='Tom George',  # Replace with your name
    author_email='tom@penberth.com',  # Replace with your email
    description='A Python tool for synchronizing screen colors with smart bulbs.',  # Short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dewgenenny/ScreenSync',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'screensync': ['assets/*']
    },
    install_requires=[
        'tinytuya>=1.2.0',
        'Pillow>=8.0.0',
        'paho-mqtt',
        'matplotlib',
        'mss',
        'platformdirs'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
    entry_points={  # Optional
        'console_scripts': [
            'screensync=screensync.ui:main',  # Replace with your package/module structure
        ],
    },
)




