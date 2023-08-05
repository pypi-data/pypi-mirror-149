try:
    from setuptools import setup #enables develop
except ImportError:
    from distutils.core import setup

install_requires = [
                    'kaldi_io',
                    'tqdm',
                    'matplotlib',
                    'numpy',
                    'torch',
                    'librosa',
                    'pandas',
                    'pysptk',
                    'phonet',
                    'scipy',
                    'scikit_learn',
                    ]


setup(
    name='disvoice',
    version='0.1.3',
    description='Python framework designed to compute different types of features from speech files',
    author='J. C. Vasquez-Correa',
    author_email='juan.vasquez@fau.de',
    url='https://github.com/jcvasquezc/disvoice',
    download_url='https://github.com/jcvasquezc/disvoice/#files',
    project_urls={
        "Source code": "https://github.com/jcvasquezc/disvoice",
        "Documentation": "https://disvoice.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/jcvasquezc/DisVoice/issues"
    },
    license='MIT',
    install_requires=install_requires,
    packages=['disvoice'],
    package_data={'': ['audios/*']},
    keywords = ['speech', 'speech features', 'articulatory features', 'phoneme recognition', 'prosody', 'praat'],
    dependency_links=['git+git://github.com/jameslyons/python_speech_features'],
    classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Scientific/Engineering",

  ],

)




      





