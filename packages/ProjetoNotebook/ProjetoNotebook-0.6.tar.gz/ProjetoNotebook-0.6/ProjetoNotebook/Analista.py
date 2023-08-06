#Importando Bibliotecas Necessárias
import pkg_resources
import pandas as pd
import plotly as pl
from plotly import express as px
from plotly import graph_objects as go
import time
import itertools
import math
import random
import matplotlib as mpl
from time import sleep
from numpy import array,dot,nan,zeros,append,where,multiply
from os import system,name
import requests
import concurrent.futures
from bs4 import BeautifulSoup as bs
import datetime as dt
import numpy as np
import matplotlib.patheffects
#Tornando Dados Acessíveis no ambiente
def load_TABESTUDANTES():
  stream_te = pkg_resources.resource_stream(__name__, 'Dados/estudantes-pucsp.tsv')
  return pd.read_csv(stream_te,delimiter='\t',encoding='utf-8')
def load_COLUNASP():
  stream_cp = pkg_resources.resource_stream(__name__, 'Dados/Processamentos_Feitos/colunas_p.csv')
  inter=pd.read_csv(stream_cp,encoding='utf-8')
  cp=inter.set_index('matrícula')
  return cp
def load_NOTAS():
  stream_nt = pkg_resources.resource_stream(__name__, 'Dados/Processamentos_Feitos/notas_df.csv')
  inter=pd.read_csv(stream_nt,encoding='utf-8')
  nt=inter.set_index('matrícula')
  return nt
def load_Legendas():
  CURPCOD={1:"Ciência de Dados",2:"Direito",3:"Medicina",4:"História",5:"Administração",6:"Engenharia Biomédica",7:"Design",8:"Ciência da Computação",9:"Filosofia"}
  CPC={1:"Branco",2:"Preto"}
  SPC={1:"Masculino",2:"Feminino"}
  EPC={1:"Pública",2:"Privada"}
  return CURPCOD,CPC,SPC,EPC
  
TABESTUDANTES=load_TABESTUDANTES()
COLUNASP=load_COLUNASP()
NOTAS=load_NOTAS()
CURPCOD,CPC,SPS,EPC=load_Legendas()

#Definindo a Classe AgrupamentoCondicional

#Utilizada para armazenar e modificar funções que atuam sobre os dados de cada estudante e retornam um indicador de Subconjunto para a tabela especificada.

#Recebe como parâmetro de inicialização opcional Ano e Mês para a busca do Salário Mínimo Vigente no período fornecido.

#Caso Não fornecido o parâmetro de Inicialização utiliza o módulo datetime do Python para obter o ano e mês locais da Máquina que executa o código.

class AgrupamentoCondicional():
  def SMWeb(self,ano=dt.datetime.today().year,mes=dt.datetime.today().month):
    
    '''Retorna o valor, em tipo float, do Salário Mínimo Nominal vigente no ano e mês fornecidos a partir da 
  acquisição e formatação dos dados fornecidos pela página html 
  hospedada no endereço:'https://www.dieese.org.br/analisecestabasica/salarioMinimo.html
  Caso não sejam fornecidos ano e mês utiliza a biblioteca datetime para adquirir o ano e mes locais da
  máquina de execução do código.'''
  
    mint2mstr={1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',
             11:'Novembro',12:'Dezembro'}
    link='https://www.dieese.org.br/analisecestabasica/salarioMinimo.html#2021'
    try:
      t=requests.get(link)
    except:
      return f'Erro ao buscar Página, Link:{link}'
    if t.status_code!=200:
      return f'Erro do Status de Resposta fornecida pelo Site,Esperava-se 200 e obteu {t.status_code}'
    html_str=t.content
    SMsoup=bs(html_str,'html.parser')
    tabela=SMsoup.find({'table'})
    df=pd.read_html(str(tabela))[0].apply(
                lambda x: np.array((x[0],x[1])) if x[0]!=x[1] else np.nan,axis=1).dropna()
    df_arr=array([i for i in df])
    dez=np.where(df_arr[:,0]=='Dezembro')[0]
    df_anos=[]
    for i in range(len(dez)):
      if i==0:
        df_anos.append(df_arr[0:dez[i],:])
      else:
        df_anos.append(df_arr[dez[i-1]:dez[i],:])
    anos=[int(str(i.find('a')).split('>')[1].replace('</a','')) for i in SMsoup.find_all('td') if i.find('a')!=None]
    ano_mes_dict={k:pd.DataFrame(columns=['SM Nominal'],index=[i[0] for i in v],data=[i[1] for i in v]) for k,v in zip(anos,df_anos)}
    if ano in anos:
      if type(mes)==str:
        try:
          self.SmEncontrado=float(ano_mes_dict[ano].loc[mes][0].replace('R$','').replace('.','').replace(',','.').strip())
          return float(ano_mes_dict[ano].loc[mes][0].replace('R$','').replace('.','').replace(',','.').strip())
        except:
          self.SmEncontrado=float(ano_mes_dict[ano].iloc[0][0].replace('R$','').replace('.','').replace(',','.').strip())
          return float(ano_mes_dict[ano].iloc[0][0].replace('R$','').replace('.','').replace(',','.').strip())
      else:
        try:
          self.SmEncontrado=float(ano_mes_dict[ano].loc[mint2mstr[mes]][0].replace('R$','').replace('.','').replace(',','.').strip())
          return float(ano_mes_dict[ano].loc[mint2mstr[mes]][0].replace('R$','').replace('.','').replace(',','.').strip())
        except:
          self.SmEncontrado=float(ano_mes_dict[ano].iloc[0][0].replace('R$','').replace('.','').replace(',','.').strip())
          return float(ano_mes_dict[ano].iloc[0][0].replace('R$','').replace('.','').replace(',','.').strip())
    else:
      return f'Ano {ano} Não Encontrado No Site Buscado.'
  
  def __init__(self,SM=0):
    
    '''Cria uma Instância/Objeto da Classe AgrupamentoCondicional a partir de um dicionário
    {'ano': Ano Entre 1995 e Atual,'mes': Mes do Ano fornecido} opcional fornecido para a busca
    do Salário Mínimo Vigente No momento da execução para realizar a classificação
    de classe social do IBGE utilizando a Renda Familiar Mensal.'''
    
    self.SM=SM
    #Executando a Busca do SM
    if SM==0:
      AgrupamentoCondicional.SMWeb(self)
    else:
      AgrupamentoCondicional.SMWeb(self,**self.SM)
    
  def group_renda(self,r):
    
    """Retorna uma string pertencente ao conjunto [A,B,C,D,E] que representa a classe social na 
    qual o estudante está incluido de acordo com sua renda familiar mensal medida em múltiplos
    do salário mínimo. Métrica utilizada pelo IBGE.
    Argumentos/Parâmetros:
    r=Renda Familiar mensal"""
    
    salario_min=self.SmEncontrado
    if r<=salario_min*2:
      return "E"
    elif r<=salario_min*4:
      return "D"
    elif r<=salario_min*10:
      return "C"
    elif r<=salario_min*20:
      return "B"
    else:
      return "A"
    
  def group_idade(self,i):
    
    """Retorna uma string pertencente ao conjunto [J,A1,A2,I],
    que representa em qual faixa etária o estudante se encontra de acordo com sua idade.
    Definições:
    J=Jovem (até 19 anos)
    A1=Adulto até 30 anos
    A2=Adulto entre 31 e 59 anos
    I=Idoso(Mais que 60 anos).
    Argumentos/Parâmetros:
    i= Idade"""
    
    if i<=19:
      return "J"
    elif i<=30:
      return "A1"
    elif i<=59:
      return "A2"
    else:
      return "I"
    
  def group_motiv(self,m):
    
    """Retorna uma string pertencente ao conjunto [NM,PM,M,MM] que representa em qual grupo,
       m questão da motivação em permanecer no curso, o estudante se encontra.
       Definições:
       NM=Não Motivado (0 a 3)
       PM= Parcialmente Motivado (4 a 6)
       M= Motivado (7 a 9)
       MM= Muito Motivado (10)
       Argumentos/Parâmetros:
       m=Motivação"""
    
    if m<=3:
      return "NM"
    elif m<=6:
      return "PM"
    elif m<=9:
      return "M"
    else:
      return "MM"
    
#Definindo a Classe ModificarDados

#Utilizada para armazenar funções que realizam operações sobre os dados originais e retornam análises pertinentes em formato pronto para a criação de gráficos

