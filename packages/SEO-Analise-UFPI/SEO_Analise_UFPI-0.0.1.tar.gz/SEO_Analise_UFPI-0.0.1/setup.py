from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Pacote para analisar o SEO de uma URL'
LONG_DESCRIPTION = ''

# Setting up
setup(
        name="SEO_Analise_UFPI", 
        version= VERSION,
        author= "Bruna & Elievelton",
        author_email= "gamessbrunaa@gmail.com, elievelton@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages("src"),
        install_requires=['urllib.error', 'bs4', 'selenium', 'urllib.error'],# add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)