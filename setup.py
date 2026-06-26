
# Standard imports
import glob, os
from setuptools import setup, find_packages


# Begin setup
setup_keywords = dict()
setup_keywords['name'] = 'pypeit_and_dragons'
setup_keywords['description'] = 'A comparison of reducing Gemini data with DRAGONS and PypeIt'
setup_keywords['author'] = 'J. Xavier Prochaska'
setup_keywords['author_email'] = 'jxp@ucsc.edu'
setup_keywords['license'] = 'BSD'
setup_keywords['url'] = 'https://github.com/pypeit/pypeit-and-dragons'
setup_keywords['version'] = '0.0.dev0'
# Use README.md as long_description.
setup_keywords['long_description'] = ''
if os.path.exists('README.md'):
    with open('README.md') as readme:
        setup_keywords['long_description'] = readme.read()
setup_keywords['provides'] = [setup_keywords['name']]
setup_keywords['requires'] = ['Python (>=3.12.0)']
# Dependencies live in requirements.txt (single source of truth).
setup_keywords['install_requires'] = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as reqs:
        setup_keywords['install_requires'] = [
            line.strip() for line in reqs
            if line.strip() and not line.startswith('#')]
setup_keywords['zip_safe'] = False
setup_keywords['packages'] = find_packages()

if os.path.isdir('bin'):
    setup_keywords['scripts'] = [fname for fname in glob.glob(os.path.join('bin', '*'))
                                 if not os.path.basename(fname).endswith('.rst')]

setup(**setup_keywords)
