from src.extract.extractor import ler_e_parear_dados
from src.transform.cleaner import tratar_dados_estatistico
from src.transform.visualize import gerar_grafico_integridade

from src.inference.bootstrap import executar_bootstrap
from src.inference.ab_testing import executar_teste_ab

from src.models.regression import executar_regressao
from src.models.machine_learning import executar_classificacao
from src.models.unsupervised import executar_nao_supervisionado


def executar_pipeline():
    print("\n###################################################")
    print("   PIPELINE DE CIÊNCIA DE DADOS - OLIST E-COMMERCE")
    print("###################################################")

    # PARTE 1 - ETL

    print("\n====== PARTE 1: EXTRAÇÃO E TRATAMENTO ======")

    df_bruto = ler_e_parear_dados()

    df_limpo = tratar_dados_estatistico(
        df_bruto
    )

    nome_arquivo_final = "dados_limpos_final.csv"

    print(
        f"\n-> Salvando arquivo final em: "
        f"{nome_arquivo_final}..."
    )

    df_limpo.to_csv(
        nome_arquivo_final,
        index=False,
    )

    # Visualização da AVP1
    gerar_grafico_integridade(
        df_limpo
    )

    # PARTE 2 - INFERÊNCIA ESTATÍSTICA

    print(
        "\n====== PARTE 2: INFERÊNCIA ESTATÍSTICA ======"
    )

    executar_bootstrap(
        df_limpo
    )

    executar_teste_ab(
        df_limpo
    )

    # PARTE 2 - MODELAGEM SUPERVISIONADA

    print(
        "\n====== MODELAGEM SUPERVISIONADA ======"
    )

    executar_regressao(
        df_limpo
    )

    executar_classificacao(
        df_limpo
    )

    # PARTE 2 - MODELAGEM NÃO SUPERVISIONADA

    print(
        "\n====== MODELAGEM NÃO SUPERVISIONADA ======"
    )

    executar_nao_supervisionado(
        df_limpo
    )

    # FINALIZAÇÃO

    print("\n###################################################")
    print("         PIPELINE CONCLUÍDO COM SUCESSO!")
    print("###################################################")

    print(
        "\nArquivos principais gerados:"
        "\n- dados_limpos_final.csv"
        "\n- grafico_integridade_satisfacao.png"
        "\n- distribuicao_bootstrap.png"
        "\n- distribuicao_permutacao.png"
        "\n- pca_projecao.png"
        "\n- curva_cotovelo_kmeans.png"
        "\n- clusters_kmeans.png"
    )


if __name__ == "__main__":
    executar_pipeline()