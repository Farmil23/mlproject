from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT= '-e .'
def get_requirement(file_name:str)-> List[str]:
    '''
    This function will return the list of requirements
    mentioned in the requirements file.
    '''
    
    requirement = []
    with open(file_name) as file:
        requirements = file.readlines()
        requirements =[req.replace("\n", "") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
    return requirements


setup(
    name = "Mlproject",
    version = '0.0.1',
    author = 'Farhan kamil hermansyah',
    author_email = 'Farmiljobs@gmail.com',
    packages=find_packages(),
    install_requires=get_requirement('requirements.txt'),
)