# Importando as bibliotecas necessárias
from sklearn.datasets import make_classification     # Para criar dados sintéticos de transações
from sklearn.model_selection import train_test_split # Para dividir dados em treino/teste
from sklearn.preprocessing import StandardScaler     # Para normalizar os dados
from sklearn.ensemble import RandomForestClassifier  # Algoritmo de machine learning
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report


# 1. GERAÇÃO DOS DADOS SINTÉTICOS

# Criando um dataset sintético que simula transações financeiras
X, y = make_classification(
    n_samples=10000,        # total de transações criadas
    n_features=20,          # número de características por transação (ex: valor, hora, local)
    n_informative=15,        # features realmente úteis para detectar fraude
    n_redundant=2,          # features derivadas/redundantes das informativas
    n_classes=2,            # legítima (0) ou fraudulenta (1)
    weights=[0.97],         # 97% das amostras são da classe 0 (3% fraudes - mais realista)
    flip_y=0,               # sem ruído aleatório nas classes
    random_state=42,        # garante resultados reproduzíveis
    class_sep=2.0          # aumenta a separabilidade entre as classes e facilita a detecção de fraudes
)

# 2. DIVISÃO DOS DADOS EM TREINO E TESTE

# Dividindo os dados: 80% para treinar o modelo, 20% para testá-lo
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% dos dados para teste
    random_state=42,    # para garantir resultados reproduzíveis
    stratify=y          # para manter a proporção de classes no treino e teste
)

# 3. PRÉ-PROCESSAMENTO: NORMALIZAÇÃO DOS DADOS

# Criando o objeto que fará a normalização (média=0, desvio padrão=1)
scaler = StandardScaler()


X_train = scaler.fit_transform(X_train)  # ajusta o scaler no treino e transforma os dados de treino
X_test = scaler.transform(X_test)        # transforma os dados de teste com o scaler já ajustado


# 4. TREINAMENTO DO MODELO

# Criando e treinando o modelo Random Forest
# Random Forest combina várias árvores de decisão para melhor performance
# class_weight='balanced' ajuda com datasets desbalanceados
model = RandomForestClassifier(
    n_estimators=200,           # número de árvores
    max_depth=10,               # profundidade máxima das árvores
    class_weight='balanced',    # balanceia automaticamente as classes
    random_state=42
)
model.fit(X_train, y_train)

# Fazendo predições nos dados de teste
y_pred = model.predict(X_test)

# 5. AVALIAÇÃO DO DESEMPENHO

# Calculando as métricas de avaliação
acc = accuracy_score(y_test, y_pred)     # Porcentagem total de acertos
f1 = f1_score(y_test, y_pred)           # Média harmônica entre precisão e recall
cm = confusion_matrix(y_test, y_pred)    # Matriz que mostra acertos e erros detalhados
report = classification_report(y_test, y_pred)  # Relatório completo com todas as métricas

# Exibindo os resultados
print(f"Acurácia: {acc:.4f}")
print(f"F1-score: {f1:.4f}")

print(report)

print("Matriz de confusão:")
print(cm)


# 6. ANÁLISE FINAL E INTERPRETAÇÕES


print("\n" + "="*50)
print("ANÁLISE FINAL DOS RESULTADOS")
print("="*50)

# Extraindo valores da matriz de confusão para análise detalhada
# Formato: [[TN, FP], [FN, TP]]
tn, fp, fn, tp = cm.ravel()

print(f"\nInterpretação da Matriz de Confusão:")
print(f"• Verdadeiros Negativos (TN): {tn:,} - Transações legítimas identificadas corretamente")
print(f"• Falsos Positivos (FP): {fp:,} - Transações legítimas classificadas como fraude")
print(f"• Falsos Negativos (FN): {fn:,} - Fraudes que passaram despercebidas")
print(f"• Verdadeiros Positivos (TP): {tp:,} - Fraudes detectadas corretamente")

# Calculando métricas adicionais para interpretação
precision = tp / (tp + fp) if (tp + fp) > 0 else 0    # Das previstas como fraude, quantas eram realmente
recall = tp / (tp + fn) if (tp + fn) > 0 else 0       # Das fraudes reais, quantas foram detectadas
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0  # Das legítimas reais, quantas foram identificadas

print(f"\nMétricas Detalhadas:")
print(f"• Precisão: {precision:.4f} ({precision*100:.2f}%) - Das predições de fraude, quantas eram corretas")
print(f"• Recall: {recall:.4f} ({recall*100:.2f}%) - Das fraudes reais, quantas foram detectadas")
print(f"• Especificidade: {specificity:.4f} ({specificity*100:.2f}%) - Das transações legítimas, quantas foram identificadas")


# Avaliação final do desempenho
if f1 > 0.7:
    status = "EXCELENTE - Modelo pronto para produção"
elif f1 > 0.5:
    status = "MODERADO - Modelo precisa de ajustes"
else:
    status = "INSUFICIENTE - Modelo precisa ser reformulado"

print(f"\nAvaliação Final: {status}")
print(f"F1-Score: {f1:.4f} | Acurácia: {acc:.4f}")