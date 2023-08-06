from setuptools import setup,find_packages,Extension

VERSION = '0.6'
DESCRIPTION = 'Automação do processo de classificação de solicitações de compra de Notebooks à faculdade -Trabalho Acadêmico Hipotético'
LONG_DESCRIPTION = 'Biblioteca que integra as análises iniciais e gráficos feitos sobre o conjunto de dados fornecidos para reconhecimento da natureza destes, com a implementação dos critérios de aprovação escolhidos, ferramentas para a classificação de novos estudantes e criação do perfil do estudante baseado na média ponderada das notas normalizadas atribuídas com possibilidade de pesquisa de novos pesos através de teste por força bruta implementado em API externa.'

# Setting up
setup(
    name="ProjetoNotebook",
    version=VERSION,
    author="Lucas Almeida",
    author_email="ra00319146@pucsp.edu.br",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','pandas','plotly','matplotlib','bs4','requests'],
    keywords=['python','pucsp','cdia'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
   include_package_data=True,
   package_data={'': ['Dados/*.tsv','Dados/Processamentos_Feitos/*.csv']},
   url='https://github.com/lc1a/ProjetoNotebook',
   entry_points={'ProjetoNotebook.Analista':'Analista=ProjetoNotebook:Analista'}
)