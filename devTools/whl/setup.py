from setuptools import setup, find_packages
import os
import datetime
import shutil

# project base directory
base_dir = os.path.join(os.path.dirname(__file__), '..', '..')

requirements_path = os.path.join(base_dir, 'config', 'requirements.txt')
timeNow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')

# Read requirment.txt and store
with open(requirements_path) as f:
    required = f.read().splitlines()

# Move the build artifacts to a target dir
def move_build_artifcats(target_dir, base_dir, package_name):
    # Paths for the artifacts
    dist_dir = os.path.join(base_dir, 'devTools', 'whl', 'dist')
    build_dir = os.path.join(base_dir, 'devTools', 'whl', 'build')
    egg_info_dir = os.path.join(base_dir, 'devTools', 'whl', f'gc_parser_{timeNow}.egg-info')

    # Create the target dir if it does not exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Move each item to the target dir
    if os.path.exists(dist_dir):
        shutil.move(dist_dir, target_dir)
    if os.path.exists(build_dir):
        shutil.move(build_dir, target_dir)
    if os.path.exists(egg_info_dir):
        shutil.move(egg_info_dir, target_dir)

# Setup package
package_name = f'gc-parser-{timeNow}'
setup(
    name=package_name,
    version='1.0.0',
    author='GAMECHANGER DE Policy',
    packages=find_packages(where=base_dir, include=['parsers*']), # Recursively include everything in parsers/
    package_dir={'': base_dir}, # Project root
    install_requires=required, # requirment.txt
    description='gc-parser main branch',
    url='https://github.com/dod-advana/gamechanger-parser',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
# After exe consolidate files
output_dir = os.path.join(base_dir, 'devTools', 'whl', 'whl_creation_output')
move_build_artifcats(output_dir, base_dir, package_name)