#Possui também funções para agrupar estudantes em subconjuntos a partir de colunas pré-determinadas para facilitar a visualização gráfica das informações

#Ao ser chamada inicializa uma Instância da Classe AgrupamentoCondicional, Logo aceita o mesmo parâmetro opcional desta e realiza   #as operações que envolvem a classificação dos estudantes em classes sociais utilizando o valor do salário mínimo obtido através da  #função SMWeb

class ModificarDados():
  
  def __init__(self,SM=0):
    '''Inicializador da Classe ModificarDados que aceita o mesmo parâmetro Opcional da Classe AgrupamentoCondiciona
    Pois Inicializa uma Instância desta.'''
    
    self.inst_AC=AgrupamentoCondicional(SM)
    
  def criar_subcjtdict(self,tabela,colunas,legendas=None,n=1):
    """Retorna dicionário(s) de tabela(s) de subconjunto(s) de todos os itens da tabela original, que apresentam o mesmo valor em uma determinada coluna, 
    para todos os valores presentes nesta coluna.
    Argumentos/Parâmetros:
    tabela=tabela original (já existente) do Pandas;
    colunas= Nome da coluna da tabela original (ou lista destes nomes) sobre a qual se deseja criar os subconjuntos;
    legendas=Dicionário que tem como chaves os códigos presentes na coluna da tabela original e como valores as legendas destes códigos que serão as chaves 
    do dicionário criado.Seu valor padrão é None
    e quando não fornecido tal dicionário, as chaves do dicionário criado serão os próprios valores sobre os quais foram feitos os subconjuntos.;
    n= Número de colunas sobre as quais se deseja criar subconjuntos. 
    Seu valor padrão é 1 e caso o valor passado seja 1 mas o tipo de dado do valor passado ao parâmentro colunas não for str,int ou float a função retorna uma str de erro."""
    
    if n==1:
        if type(colunas)!=str and type(colunas)!=int and type(colunas)!=float:
            return "Se o número de colunas sobre as quais se deseja criar subconjuntos (n) for 1, O valor do parâmetro colunas tem que ser str ou float ou int."
        if legendas!=None:
            return dict([(i,z) for i,z in zip(legendas.values(),[i[1] for i in tabela.groupby([colunas])])])
        else:
            return dict([(i[0],i[1]) for i in tabela.groupby([colunas])])
    else:
        if legendas!=None:
            col_leg=[(i,list(z.values())) for i,z in zip(colunas,legendas)]
            subcjts=[list(tabela.groupby([b[0]])) for b in col_leg]
            return [dict([(i,z[1]) for i,z in zip(a,b)]) for a,b in zip([c[1] for c in col_leg],subcjts)]
        else:
            subcjts_lst=[list(tabela.groupby([i])) for i in colunas]
            leg_sub=[i for i in subcjts_lst]
            return [dict(i) for i in leg_sub]
          
  def criar_subcjtcond(self,tabela,colunas=None,condicoes=None,q=None):
      """Retorna uma tabela do subconjunto dos itens cujos valores das colunas fornecidas obedecem uma ou mais condicoes a partir de uma tabela fornecida.
    Argumentos/Parâmetros:
    tabela=tabela original (já existente) do Pandas;
    colunas=Lista da(s) coluna(s) cuja(s) qual(is) os valores serão avliados a partir da(s) condição(ções);
    condicoes=Lista da(s) condição(ções) que será(serão) usada(s) para avaliar os valores."""
      if q==None:
          col_cond=["{}{}".format(i,z) for i,z in zip(colunas,condicoes)]
          if len(colunas)>1:
              q=" and ".join(col_cond)
          else:
              q=col_cond[0]
      subcjt=tabela.query(q)
      return subcjt
    
  def juntar_endereco(self,tabela_original):
    
    '''Transforma as Colunas Originais da Tabela fornecida (excluindo bairro) para uma coluna somente que possui as mesmas
    informações em tipo string separadas por vírgulas e retorna uma cópia da tabela original com a coluna transformada e
    sem as colunas cujas informações foram agrupadas.'''
    
    tabela_cp=tabela_original.copy(deep=True)
    tabela_cp['numero']=[str(i) for i in tabela_cp['numero']]
    linhas_endereco=[list(i) for i in tabela_cp[["logradouro","numero","cidade","uf","cep"]].values]
    valores_endereco=[",".join(i) for i in linhas_endereco]
    tabela_cp.drop(['logradouro','numero','cidade','uf','cep'],inplace=True,axis=1)
    tabela_cp["endereço"]=valores_endereco
    cols=tabela_cp.columns.tolist()
    cols=cols[:-3]+cols[-1:]+cols[8:-1]
    tabela_cp=tabela_cp[cols]
    return tabela_cp
  
  def modificar(self):
    #Criando Subconjuntos Para 8 Colunas Selecionadas Para visualizar o perfil dos dados e uma Cópia da Tabela Original de Estudantes
    #Na qual os valores das colunas ['Renda','Motivação' e 'Idade'] são modificadas utilizando a Classe AgrupamentoCondicional
    subcjts_leg={k:self.criar_subcjtdict(TABESTUDANTES,k,None,1) for k in ['cor','sexo','escola','cod_curso','bairro','motivação','idade','ano_curso']}
    TABE_copia=TABESTUDANTES.copy(deep=True)
    TABE_copia['renda'],TABE_copia['idade'],TABE_copia['motivação']=TABESTUDANTES['renda'].apply(self.inst_AC.group_renda),TABESTUDANTES['idade'].apply(self.inst_AC.group_idade),TABESTUDANTES['motivação'].apply(self.inst_AC.group_motiv)
    #Criando Subconjuntos Condicionais de estudantes combinando os valores das colunas ['Cor','Escola','Sexo']
    col_vals={'cor':[1,2],'sexo':[1,2],'escola':[1,2]}
    condicoes_1=[f'{col}=={val}' for col in col_vals.keys() for val in col_vals[col]]
    poss=[i for i in itertools.combinations(condicoes_1,2) if i[0][:-1]!=i[1][:-1] and i[0][0]!=i[1][0]]
    queries=[' and '.join(comb) for comb in poss]
    subcjts_cond=[self.criar_subcjtcond(TABESTUDANTES,q=query) for query in queries]
    #Criando  tabelas de distribuição da quantidade de estudantes para colunas ['Cor','Escola','Sexo','Idade','Renda','Curso','Motivação']
    TDist={col:(len(subcjts_leg[col][1]),len(subcjts_leg[col][2])) for col in ['cor','sexo','escola']}
    subcjts_TABEcopia={i:self.criar_subcjtdict(TABE_copia,i,None,1) for i in ['idade','renda','motivação']}
    TDist['Idade']=[len(subcjts_TABEcopia['idade'][k]) for k in ['J','A1','A2']]
    TDist['Renda']=[len(subcjts_TABEcopia['renda'][k]) for k in ['A','B','C','D','E']]
    TDist['Motivação']=[len(subcjts_TABEcopia['motivação'][k]) for k in ['NM','PM','M','MM']]
    TDist['Curso']=[len(subcjts_leg['cod_curso'][i]) for i in range(1,10)]
    Indices=[['Branco','Preto'],['Masculino','Feminino'],['Pública','Privada'],['J','A1','A2'],['A','B','C','D','E'],['NM','PM','M','MM'],CURPCOD.values()]
    TDistDfs={k:pd.DataFrame({'Quantidade':array(TDist[k]),'% do Total':(array(TDist[k])/array([500]*len(TDist[k])))*100},index=ind) for k,ind in zip(TDist.keys(),Indices)}
    self.DistDfs=TDistDfs
    #Gerando Dados dos Gráficos de Distribuição:
    DistData={col:{'x':TDistDfs[col]['Quantidade'].to_numpy(),'y':list(TDistDfs[col].index)} for col in TDistDfs.keys()}
    #Parâmetros de Modificações Visuais do Matplotlib para cada gráfico
    props=[["Distribuição da Quantidade de Estudantes por Cor","Distribuição da Quantidade de Estudantes que vieram de Escola Pública/Privada","Distribuição da Quantidade de Estudantes por Sexo","Distribuição da Quantidade de Estudantes por Agrupamento de Idade","Distribuição da Quantidade de Estudantes por Classe Social","Distribuição da Quantidade de Estudantes por Curso","Distribuição da Quantidade de Estudantes por Agrupamento de Motivação"],
           [25,25,25,25,25,25,25],
           [15,15,15,15,15,15,15],
           [25,25,25,25,25,20,20],
           [160,120,120,120,140,40,60],
           [10,10,10,10,10,2,5],
           [0.4,0.4,0.4,0.4,0.4,0.25,0.33],
           [40,40,40,40,40,40,40],
           [False,False,True,False,False,False,False]]
    Dicts=[[('xy_dict',DistData[col]),
                       ('titulo',props[0][i]),
                       ('titulo_ls',props[1][i]),
                       ('tick_ls',props[2][i]),
                       ('valores_ls',props[3][i]),
                       ('limx_add',props[4][i]),
                       ('padx_valor',props[5][i]),
                       ('pady_valor',props[6][i]),
                       ('pady_titulo',props[7][i]),
                       ('ev',props[8][i])] for col,i in zip(['cor','escola','sexo','Idade','Renda','Curso','Motivação'],range(9))]
    GrafDistData={k:v for k,v in zip(DistData.keys(),Dicts)}
    self.GrafDistData=GrafDistData
    #Gerando Dados dos Gráficos de Dispersão:
    SmE=self.inst_AC.SmEncontrado
    DescribeRendaTO=TABESTUDANTES['renda'].describe()
    #Lista do ìndice de elementos na tabela para plotar no eixo x em um distanciamento uniforme
    RangeElem=list(range(1,501))
    #Transformando todos os valores de renda para os valores de seus respectivos Logaritmos de base 10
    #Com intuito de facilitar a visualiazação
    RendaLogScale=TABESTUDANTES['renda'].apply(lambda x: np.log10(x))
    #Retirando Outliers (Renda Maior que 4 Salários Mínimo ou Menor que 120 Reais)
    MA_TO_Soutliers=TABESTUDANTES['renda'].apply(lambda x:x if x<=4*SmE and x>120 else None).dropna()
    #Calculando a Porcentagem do total representada pelos outliers
    Pct_Outliers=((500-len(MA_TO_Soutliers))/500)*100
    #Realizando cálculos da Média,Desvio Padrão,Coeficiente de Variação para a tabela sem os outliers.
    DescribeRendaSoutliers=MA_TO_Soutliers.describe()
    Coef_Var=[(DescribeRendaSoutliers['std']/DescribeRendaSoutliers['mean'])*100,(DescribeRendaTO['std']/DescribeRendaTO['mean'])*100]
    GrafDispMData=[RangeElem,RendaLogScale,SmE,120,MA_TO_Soutliers,DescribeRendaTO['mean'],Pct_Outliers,Coef_Var,DescribeRendaTO['std'],
                   DescribeRendaSoutliers]
    self.GrafDispMData=GrafDispMData
    self.GrafDispData=GrafDispMData[:5]
