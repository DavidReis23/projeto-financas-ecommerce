import numpy as np
import matplotlib.pyplot as plt


def executar_teste_ab(
    df,
    n_permutacoes=2000,
    seed=42,
    caminho_saida="distribuicao_permutacao.png",
):

    print("\n====== INICIANDO TESTE A/B E TESTE DE PERMUTAÇÃO ======")

    grupo_a = (
        df.loc[
            df["payment_type"] == "credit_card",
            "payment_value",
        ]
        .dropna()
        .to_numpy()
    )

    grupo_b = (
        df.loc[
            df["payment_type"] == "boleto",
            "payment_value",
        ]
        .dropna()
        .to_numpy()
    )

    if len(grupo_a) == 0 or len(grupo_b) == 0:
        raise ValueError(
            "Não foi possível formar os grupos "
            "'credit_card' e 'boleto'."
        )

    print("\nHipóteses estatísticas:")

    print(
        "H0: μ_cartão = μ_boleto "
        "(não existe diferença no ticket médio)."
    )

    print(
        "H1: μ_cartão ≠ μ_boleto "
        "(existe diferença no ticket médio)."
    )

    alpha = 0.05

    media_a = np.mean(grupo_a)
    media_b = np.mean(grupo_b)

    diferenca_observada = media_a - media_b

    print("\n--- RESULTADOS OBSERVADOS ---")

    print(f"Grupo A - Cartão de crédito: {len(grupo_a)} registros")
    print(f"Ticket médio Cartão: R$ {media_a:.2f}")

    print(f"\nGrupo B - Boleto: {len(grupo_b)} registros")
    print(f"Ticket médio Boleto: R$ {media_b:.2f}")

    print(
        f"\nDiferença observada (A - B): "
        f"R$ {diferenca_observada:.2f}"
    )

    print(
        f"\n-> Executando {n_permutacoes} "
        "permutações sob H0..."
    )

    rng = np.random.default_rng(seed)

    dados_combinados = np.concatenate(
        [grupo_a, grupo_b]
    )

    tamanho_a = len(grupo_a)

    diferencas_permutadas = np.empty(
        n_permutacoes
    )

    for i in range(n_permutacoes):

        dados_embaralhados = rng.permutation(
            dados_combinados
        )

        permutado_a = dados_embaralhados[
            :tamanho_a
        ]

        permutado_b = dados_embaralhados[
            tamanho_a:
        ]

        diferencas_permutadas[i] = (
            np.mean(permutado_a)
            - np.mean(permutado_b)
        )

    p_value = np.mean(
        np.abs(diferencas_permutadas)
        >= abs(diferenca_observada)
    )

    print("\n--- TESTE DE HIPÓTESES ---")

    print(f"Nível de significância α: {alpha}")
    print(f"p-value empírico: {p_value:.6f}")

    if p_value < alpha:
        conclusao = (
            "Rejeitamos H0. Existe evidência "
            "estatística de diferença entre os "
            "tickets médios de cartão e boleto."
        )
    else:
        conclusao = (
            "Não rejeitamos H0. Não há evidência "
            "estatística suficiente de diferença "
            "entre os tickets médios."
        )

    print(f"\nConclusão: {conclusao}")

    plt.figure(figsize=(10, 6))

    plt.hist(
        diferencas_permutadas,
        bins=40,
        edgecolor="black",
        alpha=0.7,
    )

    plt.axvline(
        diferenca_observada,
        linewidth=2,
        label=(
            "Diferença observada "
            f"(R$ {diferenca_observada:.2f})"
        ),
    )

    plt.axvline(
        -diferenca_observada,
        linestyle="--",
        linewidth=2,
        label="Extremo simétrico bicaudal",
    )

    plt.title(
        "Distribuição de Permutação - "
        "Cartão de Crédito vs. Boleto"
    )

    plt.xlabel(
        "Diferença entre os tickets médios (R$)"
    )

    plt.ylabel("Frequência")

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        caminho_saida,
        dpi=300,
    )

    plt.close()

    print(
        f"\n-> Gráfico salvo em: {caminho_saida}"
    )

    return {
        "media_cartao": media_a,
        "media_boleto": media_b,
        "diferenca_observada": diferenca_observada,
        "p_value": p_value,
        "alpha": alpha,
        "conclusao": conclusao,
    }


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv(
        "dados_limpos_final.csv"
    )

    executar_teste_ab(df)