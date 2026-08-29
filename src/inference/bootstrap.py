import numpy as np
import matplotlib.pyplot as plt


def executar_bootstrap(
    df,
    coluna="payment_value",
    n_bootstrap=2000,
    seed=42,
    caminho_saida="distribuicao_bootstrap.png",
):

    print("\n====== INICIANDO BOOTSTRAP E INTERVALOS DE CONFIANÇA ======")

    dados = df[coluna].dropna().to_numpy()

    n = len(dados)

    if n == 0:
        raise ValueError(f"A coluna '{coluna}' não possui valores válidos.")

    media_amostral = np.mean(dados)

    # Desvio padrão amostral
    desvio_padrao = np.std(dados, ddof=1)

    print(f"-> Variável analisada: {coluna}")
    print(f"-> Tamanho da amostra (N): {n}")
    print(f"-> Média amostral: R$ {media_amostral:.2f}")
    print(f"-> Desvio padrão amostral: R$ {desvio_padrao:.2f}")

    # Gerador aleatório reproduzível
    rng = np.random.default_rng(seed)

    print(f"-> Executando {n_bootstrap} reamostragens Bootstrap...")

    medias_bootstrap = np.empty(n_bootstrap)

    # Bootstrap com reposição
    for i in range(n_bootstrap):
        amostra_bootstrap = rng.choice(
            dados,
            size=n,
            replace=True,
        )

        medias_bootstrap[i] = np.mean(amostra_bootstrap)

    # ============================
    # IC 95% - Bootstrap
    # ============================

    limite_inferior_bootstrap = np.percentile(
        medias_bootstrap,
        2.5,
    )

    limite_superior_bootstrap = np.percentile(
        medias_bootstrap,
        97.5,
    )

    # ============================
    # IC 95% - Paramétrico
    # ============================

    erro_padrao = desvio_padrao / np.sqrt(n)

    z = 1.96

    limite_inferior_parametrico = (
        media_amostral - z * erro_padrao
    )

    limite_superior_parametrico = (
        media_amostral + z * erro_padrao
    )

    print("\n--- INTERVALOS DE CONFIANÇA DE 95% ---")

    print(
        "IC Bootstrap: "
        f"R$ {limite_inferior_bootstrap:.2f} "
        f"até R$ {limite_superior_bootstrap:.2f}"
    )

    print(
        "IC Paramétrico: "
        f"R$ {limite_inferior_parametrico:.2f} "
        f"até R$ {limite_superior_parametrico:.2f}"
    )

    # ============================
    # Gráfico
    # ============================

    plt.figure(figsize=(10, 6))

    plt.hist(
        medias_bootstrap,
        bins=40,
        edgecolor="black",
        alpha=0.7,
    )

    # IC Bootstrap
    plt.axvline(
        limite_inferior_bootstrap,
        linestyle="--",
        linewidth=2,
        label="IC Bootstrap 95% - Limite inferior",
    )

    plt.axvline(
        limite_superior_bootstrap,
        linestyle="--",
        linewidth=2,
        label="IC Bootstrap 95% - Limite superior",
    )

    # IC Paramétrico
    plt.axvline(
        limite_inferior_parametrico,
        linestyle=":",
        linewidth=2,
        label="IC Paramétrico 95% - Limite inferior",
    )

    plt.axvline(
        limite_superior_parametrico,
        linestyle=":",
        linewidth=2,
        label="IC Paramétrico 95% - Limite superior",
    )

    plt.axvline(
        media_amostral,
        linewidth=2,
        label="Média amostral",
    )

    plt.title(
        "Distribuição das Médias Bootstrap - Valor das Transações"
    )

    plt.xlabel("Média do valor da transação (R$)")
    plt.ylabel("Frequência")

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        caminho_saida,
        dpi=300,
    )

    plt.close()

    print(f"\n-> Gráfico salvo em: {caminho_saida}")

    return {
        "media_amostral": media_amostral,
        "desvio_padrao": desvio_padrao,
        "n": n,
        "ic_bootstrap": (
            limite_inferior_bootstrap,
            limite_superior_bootstrap,
        ),
        "ic_parametrico": (
            limite_inferior_parametrico,
            limite_superior_parametrico,
        ),
    }

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("dados_limpos_final.csv")

    executar_bootstrap(df)