#Definindo a Classe PlotarGraficos

#Utiliza os dados gerados pela classe ModificarDados para facilitar a visualização destes através da Criação de Gráficos utilizando a Biblioteca de Plotagem Matplotlib, armazena funções as quais cada uma realiza a criação de um ou mais gráficos diferente e os salva como um arquivo .jpg no diretório especificado na chamada da função. Aceita o mesmo parâmetro opcional da classe AgrupamentoCondicional Pois inicializa, através da classe ModificarDados, uma instância desta.

#Gráficos Gerados:

#Histograma da Renda da tabela armazenada na variável TABESTUDANTES (Tabela Original)

#Gráfico de Dispersão da Renda em Escala Logaritmica com Linhas Horizontais Representando o Limite de Renda de cada Classe Social

#Mesmo Gráfico de Dispersão porém com linhas horizontais representando a Média das rendas com e sem Outliers, os desvios padrões , coeficientes de variações para cada um destes conjuntos e a Mediana do Conjunto com Outliers

#Conjunto de Gráficos de Barras Horizontais no qual cada gráfico mostra uma distribuição dos valores de uma determinada coluna na tabela e as porcentagens destes valores em relação ao total
class PlotarGraficos():
  
  def __init__(self,SM=0):
    
    ''' Inicializa uma Instância da classe Plotar Gráficos que
    Utiliza os dados gerados pela classe ModificarDados para facilitar a visualização 
    destes através da Criação de Gráficos utilizando a Biblioteca de Plotagem Matplotlib,
    armazena funções as quais cada uma realiza a criação de um ou mais gráficos diferente
    e os salva como um arquivo .jpg no diretório especificado na chamada da função.
    Aceita o mesmo parâmetro opcional da classe AgrupamentoCondicional 
    Pois inicializa, através da classe ModificarDados, uma instância desta.'''
    
    #Inicializando uma Instância da Classe ModificarDados e atribuindo ao seu argumento Opcional
    #O mesmo valor passado ao argumento Opcional do inicializador da classe PlotarGraficos
    self.inst_MD=ModificarDados(SM)
    #Utilizando o Método modificar da Instância de ModificarDados para armazenar os dados gerados a partir
    #deste Argumento Opcional em atributos da Instância 'inst_MD'
    self.inst_MD.modificar()
    
  def PlotarHistRendaTO(self,path):
    
    '''Plotagem do Histograma da Renda da tabela armazenada na variável TABESTUDANTES (Tabela Original)'''
    
    fig=mpl.pyplot.figure(constrained_layout=True,figsize=(12,8))
    gs=fig.add_gridspec(3,4,hspace=0.2,wspace=0.2)
    ax=[fig.add_subplot(gs[0,:]),fig.add_subplot(gs[1,0:2]),fig.add_subplot(gs[1,2:4])]
    ax1=[fig.add_subplot(gs[2,0:2]),fig.add_subplot(gs[2,2:4])]
    ax[0].hist(TABESTUDANTES['renda'],bins=500,color='b')
    ax[0].set_xlim(0,1212*2)
    ax[0].set_ylim(0,260)
    ax[1].hist(TABESTUDANTES['renda'],bins=500,color='b')
    ax[1].set_xlim(1212*2,1212*4)
    ax[1].set_ylim(0,180)
    ax[2].hist(TABESTUDANTES['renda'],bins=500,color='r')
    ax[2].set_xlim(1212*4,1212*10)
    ax[2].set_ylim(0,35)
    ax1[0].hist(TABESTUDANTES['renda'],bins=500,color='r')
    ax1[0].set_xlim(1212*10,1212*20)
    ax1[0].set_ylim(0,4)
    ax1[1].hist(np.log10(TABESTUDANTES['renda']),bins=500,color='r')
    ax1[1].set_xlim(5.75,6)
    ax1[1].set_ylim(0,1.1)
    classes=["E","D","C"]
    classes1=["B","A"]
    for i in range(3):
      ax[i].set_title("Classe {}".format(classes[i]),**{"family":"Monospace","size":14,"weight":"bold"})
    for z in range(2):
      ax1[z].set_title("Classe {}".format(classes1[z]),**{"family":"Monospace","size":14,"weight":"bold"})
      axxl=[i for a in ax for i in a.get_xticklabels()]
      axyl=[i for a in ax for i in a.get_yticklabels()]
      ax1xl=[i for a in ax1 for i in a.get_xticklabels()]
      ax1yl=[i for a in ax1 for i in a.get_yticklabels()]
    tick_font=mpl.font_manager.FontProperties(family='Monospace',size=12, weight='bold')
    for label in axxl:
      label.set_fontproperties(tick_font)
    for label in axyl:
      label.set_fontproperties(tick_font)
    for label in ax1xl:
      label.set_fontproperties(tick_font)
    for label in ax1yl:
      label.set_fontproperties(tick_font)
    ax1[1].set_xlabel('Escala Logarítmica',fontdict={"family":"Monospace","size":10,"weight":"bold"})
    fig.suptitle("Histograma de Cada Classe Social",family="Monospace",size=20,weight="bold",ha='center',va='top',y=1.08,x=0.51)
    fig.supylabel("Quantidade de Estudantes",family="Monospace",size=20,weight="bold",x=-0.1)
    fig.supxlabel("Renda",family="Monospace",size=20,weight="bold",x=0.5,y=-0.1)
    mpl.pyplot.savefig(path,dpi=1280,bbox_inches='tight')
    
    
  def PlotarGrafDisp(self,path):
    
    '''Gráfico de Dispersão da Renda em Escala Logaritmica com Linhas Horizontais Representando o Limite de Renda de cada Classe Social'''
    
    def texto_personalizado(pos_x,pos_y,padx,pady,c,texto,ax,ts):
      return ax.text(s=texto,x=pos_x+padx,y=pos_y+pady,fontdict={"family":"Monospace","size":ts,"weight":"bold"},
                     color=c,path_effects=[mpl.patheffects.withStroke(linewidth=1, foreground="black")])
    
    fig,ax=mpl.pyplot.subplots(figsize=(12,8))
    colors=mpl.pyplot.get_cmap("coolwarm")
    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    n_elem,renda_logscale,sm,r_menor,ma_soutlier2=self.inst_MD.GrafDispData
    limite_classe_rendaagr=dict([(k,np.log10(sm*v)) for k,v in zip(['E','D','C','B','A'],[2,4,10,20,20])])
    ax.scatter(n_elem,renda_logscale,color=colors(rescale(renda_logscale)))
    hlines=[ax.axhline(i,linestyle='dashed',color=c) for i,c in zip(list(limite_classe_rendaagr.values())[:-1],[(0.2, 0.4, 1, 1),
                                                                                                                (0.4, 0.6, 0.7, 1),
                                                                                                                (0.9, 0.6, 0.1, 1),
                                                                                                                (0.8, 0.2, 0.1, 1)])]
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    tick_font=mpl.font_manager.FontProperties(family='Monospace',size=12, weight='bold')
    for label in ax.get_yticklabels():
      label.set_fontproperties(tick_font)
    for label in ax.get_yticklabels():
        label.set_fontproperties(tick_font)
    #Criando e ajustando a posição e cor do Texto das Classes.
    texto_personalizado(100,3.38453261549,-50,-2,(0.2, 0.4, 1, 1),"Classe E = 69.8%",ax,18)
    texto_personalizado(100,3.68556261116,-120,-0.23,(0.4, 0.6, 0.7, 1),"Classe D = 20.0%",ax,18)
    texto_personalizado(100,4.08350261983,-120,-0.27,(0.3,0.5,0.5,1),"Classe C = 8.4%",ax,18)
    texto_personalizado(100,4.38453261549,-120,-0.23,(0.9, 0.6, 0.1, 1),"Classe B = 1.0%",ax,18)
    texto_personalizado(100,4.38453261549+1,-50,+0.5,(0.8, 0.2, 0.1, 1),"Classe A = 0.8%",ax,18)
    #Definindo Título, Texto do eixo y e cor de fundo do gráfico.
    ax.set_title("Gráfico de Dispersão da Renda dos Estudantes em Escala Logarítmica",**{"family":"Monospace","size":25,"weight":"bold"},loc='center',pad=40)
    ax.set_ylabel("log('Renda em R$')",fontdict={"family":"Monospace","size":15,"weight":"bold"},labelpad=40)
    ax.set_facecolor((0.65,0.64,0.647,0.09))
    #Salvando em .jpg
    mpl.pyplot.savefig(path,dpi=1280,bbox_inches='tight')
  
  def PlotarGrafDispM(self,path):
    
    '''Mesmo Gráfico de Dispersão porém com linhas horizontais representando a Média das rendas com e sem Outliers,
    os desvios padrões , coeficientes de variações para cada um destes conjuntos e a Mediana do Conjunto com Outliers'''
    
    n_elem,renda_logscale,sm,r_menor,ma_soutlier2,media_a,pct_outliers,cvs,desvio_padrao,d_soutlier=self.inst_MD.GrafDispMData
    
    def texto_personalizado(pos_x,pos_y,padx,pady,c,texto,ax,ts):
      return ax.text(s=texto,x=pos_x+padx,y=pos_y+pady,fontdict={"family":"Monospace","size":ts,"weight":"bold"},color=c,
                     path_effects=[mpl.patheffects.withStroke(linewidth=1, foreground="black")])
    
    fig,ax=mpl.pyplot.subplots(figsize=(12,8))
    colors=mpl.pyplot.get_cmap("coolwarm")
    rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
    limite_classe_rendaagr=dict([(k,np.log10(sm*v)) for k,v in zip(['E','D','C','B','A'],[2,4,10,20,20])])
    ax.scatter(n_elem,renda_logscale,color=colors(rescale(renda_logscale)))
    hlines=[ax.axhline(np.log10(media_a),color='red',linestyle='dashed',label="MA de Todos os Dados: R${:.2f}".format(media_a)),
    ax.axhline(np.log10(ma_soutlier2.mean()),color='green',linestyle='dashed',
               label="MA ao Retirar Classes A,B,C e Rendas Menores que R${}\n({:.2f}% dos Estudantes): R${:.2f}".format(
                   r_menor,pct_outliers,ma_soutlier2.mean())),
    ax.axhline(np.log10(TABESTUDANTES['renda'].median()),color='black',linestyle='dashed',label='Mediana de Todos os Dados: R${}'.format(
        TABESTUDANTES['renda'].median()))]
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    tick_font=mpl.font_manager.FontProperties(family='Monospace',size=12, weight='bold')
    for label in ax.get_yticklabels():
      label.set_fontproperties(tick_font)
    for label in ax.get_yticklabels():
      label.set_fontproperties(tick_font)
    texto_personalizado(550,5,-16,0,'red',"Desvio Padrão: {:.2f}\nCoef. de Variação: {:.2f}%".format(desvio_padrao,cvs[1]),ax,18)
    texto_personalizado(550,2,-16,0,'green',"Desvio Padrão: {:.2f}\nCoef. de Variação: {:.2f}%".format(d_soutlier['std'],cvs[0]),ax,18)
    ax.set_title("Gráfico de Dispersão da Renda dos Estudantes em Escala Logarítmica",**{"family":"Monospace","size":25,"weight":"bold"},loc='center',pad=40)
    ax.set_ylabel("log('Renda em R$')",fontdict={"family":"Monospace","size":15,"weight":"bold"},labelpad=40)
    ax.set_facecolor((0.65,0.64,0.647,0.09))
    ax.legend(prop={"family":"Monospace","weight":"semibold","size":13})
    mpl.pyplot.savefig(path,dpi=1280,bbox_inches='tight')
    
  def PlotarGrafBarras(self,path):
    
    '''Conjunto de Gráficos de Barras Horizontais no qual cada gráfico 
    mostra uma distribuição dos valores de uma determinada 
    coluna na tabela e as porcentagens destes valores em relação ao total'''
    
    def criar_g_barras(titulo,xy_dict,titulo_ls=20,tick_ls=15,valores_ls=25,sombra_s=4,
                       bgcolor="silver",limx_add=100,padx_valor=10,pady_valor=0.4,
                       pady_titulo=20,ev=False,path=path):
      
      """Cria um gráfico de barras horizontais a partir do título e do dicionário de valores fornecidos para x e y usando o pyplot da 
      biblioteca matplotlib e salva em um arquvio .jpg.
      Argumentos/Parâmetros:
      titulo= Título do gráfico. (str)
      xy_dict= dicionário do tipo {'x': lista ou np.ndarray dos valores do eixo x,'y':lista ou np.ndarray dos valores do eixo y}
      titulo_ls=Tamanho do Texto do Título (int ou float)
      tick_ls= Tamanho do Texto dos valores representados nos eixos x e y (int ou float)
      valores_ls= Tamanho do Texto que representa o valor exato, no eixo x, localizado em frente a cada barra (int ou float)
      sombra_s= Intensidade do efeito de sombra no texto localizado em frente a cada barra (int ou float)
      bgcolor= str com nome de uma cor que será a cor usado no plano de fundo do gráfico
      limx_add= Valor adicional ao limite do eixo x no gráfico para que os textos em frente as barras não saiam do gráfico quando valores de x são altos.
      padx_valor= int ou float representando a quantidade de pixels para mover todos os textos em frente as barras no eixo x do gráfico.
      pay_valor= int ou float representando a quantidade de pixels para mover todos os textos em frente as barras no eixo y do gráfico.
      pady_titulo= int ou float representando a quantidade de pixels para mover o texto do título no eixo y: Mais perto , ou longe do começo do gráfico.
      ev= valor booleano que será usado para gerar as cores do gráfico -- se False o matplotlib.colors é usado para gerar um mapeamento de cores utilizando 
      os valores mínimo e máximo , no  eixo x, dos pontos;
      --se True gera cores a partir de uma escolha aleatória das cores tab: do matplotlib. Deve ser atribuído TRUE somente se o valor mínimo e o valor 
      máximo dos pontos no eixo x FOR IGUAL.
      """
      
      fig,ax=mpl.pyplot.subplots(figsize=(12,8))
      ax.set_title(titulo,**{"family":"Monospace","size":titulo_ls,"weight":"bold"},pad=pady_titulo)        
      colors=mpl.pyplot.get_cmap("Pastel1")
      rescale = lambda y: (y - np.min(y)) / (np.max(y) - np.min(y))
      if ev==False:
          hbars=ax.barh(xy_dict["y"],xy_dict["x"],color=colors(rescale(xy_dict['x'])),edgecolor='black',linewidth=1.5)
          for i,z,c in zip(hbars,xy_dict["x"],colors(rescale(xy_dict['x']))):
              ax.text(s="{} = {:.2f}%".format(z,(z/sum(xy_dict['x']))*100),x=z+padx_valor,y=i.get_y()+pady_valor,**{"family":"Monospace","size":valores_ls,
                                                                                                                       "weight":"bold"},
                    color=c,path_effects=[mpl.patheffects.withStroke(linewidth=sombra_s, foreground="black")])
      else:
          colors=random.choices(['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:olive','tab:cyan'],k=len(xy_dict))
          hbars=ax.barh(xy_dict["y"],xy_dict["x"],color=colors,edgecolor='black',linewidth=1.5)
          for i,z,c in zip(hbars,xy_dict["x"],colors):
              ax.text(s="{} = {:.2f}%".format(z,(z/sum(xy_dict['x']))*100),x=z+padx_valor,y=i.get_y()+pady_valor,
                      **{"family":"Monospace","size":valores_ls,"weight":"bold"},
                    color=c,path_effects=[mpl.patheffects.withStroke(linewidth=sombra_s, foreground="black")])
      ticks_font = mpl.font_manager.FontProperties(family='Monospace',size=tick_ls, weight='bold')
      for label in ax.get_xticklabels():
            label.set_fontproperties(ticks_font)
      for label in ax.get_yticklabels():
            label.set_fontproperties(ticks_font)
      ax.set_xlim(ax.get_xlim()[0],ax.get_xlim()[1]+limx_add)
      ax.set_facecolor(bgcolor)
      mpl.pyplot.savefig(path+'{}'.format(titulo.lower().replace(" ","_").replace("/","_")+'.jpg'),dpi=1280,bbox_inches='tight')
    GrafData=self.inst_MD.GrafDistData
    PlotarGrafBarras=[criar_g_barras(**dict(GrafData[i])) for i in GrafData.keys()]
    
