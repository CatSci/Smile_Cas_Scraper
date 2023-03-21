from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)-> List[str]:
    """This function will return a list of requirements

    Args:
        file_path (str): file path to requirements.txt

    Returns:
        List[str]: A list of all python packages
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
    name = 'SmileScraper',
    version = '0.0.1',
    author = 'CatSci',
    author_email = 'atul.yadav@catsci.com',
    packages= find_packages(),
    install_requires = get_requirements('requirements.txt')
)
