# -*- coding: utf-8 -*-
"""m4-algoritmos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bsKG0Y1crjfc-9oi_5lIOtgzs-jhCBj7

**Grupo 11 - Algoritmos e Data Science**

Emanuel Luz de Abreu<br>
Leidiana de Carli<br>
Lissandra Dutra<br>
Vinícius Silva Salinas

#### **Business Understanding**

*Turnover* ou rotatividade de mão-de-obra em uma companhia é caracterizado pelo fluxo de entradas e saídas de pessoas em uma organização. Dependendo da taxa que este indicador representa, outros indicadores como grau de satisfação de funcionários, custos com admissão e demissão dos mesmos, treinamentos aplicados e até mesmo a satisfação de clientes tem seus resultados diretamente influenciados.  

Através do website Kaggle (*https://www.kaggle.com/kmldas/hr-employee-data-descriptive-analytics*) foi obtido o dataset "HR Employee Analytics". Os atributos e registros presentes no mesmo serão analisados e utilizados em um **algoritmo de regressão** de forma a prever o nível de satisfação de colaboradores da empresa contemplatada mediante a variável alvo cujos valores vão de 0 (não satisfeitos) a 1 (satisfeitos).

#### **Data Understanding**

Os dados utilizados foram disponibilizados na plataforma Kaggle pelo usuário Kamal Das. A base refere-se a dados do setor de recursos humanos da empresa MNC e podem ser encontrados no link disponibilizado no tópico acima.

A base é composta de 1 arquivo com 14599 registros e encontra-se no formato xlsx. Os dados estão distribuídos em 11 colunas, que correspondem a:

**`Emp_Id`:** um código de identificação único atribuído a cada funcionário, composto de 3 letras e 5 números

**`satisfaction_level`:** um número de 0 a 1 que expressa em porcentagem o nível de satisfação de cada funcionário, sendo 1 muito satisfeito e 0 insatisfeito

**`last_evaluation`:** um número de 0 a 1 que expressa o tempo em anos desde a última avaliação

**`number_project`:** o número de projetos em que um funcionário está trabalhando

**`average_montly_hours`:** a média de horas trabalhadas nos últimos três meses

**`time_spend_company`:** tempo que o funcionário leva se deslocando para o escritório em horas

**`Work_accident`:** se o funcionário se envolveu em um acidente de trabalho, sendo 0 para não e 1 para sim

**`left`:** se o funcionário já deixou a empresa, sendo 0 para não e 1 para sim

**`promotion_last_5years`:** se o funcionário foi promovido nos últimos 5 anos, sendo 0 para não e 1 para sim

**`Department`:** departamento em que o funcionários está trabalhando

**`salary`:** salário categorizado em low, medium e high
"""

# Importação de bibliotecas
import pandas as pd

# Leitura dos dados. É necessário fazer o upload do arquivo que está disponível no Kaggle
dados = pd.read_excel('HR_Employee_Data.xlsx')

"""**Explorando os dados**"""

# Verificando os tipos de dados
dados.dtypes

# Quantidade de linhas e colunas
dados.shape

# Resumo estatítico dos dados
print(dados.describe())

# Média do grau de satisfação
dados["satisfaction_level"].mean()

# Menor grau de satisfação
dados["satisfaction_level"].min()

# Maior grau de satisfação
dados["satisfaction_level"].max()

# Desvio padrão dos valores de grau de satisfação
dados["satisfaction_level"].std()

# Média de tempo desde a última avaliação
dados["last_evaluation"].mean()

# Verificando o número de promoções nos últimos 5 anos
dados["promotion_last_5years"].sum()

# Análise de correlações entre variáveis
pd.crosstab(dados["salary"],dados["promotion_last_5years"],margins=True)

# Análise de correlações entre variáveis
pd.crosstab(dados["number_project"],dados["promotion_last_5years"],margins=True)

"""**Qualidade dos dados**"""

# Verificando se há campos nulos
dados.isnull().sum()

# Importação de mais bibliotecas
!pip install seaborn --upgrade
import seaborn as sns
import numpy as np

# Análise de Correlação por Mapa de Calor

sns.heatmap(dados.corr(), annot=True, vmin=-1, vmax=1, cmap='coolwarm')

# Correlação pelo coeficiente de Pearson da Satisfação VS Promoção nos Últimos 5 Anos

satisfaction = dados["satisfaction_level"]
promotion = dados["promotion_last_5years"]
correlation_A = satisfaction. corr(promotion)
print(correlation_A)

# Correlação pelo coeficiente de Pearson da Satisfação VS Número de Projetos
numero_projetos = dados["number_project"]
satisfaction = dados["satisfaction_level"]
correlation_B = numero_projetos. corr(satisfaction)
print(correlation_B)

"""#### **Data Preparation**"""

