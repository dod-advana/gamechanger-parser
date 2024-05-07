from setuptools import setup, find_packages
import os
import datetime
import shutil
import glob

# project base directory
base_dir = os.path.join(os.path.dirname(__file__), '..', '..')

requirements_path = os.path.join(base_dir, 'config', 'requirements.txt')
timeNow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')

# Read requirment.txt and store
with open(requirements_path) as f:
    required = f.read().splitlines()

# # # # #
# Purpose : Move the build artifacts to a target dir
# To consolidate setup output files
# # # # #
def move_build_artifcats(target_dir, base_dir):
    # Create the target dir if it does not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Paths for the artifacts
    dist_dir = os.path.join(base_dir, 'devTools', 'whl', 'dist')
    build_dir = os.path.join(base_dir, 'devTools', 'whl', 'build')

    # Find .egg-info dir
    egg_info_dirs = glob.glob(os.path.join(base_dir, 'gc_parser_*.egg-info')) # This generates in base dir for some reason #TODO: Fix for quality of life but not needed for functionality
    for egg_info_dir in egg_info_dirs:
        if os.path.exists(egg_info_dir):
            shutil.move(egg_info_dir, target_dir)

    # Move each item to the target dir
    if os.path.exists(dist_dir):
        shutil.move(dist_dir, target_dir)
    if os.path.exists(build_dir):
        shutil.move(build_dir, target_dir)

# Setup package
package_name = f'gc-parser-{timeNow}'
setup(
    name=package_name,
    version='1.0.1',
    author='GAMECHANGER DE Policy',
    packages=find_packages(where=base_dir, include=['policy_analytics_parser*']), # Recursively include everything in folder
    package_dir={'': base_dir}, # Project root
    install_requires=required, # requirment.txt
    description='gc-parser main branch',
    url='https://github.com/dod-advana/gamechanger-parser',
    classifiers=[
        "Programming Language :: Python :: 3.8.10",
    ],
)
# After exe, consolidate files
output_dir = os.path.join(base_dir, 'devTools', 'whl', 'whl_creation_output')
move_build_artifcats(output_dir, base_dir)