#Definindo a Classe NotasNormalizadas

#tem como propósito Armazenar as funções que alteram os valores das cinco Colunas Primárias Pré-Determinadas,
#Para cada estudante, com o valor da NotaNormalizada (calculada a partir deste valor)
#das respectivas colunas.

#Aceita mesmo parâmetro opcional da classe AgrupamentoCondicional para a Busca do Salário Mínimo Vigente Pois instancia uma classe desta.

#Define o método Criar para cada Instância que retorna uma Tabela de Notas dos estudantes utilizando a tabela na variável COLUNASP (Tabela das colunas primárias pré-determinadas) e o Salário Mínimo Encontrado pela Instância da classe AgrupamentoCondicional

#Critérios:

#Colunas Principais
#Renda
#Escola
#Motivação
#Curso
#Cor

#Pesos Reguladores das Colunas Principais
# Pr
# Pe
# Pm
# Pcur
# Pc

#Média Ponderada:

#Mp = {Pr*RN + Pe*EN + Pm*MN + Pcur*CurN + Pc*CN}/{Pr+Pe+Pm+Pcur+Pc}

#Com: Mp pertencente a [0,10]

#Tal que:

#RN=Nota Normalizada da Renda
#EN=Nota Normalizada da Escola
#MN=Nota Normalizada da Motivação
#CurN=Nota Normalizada do Curso
#CN=Nota Normalizada da Cor

