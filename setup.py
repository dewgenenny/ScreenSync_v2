from setuptools import setup, find_packages

setup(
    name='ScreenSync',
    version='0.0.4',
    author='Tom George',
    author_email='tom@penberth.com',
    description='A Python tool for synchronizing screen colors with smart bulbs.',
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
        'platformdirs',
        'flux_led'
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




