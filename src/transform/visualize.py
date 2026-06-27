import os
import matplotlib.pyplot as plt
import seaborn as sns


def gerar_grafico_integridade(df):
    """Gera um gráfico analítico focado em honestidade estatística e ética

    visual, investigando a relação causal entre o tempo de entrega e a nota do
    cliente.
    """
    print(
        "\n====== INICIANDO ETAPA DE VISUALIZAÇÃO (VISUALIZE) ======"
    )

    df_plot = df.copy()

    df_plot = df_plot[
        (df_plot["tempo_entrega_dias"] >= 0)
        & (df_plot["tempo_entrega_dias"] <= 30)
    ]

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    sns.lineplot(
        data=df_plot,
        x="tempo_entrega_dias",
        y="review_score",
        marker="o",
        color="#2c3e50",
        linewidth=2,
        errorbar=("ci", 95),
    )

    plt.ylim(1, 5)

    plt.title(
        "Impacto do Tempo de Entrega na Satisfação do Cliente (Olist)",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel(
        "Tempo de Entrega Real (Dias)", fontsize=11, labelpad=10
    )
    plt.ylabel(
        "Nota de Avaliação Média (Review Score)",
        fontsize=11,
        labelpad=10,
    )

    plt.figtext(
        0.1,
        0.01,
        "* O sombreamento ao redor da linha representa o Intervalo de Confiança de 95%.\n"
        "* Escala do eixo Y mantida estritamente nos limites originais da pesquisa (1-5) para evitar distorções visuais.",
        fontsize=9,
        style="italic",
        color="#7f8c8d",
    )

    # Salvando o gráfico de forma automatizada
    caminho_salvamento = "grafico_integridade_satisfacao.png"
    plt.tight_layout()
    plt.savefig(caminho_salvamento, dpi=300)
    plt.close()

    print(
        f"   [Resultado] Gráfico ético gerado com sucesso e salvo como '{caminho_salvamento}'!"
    )


if __name__ == "__main__":
    print(
        "Execute o script 'main.py' na raiz para rodar o pipeline completo."
    )