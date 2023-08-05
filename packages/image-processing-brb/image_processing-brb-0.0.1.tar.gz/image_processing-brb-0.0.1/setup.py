# Usado para especificar como um pacote deve ser construído

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read() # carregamento do arquivo README.md no script
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines() # carregamento do arquivo requirements.txt no script
    
setup (
    name='image_processing-brb', # nome do pacote a ser empacotado
    version='0.0.1', # versão do pacote - toda vez que o pacote for subido, o número da versão deve ser incrementado
    author='Bruno Rigueti Brandao', # nome do autor do pacote
    author_email= 'bruno.rigueti@outlook.com', # email do autor do pacote
    description= 'pacote de exemplo para aprender a empacotar pacotes', # breve descrição do pacote
    long_description=page_description, # descrição completa do pacote a ser acessada pelo arquivo README.md
    long_description_content_type='text/markdown', # tipo de arquivo do README - .md(markdown
    url='https://github.com/rigueti-bruno/Cognizant-Data-Cloud-Engineer/tree/main/Programa%C3%A7%C3%A3o_Python/Desafio%20Codigo%201/image-processing-package', # link do repositório onde o pacote está armazenado
    packages=find_packages(), # função que busca os módulos no pacote automaticamente
    #install_requires=requirements, # requerimentos para a instalação sendo acessados no arquivo requirements.txt, caso o pacote precise de outros pacotes para funcionar
    python_requires= '>3.8', # faixa de versões do Python com as quais o pacote será compatível - restringe a utilização do pacote
)