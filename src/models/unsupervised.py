import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def encontrar_cotovelo(valores_k, inercias):
    """
    Estima automaticamente o ponto do cotovelo calculando
    a maior distância entre cada ponto e a reta que liga
    o primeiro ao último ponto da curva.
    """

    pontos = np.column_stack(
        (
            np.array(valores_k, dtype=float),
            np.array(inercias, dtype=float),
        )
    )

    primeiro = pontos[0]
    ultimo = pontos[-1]

    vetor_reta = ultimo - primeiro
    norma = np.linalg.norm(vetor_reta)

    if norma == 0:
        return valores_k[0]

    vetor_unitario = vetor_reta / norma

    distancias = []

    for ponto in pontos:
        vetor_ponto = ponto - primeiro

        projecao = (
            primeiro
            + np.dot(vetor_ponto, vetor_unitario)
            * vetor_unitario
        )

        distancia = np.linalg.norm(
            ponto - projecao
        )

        distancias.append(distancia)

    indice_cotovelo = int(
        np.argmax(distancias)
    )

    return valores_k[indice_cotovelo]


def executar_nao_supervisionado(df):
    """
    Executa PCA e K-Means sobre variáveis numéricas
    do conjunto de dados tratado.
    """

    print(
        "\n====== INICIANDO APRENDIZADO "
        "NÃO SUPERVISIONADO ======"
    )

    # ==========================================
    # Seleção das variáveis
    # ==========================================

    colunas = [
        "payment_value",
        "payment_installments",
        "review_score",
        "tempo_entrega_dias",
    ]

    dados = (
        df[colunas]
        .dropna()
        .copy()
    )

    print(
        f"-> Registros utilizados: {len(dados)}"
    )

    print(
        "-> Variáveis utilizadas:"
    )

    for coluna in colunas:
        print(f"   - {coluna}")

    # ==========================================
    # Padronização
    # ==========================================

    print(
        "\n-> Padronizando as variáveis..."
    )

    scaler = StandardScaler()

    dados_padronizados = scaler.fit_transform(
        dados
    )

    # ==========================================
    # PCA
    # ==========================================

    print(
        "-> Aplicando PCA com dois "
        "componentes principais..."
    )

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    componentes = pca.fit_transform(
        dados_padronizados
    )

    variancia_pc1 = (
        pca.explained_variance_ratio_[0]
    )

    variancia_pc2 = (
        pca.explained_variance_ratio_[1]
    )

    variancia_acumulada = (
        variancia_pc1 + variancia_pc2
    )

    print(
        "\n--- VARIÂNCIA EXPLICADA PELO PCA ---"
    )

    print(
        f"PC1: {variancia_pc1 * 100:.2f}%"
    )

    print(
        f"PC2: {variancia_pc2 * 100:.2f}%"
    )

    print(
        "Variância explicada acumulada "
        f"(PC1 + PC2): "
        f"{variancia_acumulada * 100:.2f}%"
    )

    # ==========================================
    # Gráfico PCA
    # ==========================================

    plt.figure(
        figsize=(10, 6)
    )

    plt.scatter(
        componentes[:, 0],
        componentes[:, 1],
        s=8,
        alpha=0.35,
    )

    plt.title(
        "Projeção PCA dos Pedidos do E-Commerce"
    )

    plt.xlabel(
        f"Componente Principal 1 "
        f"({variancia_pc1 * 100:.2f}% da variância)"
    )

    plt.ylabel(
        f"Componente Principal 2 "
        f"({variancia_pc2 * 100:.2f}% da variância)"
    )

    plt.tight_layout()

    plt.savefig(
        "pca_projecao.png",
        dpi=300,
    )

    plt.close()

    print(
        "\n-> Gráfico salvo em: "
        "pca_projecao.png"
    )

    # ==========================================
    # Método do Cotovelo
    # ==========================================

    print(
        "\n-> Executando Método do Cotovelo..."
    )

    valores_k = list(
        range(1, 9)
    )

    inercias = []

    for k in valores_k:

        modelo_kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        modelo_kmeans.fit(
            dados_padronizados
        )

        inercias.append(
            modelo_kmeans.inertia_
        )

        print(
            f"   k={k} | "
            f"Inércia={modelo_kmeans.inertia_:.2f}"
        )

    # ==========================================
    # Identificação do cotovelo
    # ==========================================

    melhor_k = encontrar_cotovelo(
        valores_k,
        inercias,
    )

    # Evita a escolha trivial k = 1
    if melhor_k < 2:
        melhor_k = 2

    print(
        f"\n-> Número de clusters sugerido "
        f"pelo Método do Cotovelo: k={melhor_k}"
    )

    # ==========================================
    # Gráfico do Cotovelo
    # ==========================================

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        valores_k,
        inercias,
        marker="o",
    )

    plt.axvline(
        melhor_k,
        linestyle="--",
        label=f"Cotovelo sugerido: k={melhor_k}",
    )

    plt.title(
        "Método do Cotovelo - K-Means"
    )

    plt.xlabel(
        "Número de clusters (k)"
    )

    plt.ylabel(
        "Inércia"
    )

    plt.xticks(
        valores_k
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "curva_cotovelo_kmeans.png",
        dpi=300,
    )

    plt.close()

    print(
        "-> Gráfico salvo em: "
        "curva_cotovelo_kmeans.png"
    )

    # ==========================================
    # K-Means final
    # ==========================================

    print(
        f"\n-> Treinando K-Means final "
        f"com k={melhor_k}..."
    )

    kmeans_final = KMeans(
        n_clusters=melhor_k,
        random_state=42,
        n_init=10,
    )

    clusters = kmeans_final.fit_predict(
        dados_padronizados
    )

    dados["cluster"] = clusters

    # ==========================================
    # Distribuição dos clusters
    # ==========================================

    print(
        "\n--- DISTRIBUIÇÃO DOS CLUSTERS ---"
    )

    distribuicao = (
        dados["cluster"]
        .value_counts()
        .sort_index()
    )

    print(distribuicao)

    # ==========================================
    # Perfil dos clusters
    # ==========================================

    perfil_clusters = (
        dados.groupby("cluster")[colunas]
        .mean()
        .round(2)
    )

    print(
        "\n--- PERFIL MÉDIO DOS CLUSTERS ---"
    )

    print(perfil_clusters)

    # ==========================================
    # Visualização dos clusters no PCA
    # ==========================================

    plt.figure(
        figsize=(10, 6)
    )

    scatter = plt.scatter(
        componentes[:, 0],
        componentes[:, 1],
        c=clusters,
        s=8,
        alpha=0.45,
    )

    plt.title(
        f"Clusters K-Means projetados no PCA "
        f"(k={melhor_k})"
    )

    plt.xlabel(
        "Componente Principal 1"
    )

    plt.ylabel(
        "Componente Principal 2"
    )

    plt.colorbar(
        scatter,
        label="Cluster",
    )

    plt.tight_layout()

    plt.savefig(
        "clusters_kmeans.png",
        dpi=300,
    )

    plt.close()

    print(
        "\n-> Gráfico salvo em: "
        "clusters_kmeans.png"
    )

    print(
        "\n====== APRENDIZADO NÃO "
        "SUPERVISIONADO CONCLUÍDO ======"
    )

    return {
        "pca": pca,
        "kmeans": kmeans_final,
        "melhor_k": melhor_k,
        "variancia_pc1": variancia_pc1,
        "variancia_pc2": variancia_pc2,
        "variancia_acumulada":
            variancia_acumulada,
        "perfil_clusters":
            perfil_clusters,
    }


if __name__ == "__main__":

    df = pd.read_csv(
        "dados_limpos_final.csv"
    )

    executar_nao_supervisionado(df)