class NotasNormalizadas():
  
  def __init__(self,tbcp=COLUNASP,SM=0):
    
    '''Inicializa uma Instância da Classe NotasNormalizadas que tem como propósito
    Armazenar as funções que alteram os valores das cinco Colunas Primárias Pré-Determinadas,
    Para cada estudante, com o valor da NotaNormalizada (calculada a partir deste valor)
    das respectivas colunas. Define um método (Criar) para retornar uma Tabela do Pandas
    contendo as notas das cinco colunas para cada estudante e tem com índice o RA dos
    estudantes. Aceita o mesmo parâmetro Opcional da classe AgrupamentoCondicional para
    a busca do salário mínimo vigente pois inicializa uma instância desta.'''
    
    self.tbcp=tbcp.copy(deep=True)
    self.inst_AC=AgrupamentoCondicional(SM)
    
  def Criar(self):
    '''Aplica as Funções de Normalização da Nota para os dados de cada Estudante e retorna uma Tabela destas.'''
    
    def RN(r):
      '''Nota Normalizada da Renda: Utiliza o Valor do Salário Mínimo Encontrado pela Classe Agrupamento Condicional
      
      Se Renda for Menor ou Igual a 1 Salários Mínimo: RN=10
      Se Renda for Menor ou Igual a 2 Salários Mínimo e Maior que 1 Salário Mínimo: RN=8
      Se Renda for Maior que 2 salários Mínimo e Menor ou igual a 3 Salários Mínimos: RN=7
      Se Renda for Maior que 3 salários Mínimos e Menor ou igual a 4 Salários Mínimo: RN=6
      
      Se nenhum destes for o caso atribuí notas únicas às classes sociais restantes utilizando o agrupamento da
      instância da classe AgrupamentoCondicional especificada na Inicialização:
      
      Classe C( Renda Maior que 4 e menor ou igual a 10 Salários Mínimos): RN=3
      Classe B( Renda Maior que 10 e menor ou igual a 20 Salários Mínimos): RN=1
      Classe A( Renda Maior que 20 Salários Mínimos): RN=0'''
      salario_min=self.inst_AC.SmEncontrado
      if r<=2*salario_min:
        if r<=salario_min:
          return 10
        else:
          return 8
      elif r<=4*salario_min:
        if r<=3*salario_min:
          return 7
        else:
          return 6
      else:
        classe = self.inst_AC.group_renda(r)
        if classe=="A":
          return 0
        elif classe=="B":
          return 1
        elif classe=="C":
          return 3
        
    def EN(e):
      '''Nota Normalizada da Escola: Privada Receba 50% dos Pontos da Escola Pública
      
      Pública: EN=10
      Privada: EN=5'''
      
      if e==1:
        return 10
      else:
        return 5
      
    def CurN(c):
      '''Nota Normalizada Dos Cursos: 1 nota diferente para cada curso:
      
      "Ciência de Dados": CurN=10
      "Direito": CurN=4
      "Medicina": CurN=3
      "História": CurN=2
      "Administração": CurN=3
      "Engenharia Biomédica": CurN=7
      "Design": CurN=7
      "Ciência da Computação": CurN=10
      "Filosofia": CurN=1
      '''
      
      if c==1:
        return 10
      elif c==2:
        return 4
      elif c==3:
        return 3
      elif c==4:
        return 2
      elif c==5:
        return 3
      elif c==6:
        return 7
      elif c==7:
        return 7
      elif c==8:
        return 10
      else:
        return 1
      
    def CN(cor):
      
      '''Nota Normalizada da Cor: Estudantes Brancos Recebem 80% da nota dos Estudantes Pretos
      Branco: CN=8
      Preto: CN=10'''
      
      if cor==1:
        return 8
      else:
        return 10
      
    n_renda=self.tbcp['renda'].apply(RN)
    n_escola=self.tbcp['escola'].apply(EN)
    n_curso=self.tbcp['cod_curso'].apply(CurN)
    n_cor=self.tbcp['cor'].apply(CN)
    n_motiv=self.tbcp['motivação']
    notas=pd.DataFrame(columns=['Renda','Escola','Motivação','Curso','Cor'],data=[(a,b,c,d,e) for a,b,c,d,e in 
                                                                              zip(n_renda,n_escola,n_motiv,n_curso,n_cor)],index=self.tbcp.index)
    return notas
  
#Definindo a Classe NovosPesos

#Classe criada com a finalidade de realizar análises separadas sobre como diferentes pesos da Média Ponderada aplicados sobre
#as notas normalizadas dos estudantes influenciam no processo de aprovação ou rejeição destes no processo. Desta forma facilitando
#o entendimento humano dos perfis dos estudantes aprovados, ou não , resultantes da aplicação dos pesos passados como parâmetros,
#além de permitir a checagem manual da frequência de estudantes aprovados ou rejeitados pertencentes a um subgrupo do total.
#Desta forma cada instância da classe inicializada para um array de pesos específicos representa as análises ,unicas, citadas
#para o array de pesos fornecidos.

