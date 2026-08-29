import pandas as pd

from sklearn.model_selection import (
    GridSearchCV,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def avaliar_modelo(nome, modelo, X_teste, y_teste):


    previsoes = modelo.predict(X_teste)

    matriz = confusion_matrix(
        y_teste,
        previsoes,
    )

    acuracia = accuracy_score(
        y_teste,
        previsoes,
    )

    precisao = precision_score(
        y_teste,
        previsoes,
        zero_division=0,
    )

    recall = recall_score(
        y_teste,
        previsoes,
        zero_division=0,
    )

    f1 = f1_score(
        y_teste,
        previsoes,
        zero_division=0,
    )

    print(f"\n====== {nome} ======")

    print("\nMatriz de Confusão:")
    print(matriz)

    print(f"\nAcurácia: {acuracia:.4f}")
    print(f"Precisão: {precisao:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")

    return {
        "matriz_confusao": matriz,
        "acuracia": acuracia,
        "precisao": precisao,
        "recall": recall,
        "f1_score": f1,
    }


def executar_classificacao(
    df,
    tamanho_amostra=30000,
):

    print(
        "\n====== INICIANDO MODELAGEM "
        "PREDITIVA DE CLASSIFICAÇÃO ======"
    )

    dados = df.copy()

    colunas_data = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for coluna in colunas_data:
        dados[coluna] = pd.to_datetime(
            dados[coluna],
            errors="coerce",
        )

    dados["atrasado"] = (
        dados["order_delivered_customer_date"]
        > dados["order_estimated_delivery_date"]
    ).astype(int)

    # Prazo prometido ao cliente no momento
    # em que a compra foi realizada.
    dados["prazo_estimado_dias"] = (
        dados["order_estimated_delivery_date"]
        - dados["order_purchase_timestamp"]
    ).dt.days

    colunas_modelo = [
        "payment_value",
        "payment_installments",
        "prazo_estimado_dias",
        "atrasado",
    ]

    dados = (
        dados[colunas_modelo]
        .dropna()
        .copy()
    )

    # Elimina eventuais prazos inconsistentes
    dados = dados[
        dados["prazo_estimado_dias"] >= 0
    ]

    print(
        f"-> Registros disponíveis: {len(dados)}"
    )

    print("\nDistribuição da variável alvo:")

    print(
        dados["atrasado"]
        .value_counts()
        .sort_index()
    )

    print(
        "\n0 = entregue no prazo"
        "\n1 = entregue atrasado"
    )

    if len(dados) > tamanho_amostra:

        dados, _ = train_test_split(
            dados,
            train_size=tamanho_amostra,
            stratify=dados["atrasado"],
            random_state=42,
        )

        print(
            f"\n-> Amostra estratificada utilizada "
            f"na modelagem: {len(dados)} registros"
        )

    X = dados[
        [
            "payment_value",
            "payment_installments",
            "prazo_estimado_dias",
        ]
    ]

    y = dados["atrasado"]

    (
        X_treino,
        X_teste,
        y_treino,
        y_teste,
    ) = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(
        f"\n-> Treino: {len(X_treino)} registros"
    )

    print(
        f"-> Teste: {len(X_teste)} registros"
    )

    pipeline_logistica = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "modelo",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    parametros_logistica = {
        "modelo__C": [
            0.1,
            1.0,
            10.0,
        ],
        "modelo__class_weight": [
            None,
            "balanced",
        ],
    }

    print(
        "\n-> Executando GridSearchCV "
        "para Regressão Logística..."
    )

    grid_logistica = GridSearchCV(
        estimator=pipeline_logistica,
        param_grid=parametros_logistica,
        cv=3,
        scoring="f1",
        n_jobs=-1,
    )

    grid_logistica.fit(
        X_treino,
        y_treino,
    )

    print(
        "\nMelhores parâmetros "
        "da Regressão Logística:"
    )

    print(
        grid_logistica.best_params_
    )

    print(
        f"Melhor F1 médio na validação cruzada: "
        f"{grid_logistica.best_score_:.4f}"
    )

    resultados_logistica = avaliar_modelo(
        "REGRESSÃO LOGÍSTICA",
        grid_logistica.best_estimator_,
        X_teste,
        y_teste,
    )

    pipeline_knn = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "modelo",
                KNeighborsClassifier(
                    n_jobs=-1,
                ),
            ),
        ]
    )

    parametros_knn = {
        "modelo__n_neighbors": [
            5,
            11,
        ],
        "modelo__weights": [
            "uniform",
            "distance",
        ],
    }

    print(
        "\n-> Executando GridSearchCV "
        "para KNN..."
    )

    grid_knn = GridSearchCV(
        estimator=pipeline_knn,
        param_grid=parametros_knn,
        cv=3,
        scoring="f1",
        n_jobs=-1,
    )

    grid_knn.fit(
        X_treino,
        y_treino,
    )

    print(
        "\nMelhores parâmetros do KNN:"
    )

    print(
        grid_knn.best_params_
    )

    print(
        f"Melhor F1 médio na validação cruzada: "
        f"{grid_knn.best_score_:.4f}"
    )

    resultados_knn = avaliar_modelo(
        "KNN",
        grid_knn.best_estimator_,
        X_teste,
        y_teste,
    )

    print(
        "\n====== COMPARAÇÃO FINAL ======"
    )

    print(
        "\nRegressão Logística:"
        f"\nAcurácia: "
        f"{resultados_logistica['acuracia']:.4f}"
        f"\nPrecisão: "
        f"{resultados_logistica['precisao']:.4f}"
        f"\nRecall: "
        f"{resultados_logistica['recall']:.4f}"
        f"\nF1: "
        f"{resultados_logistica['f1_score']:.4f}"
    )

    print(
        "\nKNN:"
        f"\nAcurácia: "
        f"{resultados_knn['acuracia']:.4f}"
        f"\nPrecisão: "
        f"{resultados_knn['precisao']:.4f}"
        f"\nRecall: "
        f"{resultados_knn['recall']:.4f}"
        f"\nF1: "
        f"{resultados_knn['f1_score']:.4f}"
    )

    return {
        "regressao_logistica": resultados_logistica,
        "knn": resultados_knn,
        "melhores_parametros_logistica":
            grid_logistica.best_params_,
        "melhores_parametros_knn":
            grid_knn.best_params_,
    }


if __name__ == "__main__":

    df = pd.read_csv(
        "dados_limpos_final.csv"
    )

    executar_classificacao(df)