# Remoção de uma das colunas, que atrapalhará o desenvolvimento do modelo de regressão, e é desnecessária para as análises
dados = dados.drop(columns=['Emp_Id'])

# Padronização dos nomes das colunas e alteração do tipo de duas variáveis qualitativas para 'category'
dados = dados.rename(columns = {'Work_accident':'work_accident','Department':'department'})
dados['department'] = dados['department'].astype('category')
dados['salary'] = dados['salary'].astype('category')
dados.dtypes

# Visualização dos dados tratados
dados.head()

# Entendendo variáveis dummies
dados['salary'].value_counts()

# Entendendo variáveis dummies
dados['department'].value_counts()

"""#### **One Hot Encoder**<br>
Necessário para uso da variável qualitativa nominal `department` no modelo
"""

# Instalação de um módulo a ser utilizado
!pip install category_encoders

# Transformando a coluna department
from category_encoders.one_hot import OneHotEncoder
enc = OneHotEncoder(cols=['department'], use_cat_names=True)
dados = enc.fit_transform(dados)

# Visualizando o resultado
dados.head()

"""#### **Ordinal Encoder**<br>
Necessário para uso da variável qualitativa ordinal `salary` no modelo
"""

# Transformando a coluna salary
from category_encoders.one_hot import OrdinalEncoder
enc = OrdinalEncoder(cols=['salary'])
dados = enc.fit_transform(dados)

# Visualizando o resultado
dados.head()

"""#### **Modeling**

Variável alvo: satisfaction_level
"""

# Separando as variáveis entre preditoras e alvo
alvo = dados['satisfaction_level']
pred = dados.drop('satisfaction_level', axis = 1)

# Criando os conjuntos de dados de treino e teste
from sklearn.model_selection import train_test_split

pred_treino, pred_teste, alvo_treino, alvo_teste = train_test_split(pred, alvo, test_size = 0.2)

# Criação do modelo
from sklearn.ensemble import RandomForestRegressor
mdl = RandomForestRegressor(n_estimators=100)
mdl.fit(pred_treino, alvo_treino)

# Analisando a importância de cada variável preditora para a geração de valor da variável alvo
mdl.feature_importances_

# Aplicação do modelo para o conjunto de dados teste
previsoes = mdl.predict(pred_teste)
previsoes

"""#### **Evaluation**"""

# Avaliação do modelo com MAE
from sklearn.metrics import mean_absolute_error
mean_absolute_error(alvo_teste, previsoes)

# Verificação e comparação dos resultados dos três primeiros registros do conjunto de dados teste
previsoes[0:3]

alvo_teste[0:3]

# Aplicação do modelo em valores que o usuário pode definir livremente
previsao_amostras = mdl.predict([[0.63,4,135,2,1,0,0,1,0,0,0,0,0,0,0,0,0,3]])
previsao_amostras

"""#### **Final Conclusion**

O conjunto de dados utilizado para estudo se mostrou de  boa qualidade, no qual não foi necessário grandes intervenções para tratar a base e limpar registros inválidos. Na etapa de limpeza não foram identificadas anomalias, como valores nulos ou inconsistentes, ou ainda discrepâncias que poderiam comprometer a análise como um todo, foram feitos pequenos ajustes como a exclusão do campo `Emp_Id` que identifica um funcionário mas não influenciaria a análise.

Em relação aos negócios, algumas questões foram analisadas, como:

Existe alguma relação entre a  satisfação  de um funcionário com o número de
projetos executados?

Nessa questão foi identificada uma correlação negativa, ou seja, a satisfação de um funcionário está, de maneira inversamente proporcional, relacionada ao número de projetos, nos dando algumas ideias que podem ser exploradas pelo setor de Recursos Humanos da empresa, como: esta baixa satisfação do funcionário pode estar ligada à uma sobrecarga de trabalho gerando assim uma insatisfação e por consequência, em uma próxima análise, uma baixa qualidade de serviço.

Outra questão analisada foi: existe correlação entre a satisfação de um funcionário com o fato dele ser ou não promovido nos últimos 5 anos?

Nesse caso, tivemos uma correlação positiva, mas não tão satisfatória como prevíamos, pois obtivemos um índice relativamente baixo, igual a 0.025. Este valor obtido  significa que não existe um único fator decisivo nessa amostra de dados, e sim uma combinação de variáveis que contribui para a satisfação do funcionário.

Por ultimo, concluímos que o algoritmo desenvolvido pode **auxiliar tomadores de decisão a planejar políticas de RH** visando o aumento dos índices de satisfação de colaboradores, tempo de empresa, e redução de turn-over. Com as  análises geradas por esse algoritmo também é possível auxiliar no planejamento de políticas de recrutamento e a melhoria contínua dos profissionais da companhia.
"""