#Consta também com um método para a criação de um gráfico de rede interativo cujos vértices são os Termos gerados pela multiplicação das notas normalizadas de um estudante qualquer pelo peso da sua respectiva coluna, permitindo assim a análise de quais colunas primárias mais estão influenciando na filtragem dos estudantes.

#O método permite a plotagem dos termos de um estudante único, uma lista de estudantes (Referenciados por uma string que corresponde ao seu RA) ou uma média feita para os termos dos estudantes presentes em 4 Subgrupos:

#(Aprovados-80% da Mp Máxima),
#(Entre 70% e 80% da Mp Máxima),
#(Entre 40% e 70% da Mp Máxima) e
#(Menor que 40% da Mp Máxima)

#as plotagens destas médias representa o perfil de um estudante mediano em relação à sua nota de Mp de cada um destes Subconjuntos e tem como finalidade facilitar a observação de quais colunas primárias alteradas pelos pesos mais influenciam no processo de filtragem dos estudantes.

class NovosPesos():
  def __init__(self,pesos_arr):
    
    '''Classe criada com a finalidade de realizar análises separadas sobre 
       como diferentes pesos da Média Ponderada aplicados sobre as notas normalizadas
       dos estudantes influenciam no processo de aprovação ou rejeição destes no processo.
       Desta forma facilitando o entendimento humano dos perfis dos estudantes aprovados, ou não ,
       resultantes da aplicação dos pesos passados como parâmetros, além de permitir a checagem manual 
       da frequência de estudantes aprovados ou rejeitados pertencentes a um subgrupo do total.
       Desta forma cada instância da classe inicializada para um array de pesos específicos representa as análises
       ,unicas, citadas para o array de pesos fornecidos. Utiliza a Variável Local COLUNASP (Pré-Definida) e a
       Variável local NOTAS (DataFrame do Pandas contendo as notas normalizadas dos estudantes em colunas e como índice
       os RAs destes.) gerada no momento de criação do Módulo (4/05/2022) utilizando a classe NotasNormalizadas
       utilizando o Salário Mínimo vigente no período citado por motivos de otimização, logo para altera-la basta
       mudar o valor da Variável Local no Ambiente de Execução.'''
    
    #Fazendo uma Cópia da Tabela de Colunas Primárias
    colunas_pc=COLUNASP.copy(deep=True)
    #Transformando os valores da Tabela de Notas em um array do Numpy e Calculando a Média Ponderada para cada 
    #estudante utilizando a função dot do Numpy que, como notas tem formato (500,5) e o array de pesos (1,5)
    #Calcula a Soma do produto interno de cada array de Notas pelo array de Pesos,produzindo um array de formato
    #(500,1) que representa a soma NNi*pi, sendo NNi a Nota Normalizada de indice i do estudante e pi o Peso de
    #Índice i do array de pesos. Portanto para obter a Média Ponderada dividimos esse array por um array de de mesmo
    #formato com o valor da soma dos pesos repetidos já que o operador '/' quando aplicados a arrays, de mesma 
    #dimensionalidade,do numpy retorna um array novo em que cada elemento de índice i é a divisão do elemento de índice i 
    #do primeiro array pelo elemento de índice i do segundo array, Logo ,no caso em questão, o valor atribuído à variável
    #mp é um array de formato (500,1) em que cada elemento corresponde à Média Ponderada de cada estudante seguindo o índice
    #da tabela NOTAS que é o mesmo da tabela COLUNASP.
    notas_arr=NOTAS.to_numpy()
    mp=dot(notas_arr,pesos_arr)/array([sum(pesos_arr)]*500)
    #Calculando o Limite de Aprovação Representado como uma Mp a partir de 80% 
    #do valor máximo permitido pelos pesos para Mp
    l_appr=(dot(array([10,10,10,10,10]),pesos_arr)/sum(pesos_arr))*0.8
    colunas_pc['Mp']=mp
    #Calculando os Termos Individuais da Mp para cada estudante de forma semelhante ao cálculo da soma destes
    #porém utilizando a função multiply do numpy para não efetivar a soma e atribuindo os resultados à coluna
    #na cópia de COLUNASP
    termos_i=multiply(pesos_arr,notas_arr)/array([sum(pesos_arr)]*500).reshape([500,1])
    colunas_pc['Termos_p']=[list(i) for i in termos_i]
    colunas_p_arr=colunas_pc.to_numpy()
    #Filtrando os Estudantes aprovados,não aprovados e subconjuntos destes a partir do Limite de Aprovação calculados utilizando
    # a Indexação condicional de arrays por meio da função where do Numpy
    appr,nappr=colunas_p_arr[where(colunas_p_arr[:,-2]>=l_appr)],colunas_p_arr[where(colunas_p_arr[:,-2]<l_appr)]
    dfappr,dfnappr=colunas_pc.iloc[where(colunas_p_arr[:,-2]>=l_appr)],colunas_pc.iloc[where(colunas_p_arr[:,-2]<l_appr)]
    cp={3:(1,2,3,4,5,6,7,8,9),1:(1,2),5:(1,2),4:(1,2)}
    apprfilt=[dfappr.iloc[where(dfappr.to_numpy()[:,k]==a)] for k in cp.keys() for a in cp[k]]
    naoapprfilt=[dfnappr.iloc[where(dfnappr.to_numpy()[:,k]==a)] for k in cp.keys() for a in cp[k]]
    #Criando array no qual os elementos são a quantidade de alunos aprovados ou não aprovados de um determinado
    #subconjunto dos estudantes (Valores específicos de uma das colunas)
    qtd_apprfilt=array([len(i) for i in apprfilt])
    qtd_napprfilt=array([len(i) for i in naoapprfilt])
    #Fazendo a soma de cada elemento i do array dos aprovados com o elemento i dos não aprovados o que resulta
    #em um array contendo a quantidade total de estudantes em determinado subconjunto e Fazendo uma Tabela do Pandas contendo
    #A quantidade de aprovados,quantidade de não aprovados,pct de aprovação e pct de não aprovação para cada subconjunto
    total=qtd_apprfilt+qtd_napprfilt
    freqs_dict={'curso':qtd_apprfilt[:9],'escola':qtd_apprfilt[9:11],'sexo':qtd_apprfilt[11:13],'cor':qtd_apprfilt[13:]}
    freqsn_dict={'curso':qtd_napprfilt[:9],'escola':qtd_napprfilt[9:11],'sexo':qtd_napprfilt[11:13],'cor':qtd_napprfilt[13:]}
    col_por_cod=[{0:"Ciência de Dados",1:"Direito",2:"Medicina",3:"História",
                      4:"Administração",5:"Engenharia Biomédica",6:"Design",7:"Ciência da Computação",8:"Filosofia"},
                   {0:"Pública",1:"Privada"},
                   {0:"Masculino",1:"Feminino"},
                   {0:"Branco",1:"Preto"}]
    freq_df_dict={k:pd.DataFrame({'Aprovados':freqs_dict[k],'Não Aprovados':freqsn_dict[k],
                                'Pct Aprovados':['{}%'.format(round((a/(a+b))*100,2)) for a,b in zip(freqs_dict[k],freqsn_dict[k])],
                                'Pct Não Aprovados':['{}%'.format(round((b/(a+b))*100,2)) for a,b in zip(freqs_dict[k],freqsn_dict[k])]},
                                 index=v.values()) for k,v in zip(freqs_dict.keys(),col_por_cod)}
                
    appr_filt={'Curso':apprfilt[:9],'Escola':apprfilt[9:11],'Sexo':apprfilt[11:13],'Cor':apprfilt[13:]}
    naoappr_filt={'Curso':naoapprfilt[:9],'Escola':naoapprfilt[9:11],'Sexo':naoapprfilt[11:13],'Cor':naoapprfilt[13:]}
    #Atribuindo a Tabela COLUNASP alterada com as colunas 'Mp' e 'Termos_p' dependentes do parâmetro array de pesos
    #e as outras análises calculadas a atributos da Instância inicializada com esse parâmetro
    self.pesos=pesos_arr
    self.tabela_alterada=colunas_pc
    self.qtds=freq_df_dict
    self.aprovados_filtrados=appr_filt
    self.naprovados_filtrados=naoappr_filt
    self.aprovados=dfappr
    self.naprovados=dfnappr
    self.l_appr=l_appr
    self.n_max=mp.max()
      
  def __str__(self):
    return 'Análise de Resultados para Pesos:\nRenda:{}\nEscola:{}\nMotivação:{}\nCurso:{}\nCor:{}'.format(self.pesos[0],self.pesos[1],
                                                                                                           self.pesos[2],self.pesos[3],
                                                                                                           self.pesos[4])
  def __repr__(self):
    return 'Análise de Resultados para Pesos:\nRenda:{}\nEscola:{}\nMotivação:{}\nCurso:{}\nCor:{}'.format(self.pesos[0],self.pesos[1],
                                                                                                           self.pesos[2],self.pesos[3],
                                                                                                           self.pesos[4])
  def qtd_total(self):
    
    '''Função Utilizada para retornar uma Tabela do Pandas cujos índices são Aprovados e Não Aprovados e as
    colunas são "Quantidade" que contém o número de aprovados e não aprovados e "Pct do Total" que contém
    A porcentagem do Total de Estudantes que cada grupo representa.'''
    
    freqs=[len(self.aprovados),len(self.naprovados)]
    total=sum(freqs)
    pcts=['{}%'.format(round((i/total)*100,2)) for i in freqs]
    tabela=pd.DataFrame({'Quantidade':freqs,'Porcentagens':pcts},index=['Aprovados','Não Aprovados'])
    return tabela
  
  def agrupar_por_mp(self):
    
    '''Função Utilizada para retornar um dicionário cujas chaves são os Nomes dos Subgrupos da Tabela Alterada criada
    a partir de limites definidos para o valor da coluna "Mp" e cujos valores são Tabelas do Pandas que contém estes
    respectivos subconjuntos.'''
    
    def group_freq(mp):
      if mp>=self.l_appr:
        return 1
      elif mp>=self.n_max*0.7:
        return 2
      elif mp>=self.n_max*0.4:
        return 3
      else:
        return 4
    grupos=self.tabela_alterada['Mp'].apply(group_freq)
    grupos_dict={k:self.tabela_alterada.loc[grupos.apply(lambda x:x if x==v else None).dropna().index] for k,v in 
                 zip(['Maior que {}'.format(self.l_appr),'Entre {} e {}'.format(self.n_max*0.7,self.l_appr),'Entre {} e {}'.format(self.n_max*0.4,self.n_max*0.7),
                      'Menor que {}'.format(self.n_max*0.4)],[1,2,3,4])}
    medias={}
    for g,df in grupos_dict.items():
      if len(df)!=0:
        medias[g]=np.mean(array([array(i) for i in df['Termos_p'].to_numpy()]),axis=0)
    self.grupo_medias=medias
    return grupos_dict,medias
  
  def grafico_rede(self,RA,mostrar_media=None):
    
    '''Método de Criação de um gráfico de rede interativo cujos vértices são os Termos gerados pela multiplicação 
    das notas normalizadas de um estudante qualquer pelo peso da sua respectiva coluna, 
    permitindo assim a análise de quais colunas primárias mais estão influenciando na filtragem dos estudantes.
    de uma lista de estudantes (Referenciados por uma string na lista "RA" que corresponde ao seu RA) 
    ou uma média feita para os termos dos estudantes presentes nos 4 subgrupos criados pelo método "agrupar_por_mp"
    cuja inclusão pode ser controlada pela varável de controle "mostrar_media" definida como None por Padrão.'''
    
    colunas=['Renda','Escola','Motivação','Curso','Cor','Renda']
    rs=[np.append(a,a[0]) for a in [np.array(self.tabela_alterada.loc[i]['Termos_p']) for i in RA]]
    cpdf_lst=[pd.DataFrame(dict(r=r,theta=colunas)) for r in rs]
    g_lst=[go.Scatterpolar(r=i['r'],theta=i['theta'],fill='toself',name=z,
                         hovertemplate=['Nota {}:{:.2f}'.format(b,a) for a,b in zip(i['r'],i['theta'])],
                         text="RA:{}<br>Total:{:.2f}".format(z,self.tabela_alterada.loc[z]['Mp'])) for i,z in zip(cpdf_lst,RA)]
    fig=go.Figure()
    for g in g_lst:
      fig.add_trace(g)
    if mostrar_media==True:
      try:
        medias_=self.agrupar_por_mp()[1]
        medias={k:np.append(medias_[k],medias_[k][0]) for k in medias_.keys()}
        m_cpdflst=[pd.DataFrame(dict(r=medias[i],theta=colunas)) for i in medias.keys()]
        media_lst=[go.Scatterpolar(r=i['r'],theta=i['theta'],fill='toself',name=z,
                             hovertemplate=['Nota {}:{:.2f}'.format(b,a) for a,b in zip(i['r'],i['theta'])],
                             text="{}<br>Total:{:.2f}".format(z,round(sum(i['r'][:-1]),2))) for i,z in zip(m_cpdflst,['Aprovados: Maior que {:.2f}'.format(self.l_appr),
                                                                                                                  'Entre {:.2f} e {:.2f}'.format(self.n_max*0.7,self.l_appr),
                                                                                                                  'Entre {:.2f} e {:.2f}'.format(self.n_max*0.4,self.n_max*0.7),
                                                                                                                  'Menor que {:.2f}'.format(self.n_max*0.4)])]
      except:
        medias_=self.agrupar_por_mp()[1]
        medias={k:np.append(medias_[k],medias_[k][0]) for k in medias_.keys() if k!=np.nan}
        m_cpdflst=[pd.DataFrame(dict(r=medias[i],theta=colunas)) for i in medias.keys()]
        media_lst=[go.Scatterpolar(r=m_cpdflst[0]['r'],theta=m_cpdflst[0]['theta'],fill='toself',name="Aprovados",
                             hovertemplate=['Nota {}:{:.2f}'.format(b,a) for a,b in zip(m_cpdflst[0]['r'],m_cpdflst[0]['theta'])],
                             text="{}<br>Total:{:.2f}".format('Aprovados',round(sum(m_cpdflst[0]['r'][:-1]),2)))]
      for mg in media_lst:
        fig.add_trace(mg)
    elif mostrar_media=='Aprovados':
      medias_=self.agrupar_por_mp()[1]
      medias={k:np.append(medias_[k],medias_[k][0]) for k in medias_.keys()}
      m_cpdflst=[pd.DataFrame(dict(r=medias[i],theta=colunas)) for i in medias.keys()]
      m_cpdflst=[pd.DataFrame(dict(r=medias[i],theta=colunas)) for i in medias.keys()]
      try:
        media_lst=[go.Scatterpolar(r=i['r'],theta=i['theta'],fill='toself',name=z,
                             hovertemplate=['Nota {}:{:.2f}'.format(b,a) for a,b in zip(i['r'],i['theta'])],
                             text="{}<br>Total:{:.2f}".format(z,round(sum(i['r'][:-1]),2))) for i,z in zip(m_cpdflst,['Aprovados: Maior que {:.2f}'.format(self.l_appr),
                                                                                                                  'Entre {:.2f} e {:.2f}'.format(self.n_max*0.7,self.l_appr),
                                                                                                                  'Entre {:.2f} e {:.2f}'.format(self.n_max*0.4,self.n_max*0.7),
                                                                                                                  'Menor que {:.2f}'.format(self.n_max*0.4)])]
      except:
        media_lst=[go.Scatterpolar(r=m_cpdflst[0]['r'],theta=m_cpdflst[0]['theta'],fill='toself',name="Aprovados",
                             hovertemplate=['Nota {}:{:.2f}'.format(b,a) for a,b in zip(m_cpdflst[0]['r'],m_cpdflst[0]['theta'])],
                             text="{}<br>Total:{:.2f}".format('Aprovados',round(sum(m_cpdflst[0]['r'][:-1]),2)))]
      fig.add_trace(media_lst[0])
    fig.update_layout(
    polar=dict(radialaxis=dict(visible=False,range=[0,5])),
    showlegend=True,
    font={'family':'Monospace','size':18},
    title={
        'text': 'Gráfico de Rede das Notas Ponderadas',
        'y':0.92,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top',
        'font':{'family':'Monospace','size':30,'color':'black'},
        'pad':{'t':-40}},
    legend={'font':{'family':'Monospace','size':18}},
    hoverlabel={'font':{'family':'Monospace','size':16}},
    colorway=pl.colors.qualitative.Pastel,
    autosize=False,
    width=1280,
    height=720)
    fig.update_traces({'line':{'width':2.3},'marker':{'size':8}})
    return fig.show()
