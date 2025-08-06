from setuptools import setup  

setup(
  name = 'licensing',         # How you named your package folder (MyLib)
  packages = ['licensing'],   # Chose the same as "name"
  version = '0.53',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  #description_file = 'Client library for Cryptolens licensing Web API.',   # Give a short description about your library
  long_description = 'Client library for Cryptolens Web API (software licensing).',
  long_description_content_type="text/markdown",
  author = 'Cryptolens AB',                   # Type in your name
  author_email = 'support@cryptolens.io',      # Type in your E-Mail
  url = 'https://cryptolens.io',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Cryptolens/cryptolens-python/archive/v_53.tar.gz',
  project_urls={                       # optional, shows on PyPI
        "Source": "https://github.com/Cryptolens/cryptolens-python",
        "Tracker": "https://github.com/Cryptolens/cryptolens-python/issues",
    },
  keywords = ['software licensing', 'licensing library', 'cryptolens'],   # Keywords that define your package best
  classifiers=[
    #'Development Status :: 5 - Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Operating System :: OS Independent',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
  ],

)