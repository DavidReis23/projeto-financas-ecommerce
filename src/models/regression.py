import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


def executar_regressao(df):

    print("\n====== INICIANDO REGRESSÃO LINEAR MÚLTIPLA ======")

    colunas = [
        "review_score",
        "tempo_entrega_dias",
        "payment_value",
    ]

    dados = df[colunas].dropna().copy()

    print(f"-> Registros utilizados: {len(dados)}")

    # Variável resposta Y
    y = dados["review_score"]

    # Variáveis preditoras X1 e X2
    X = dados[
        [
            "tempo_entrega_dias",
            "payment_value",
        ]
    ]

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print(
        f"-> Treino: {len(X_treino)} registros | "
        f"Teste: {len(X_teste)} registros"
    )

    modelo = LinearRegression()

    modelo.fit(
        X_treino,
        y_treino,
    )

    beta_0 = modelo.intercept_

    beta_tempo = modelo.coef_[0]

    beta_pagamento = modelo.coef_[1]

    print("\n--- COEFICIENTES ESTIMADOS ---")

    print(f"β0 (Intercepto): {beta_0:.6f}")

    print(
        "β1 (tempo_entrega_dias): "
        f"{beta_tempo:.6f}"
    )

    print(
        "β2 (payment_value): "
        f"{beta_pagamento:.6f}"
    )

    y_pred = modelo.predict(X_teste)

    r2 = r2_score(
        y_teste,
        y_pred,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_teste,
            y_pred,
        )
    )

    print("\n--- QUALIDADE DO MODELO ---")

    print(f"R²: {r2:.4f}")

    print(f"RMSE: {rmse:.4f}")

    print("\n--- INTERPRETAÇÃO CETERIS PARIBUS ---")

    print(
        "β1: Mantendo o valor da compra constante, "
        f"cada dia adicional de entrega está associado "
        f"a uma variação de {beta_tempo:.6f} "
        "ponto na avaliação média."
    )

    print(
        "\nβ2: Mantendo o tempo de entrega constante, "
        f"cada R$ 1 adicional no pagamento está associado "
        f"a uma variação de {beta_pagamento:.6f} "
        "ponto na avaliação média."
    )

    return {
        "modelo": modelo,
        "beta_0": beta_0,
        "beta_tempo": beta_tempo,
        "beta_pagamento": beta_pagamento,
        "r2": r2,
        "rmse": rmse,
    }


if __name__ == "__main__":

    df = pd.read_csv(
        "dados_limpos_final.csv"
    )

    executar_regressao(df)