#Definindo a Classe Gerador de Pesos

#Classe que tem como funcionalidade ajustar os parâmetros de geração aleatória de pesos utilizando valores
#Aleatórios de uma distribuição Uniforme adquirida pela função do Numpy Numpy.random.uniform()

#Retorna:

#Um Array do Numpy de formato [qtd,5] no qual cada linha representa um Array de Pesos Aleatórios Diferentes, sendo que
#o valor mínimo para qualquer elemento de qualquer um dos arrays é pmin e o valor máximo e pmax. A quantidade de arrays de Pesos Aleatórios geradas é controlada pelo parâmetro qtd que controla o formato do array gerado.

#O array retornado é guardado em um atributo da instância de classe iniciada chamado pesos_possiveis

class GeradorPesos():
  def __init__(self,pmin,pmax,qtd):
    
    '''Retorna um Array do Numpy de formato [qtd,5] no qual cada linha representa um Array de Pesos Aleatórios Diferentes, sendo que
    o valor mínimo para qualquer elemento de qualquer um dos arrays é pmin e o valor máximo e pmax. A quantidade de arrays de
    Pesos Aleatórios geradas é controlada pelo parâmetro qtd ,que controla o formato do array gerado. Os Valores são retirados de
    uma distribuição uniforme utilizando Numpy.random.uniform '''
    
    self.pmin=pmin
    self.pmax=pmax
    self.qtd=qtd
    self.pesos_possiveis=np.random.uniform(pmin,pmax,(qtd,5))
    
  def __str__(self):
    return 'Gerador de Pesos Possíveis para a Média Ponderada Sendo que\nPeso Min:{}\nPeso Max:{}'.format(self.pmin,self.pmax)
  def __repr__(self):
    return 'Gerador de Pesos Possíveis para a Média Ponderada Sendo que\nPeso Min:{}\nPeso Max:{}'.format(self.pmin,self.pmax)
  
