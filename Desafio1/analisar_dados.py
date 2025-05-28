from matplotlib.widgets import Button
import pandas as pds #Carregar dados
import matplotlib.pyplot as plts
import seaborn as sbns
import numpy as np

dados = pds.read_csv("student_preferences_extended.csv")


#verificando os dados
#print(dados.head())
#print(dados.columns)
#print(dados.info())
#print(dados.isnull().sum())

#dadosL = dados limpos (tratamento dos dados)
dadosL = dados.drop(columns=['id_aluno', 'tempo_resposta', 'horas_estudo_dia', 'comentario'])

#como somente esta coluna possui valores nulos, iremos tratar apenas esta.
dadosL['framework_preferido']  = dadosL['framework_preferido'].fillna("Não informado")

#verificando se os valores foram tratados corretamente
#print(dadosL.isnull().sum())

#print(dadosL.describe())

#Conta a quantidade de vezes que a mesma linguagem aparece
linguagens = dadosL['linguagem_preferida'].value_counts()

#satisfacao ao longo do curso
pesquisaDeSatisfacao = dadosL.groupby('semestre')['satisfacao_curso'].mean()

#verificar se ha uma melhora ou nao nos casos em que os alunos estudam em grupo
mediaGrupo = dadosL.groupby('estuda_em_grupo')['media_geral'].mean().sort_index()

#será o gráfico de linguagens mais populares
def graficoPizza(var):
    #limpa a janela
    var.clear()
    #cria o gráfico em estilo pizza começando do ângulo 140 e a porcentagem representada
    #para cada linguagem possuindo 1 casa decimal.
    var.pie(linguagens.values, labels = linguagens.index, autopct='%1.1f%%', startangle=140)
    #define o título do gráfico como linguagens mais populares
    var.set_title("Linguagens mais populares")
    
def graficoBarrasVerticais(var):
    var.clear()
    
    x = pesquisaDeSatisfacao.values
    y = pesquisaDeSatisfacao.index
    x1 = np.round(y, 2)
    sbns.barplot(x=x1, y=y, ax=var)
    var.set_xlabel("Satisfação Média")
    var.set_ylabel("Semestre")
    var.set_title("Satisfação por Semestre")

def graficoBarrasHorizontais(var):
    var.clear()
    labels = ['Não Estuda em Grupo', 'Estuda em Grupo']
    valores = mediaGrupo.values
    sbns.barplot(x=valores, y=labels, ax=var)
    var.set_ylabel("Média Geral")
    var.set_title("Impacto do Estudo em Grupo na Média Geral")

graficos = [graficoPizza, graficoBarrasVerticais, graficoBarrasHorizontais]

# Configuração da figura e botão
fig, var = plts.subplots()
plts.subplots_adjust(bottom=0.2)
indice_grafico = [0]  # Usar lista para mutabilidade

# Botão
var_button = plts.axes([0.8, 0.05, 0.1, 0.075])  # x, y, largura, altura
botao = Button(var_button, 'Próximo')

def proximo(event):
    indice_grafico[0] = (indice_grafico[0] + 1) % len(graficos)
    graficos[indice_grafico[0]](var)
    plts.draw()

botao.on_clicked(proximo)

#mostra o primeiro gráfico (em pizza)
graficos[indice_grafico[0]](var)
plts.show()