import os
import pandas as pd
from src.extract.extractor import ler_e_parear_dados
from src.transform.cleaner import tratar_dados_estatistico
from src.transform.visualize import gerar_grafico_integridade

def executar_pipeline():
    print("###################################################")
    df_bruto = ler_e_parear_dados()
    
    df_limpo = tratar_dados_estatistico(df_bruto)
    
    nome_arquivo_final = "dados_limpos_final.csv"
    print(f"\n-> Salvando arquivo final em: {nome_arquivo_final}...")
    df_limpo.to_csv(nome_arquivo_final, index=False)
    
    gerar_grafico_integridade(df_limpo)
    
    print("\n[SUCESSO] Pipeline executado de ponta a ponta!")
    print(f"Arquivo '{nome_arquivo_final}' e os gráficos foram gerados com sucesso!")
    print("###################################################")

if __name__ == "__main__":
    executar_pipeline()