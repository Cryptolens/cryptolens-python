from distutils.core import setup
setup(
  name = 'licensing',         # How you named your package folder (MyLib)
  packages = ['licensing'],   # Chose the same as "name"
  version = '0.39',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Client library for Cryptolens licensing Web API.',   # Give a short description about your library
  author = 'Cryptolens AB',                   # Type in your name
  author_email = 'support@cryptolens.io',      # Type in your E-Mail
  url = 'https://cryptolens.io',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Cryptolens/cryptolens-python/archive/v_39.tar.gz',    # I explain this later on
  keywords = ['software licensing', 'licensing library', 'cryptolens'],   # Keywords that define your package best
  classifiers=[
    #'Development Status :: 5 - Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)