#Definindo a Classe TestePeso

#Classe que contém somente uma função de inicialização a qual tem como parâmetro um array de pesos e a partir deste retorna
#um outro array de formato (16,1) contendo as análises realizadas da filtragem dos estudantes resultante da utilização destes
#pesos como os pesos da Média Ponderada das Notas Normalizadas dos estudantes.

#Incluida no Módulo somente como forma de verificação dos resultados obtidos através da chamada da API, já que estas análises estão incorporadas na função 'encontrar_pesos' do arquivo 'main.py' na Implementação da API

class TestePeso():
    def __init__(self,peso_arr):
      '''peso_arr= Numpy Array Shape(5,)
      [P_renda,P_escola,P_motivação,P_curso,P_cor]
      '''
      notas_arr=NOTAS.to_numpy()
      mp=dot(notas_arr,peso_arr)/array([sum(peso_arr)]*500)
      l_appr=(dot(array([10,10,10,10,10]),peso_arr)/sum(peso_arr))*0.8
      COLUNASP['Mp']=mp
      colunas_p_arr=COLUNASP.to_numpy()
      appr,nappr=colunas_p_arr[where(colunas_p_arr[:,-1]>=l_appr)],colunas_p_arr[where(colunas_p_arr[:,-1]<l_appr)]
      cp={3:(1,2,3,4,5,6,7,8,9),4:(1,2),5:(1,2),1:(1,2)}
      apprfilt=array([len(appr[where(appr[:,k]==a)]) for k in cp.keys() for a in cp[k]])
      naoapprfilt=array([len(nappr[where(nappr[:,k]==a)]) for k in cp.keys() for a in cp[k]])
      total=apprfilt+naoapprfilt
      self.pdarr=append(array((len(appr))),apprfilt/total)
      self.l_appr=l_appr
    
#Definindo a Classe TestarPesoAPI

#Classe utilizada para fazer múltiplas chamadas simultâneas à API de testagem dos pesos, para acelerar a busca pelos pesos filtrados, utilizando a função ThreadPoolExecutor do Módulo concurrent.features do Python ; Lidar com erros retornados pela API e formatar as múltiplas respostas bem-sucedidas em uma resposta unificada correspondente à agregação de todas as respostas obtidas
#paralelamente.

#Parâmetros de Inicialização:

#pesos_por_vm= Quantidade de Pesos que se deseja testar por chamada da API, que executa em uma única MV no ambiente do Google Cloud

#limites= Array de Condições das filtragens realizadas dos estudantes quando o peso que está sendo testado é usado como peso da Média Ponderada das Notas Normalizadas. Passado para a chamada da API em forma de parâmetro na URL.

#n_vms= Quantidade de chamadas simultâneas que se deseja realizar à API, sendo que cada uma será executada em uma MV diferente no ambiente do Google Cloud.

class TestarPesoAPI():
  def __init__(self,pesos_por_vm,limites,n_vms):
    
    '''Inicializa uma instância da classe TestarPesoAPI que armazena os parâmetros de inicialização em
    atributos desta.
    Parâmtros:
    pesos_por_vm= Quantidade de Pesos que se deseja testar por chamada da API, 
    que executa em uma única MV no ambiente do Google Cloud
    
    limites= Array de Condições das filtragens realizadas dos estudantes quando
    o peso que está sendo testado é usado como peso da Média Ponderada das Notas Normalizadas.
    Passado para a chamada da API em forma de parâmetro na URL.
    
    n_vms= Quantidade de chamadas simultâneas que se deseja realizar à API,
    sendo que cada uma será executada em uma MV diferente no ambiente do Google Cloud.
    '''
    
    self.ppvm=pesos_por_vm
    self.limites=limites
    self.nvms=n_vms
    
  def chamar_api(url):
    
    '''Função que será utilizada pelo ThreadPoolExecutor;Realiza uma única chamada à
    API e retorna o resultado obtido caso a execução tenha sido bem sucedida (Código 200)
    e pausa a execução do programa por 5 segundos (Tempo Médio da chamada) caso não tenha
    (Código diferente de 200)'''
    
    req=requests.get(url)
    if req.status_code==200:
      return req
    else:
      time.sleep(5)
      nreq=requests.get(url)
      return nreq
  def requests_simultaneos(n_requests,url_lst):
    
    '''Funçao  que cria uma fila de execução das chamadas e gerencia a acquisição do resultado destas quando 
    completadas e atualização da fila de chamadas a serem executadas, executa uma chamada diferente 
    por Thread do CPU da máquina de execução podendo-se especificar o número máximo de Threads a se utilizar.'''
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_requests) as pool:
      response_lst= list(pool.map(TestarPesoAPI.chamar_api,url_lst))
    return [i for i in response_lst]
  
  def comecar_teste(self):
    
    '''Método que incializa a execução do ThreadPoolWorker com os parâmetros de inicialização fornecidos na
    criação da instância de classe e realiza a formatação e agregação dos resultados obtidos pelas chamadas
    paralelas em uma única resposta unificada.'''
    
    url='http://us-central1-pessoal-1802.cloudfunctions.net/econtrar-pesos?qtd_pesos={}&limites={}'.format(self.ppvm,self.limites)
    response_lst=TestarPesoAPI.requests_simultaneos(self.nvms,[url]*self.nvms)
    response_unificada={}
    erros=[]
    for resp,ind in zip(response_lst,range(len(response_lst))):
      if ind==0:
        response_unificada['qtd_pesos_testados']=int(resp.json()['qtd_pesos_testados'])
        response_unificada['pesos']=resp.json()['pesos']
        response_unificada['pesos_encontrados']=int(resp.json()['pesos_encontrados'])
      else:
        try:
          response_unificada['qtd_pesos_testados']+=int(resp.json()['qtd_pesos_testados'])
          response_unificada['pesos']+=';'+ resp.json()['pesos']
          response_unificada['pesos_encontrados']+=int(resp.json()['pesos_encontrados'])
        except:
           erros.append(resp)
    response_unificada['limites']=response_lst[0].json()['limites']
    R_c1=response_unificada['pesos'].replace(';','/').replace('\n','').split(',')
    R_c2=[r.split('/') for  r in R_c1]
    R_c3=[a for r in R_c2 for a in r if len(a)!=0]
    R_c4=[a.replace('[','').replace(']','').split(' ') for a in R_c3]
    R_c5=[]
    for i in R_c4:
      parr=[]
      for a in i:
        if a!='':
          parr.append(float(a))
      R_c5.append(np.array(parr))
    pesosap=np.array(R_c5)
    response_unificada['pesos']=pesosap
    return response_unificada,erros