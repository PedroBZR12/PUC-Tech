#Importação de bibliotecas
#para manipulacao de dados e criacao de graficos
from matplotlib.widgets import Button   #uso para criar um botao para alternar entre proximo e anterior
import pandas as pds #Carregar dados e manipula-los
import matplotlib.pyplot as plts #criar graficos
import os #verificação do caminho dos arquivos para carregar.

CAMINHO_ARQUIVO = "student_preferences_extended.csv"
# Tenta carregar o arquivo
if not os.path.exists(CAMINHO_ARQUIVO):
    print(f"Arquivo '{CAMINHO_ARQUIVO}' não encontrado. Por favor, envie o arquivo.")
else:
    dados = pds.read_csv(CAMINHO_ARQUIVO)

    #verificando os dados
    #print(dados.head())
    #print(dados.columns)
    #print(dados.info())
    #print(dados.isnull().sum())

    #tratamento de dados, excluindo colunas que nao contribuem para insights.
    dadosL = dados.drop(columns=['id_aluno', 'tempo_resposta', 'horas_estudo_dia', 'comentario'])

    #como somente esta coluna possui valores nulos, iremos tratar apenas esta.
    dadosL['framework_preferido']  = dadosL['framework_preferido'].fillna("Não informado")

    #verificando se os valores foram tratados corretamente
    #print(dadosL.isnull().sum())
    #print(dadosL.describe())

    #Conta a quantidade de vezes que a mesma linguagem aparece
    linguagens = dadosL['linguagem_preferida'].value_counts()

    #satisfacao ao longo do curso, agrupamos os dados de semestre e
    #satisfacao sobre o curso, logo depois fazemos a media sobre.
    pesquisaDeSatisfacaoSemestre = dadosL.groupby('semestre')['satisfacao_curso'].mean()

    #verificar se ha uma melhora ou nao nos casos em que os alunos estudam em grupo
    mediaGrupo = dadosL.groupby('estuda_em_grupo')['media_geral'].mean()


    #verificar quais sao as areas de interesse mais populares entre os alunos
    pesquisaAreaDeInteresse = dadosL['area_interesse'].value_counts()

    #verificar quais sao os horarios mais frequentes de estudo dos alunos
    horariosEstudo = dadosL['horario_estudo'].value_counts()


    #será o gráfico de linguagens mais populares
    def graficoLinguagens(var):
        #limpa a janela
        var.clear()
        #cria o gráfico em estilo pizza começando do ângulo 140 e a porcentagem representada
        #para cada linguagem possuindo 1 casa decimal.
        var.pie(linguagens.values, labels = linguagens.index, autopct='%1.1f%%')
        #define o título do gráfico como linguagens mais populares
        var.set_title("Linguagens mais populares", fontsize=16, fontweight='bold')
        
        #grafico de satisfacao ao longo do curso
    def graficoSatisfacaoCurso(var):
        var.clear()
        var.bar(pesquisaDeSatisfacaoSemestre.index, pesquisaDeSatisfacaoSemestre.values)
        var.set_xlabel("Semestre")
        var.set_ylabel("Média da satisfação")
        var.set_title("Satisfação ao longo do curso", fontsize=16, fontweight='bold')

    def graficoMediaGrupo(var):
        var.clear()
        labels = ['Não Estuda em Grupo', 'Estuda em Grupo']
        valores = [mediaGrupo[False], mediaGrupo[True]]
        var.barh(labels, valores)
        var.set_ylabel("Média Geral")
        var.set_title("Impacto do Estudo em Grupo na Média Geral", fontsize=16, fontweight='bold')

    def graficoPesquisaAreaInteresse(var):
        var.clear()
        var.pie(pesquisaAreaDeInteresse.values, labels=pesquisaAreaDeInteresse.index, autopct='%1.1f%%')
        var.set_title("Áreas de Interesse")


    def graficoHorarioEstudo(var):
        var.clear()
        var.pie(horariosEstudo.values, labels=horariosEstudo.index, autopct='%1.1f%%')
        var.set_title("Horários de estudos preferidos")


    graficos = [graficoLinguagens, graficoSatisfacaoCurso, 
                graficoMediaGrupo, graficoPesquisaAreaInteresse,
                graficoHorarioEstudo]

    # Configuração da figura e botão
    fig, var = plts.subplots(figsize=(10,6))
    plts.subplots_adjust(bottom=0.2)
    indice_grafico = [0]

    # Botões
    var_button_prox = plts.axes([0.8, 0.05, 0.1, 0.075])  # x, y, largura, altura
    botao_prox = Button(var_button_prox, 'Próximo')     #inicializa o botão próximo

    var_button_prev = plts.axes([0.6, 0.05, 0.08, 0.075]) #mesmo do button_prox
    botao_prev = Button(var_button_prev, 'Anterior')    #inicializa o botão anterior

        #função para definir a ação do botão anterior quando for clicado
    def proximo(event):
        indice_grafico[0] = (indice_grafico[0] + 1) % len(graficos)
        graficos[indice_grafico[0]](var)
        plts.draw()
        
        #função para definir a ação do botão anterior quando for clicado
    def anterior(event):
        indice_grafico[0] = (indice_grafico[0] - 1) % len(graficos)
        graficos[indice_grafico[0]](var)
        plts.draw()

    botao_prox.on_clicked(proximo) #se o botao proximo for clicado, vai para o proximo grafico
    botao_prev.on_clicked(anterior) #se o botao anterior for clicado, vai para o grafico anterior
    #mostra o primeiro gráfico
    graficos[indice_grafico[0]](var)
    plts.show()