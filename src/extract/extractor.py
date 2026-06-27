import os
import pandas as pd

def ler_e_parear_dados(caminho_dados="data"):
    """
    Carrega os datasets principais do Olist, realiza a conversão correta de tipos 
    (datetime) e faz o pareamento (merge) analítico dos dados.
    """
    print("====== INICIANDO ETAPA DE EXTRAÇÃO E PAREAMENTO ======")
    
    caminho_orders = os.path.join(caminho_dados, "olist_orders_dataset.csv")
    caminho_payments = os.path.join(caminho_dados, "olist_order_payments_dataset.csv")
    caminho_reviews = os.path.join(caminho_dados, "olist_order_reviews_dataset.csv")
    caminho_customers = os.path.join(caminho_dados, "olist_customers_dataset.csv")

    for caminho in [caminho_orders, caminho_payments, caminho_reviews, caminho_customers]:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {caminho}. Certifique-se de colocá-lo na pasta correta.")

    print("-> Carregando arquivos CSV do Olist...")
    df_orders = pd.read_csv(caminho_orders)
    df_payments = pd.read_csv(caminho_payments)
    df_reviews = pd.read_csv(caminho_reviews)
    df_customers = pd.read_csv(caminho_customers)
    print("-> Corrigindo consistência de tipos: Convertendo colunas de texto para Datetime...")
    
    colunas_data = [
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date', 
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    
    for coluna in colunas_data:
        df_orders[coluna] = pd.to_datetime(df_orders[coluna], errors='coerce')
    df_reviews['review_creation_date'] = pd.to_datetime(df_reviews['review_creation_date'], errors='coerce')
    df_reviews['review_answer_timestamp'] = pd.to_datetime(df_reviews['review_answer_timestamp'], errors='coerce')

    print("-> Executando o pareamento de dados (Merges)...")
    df_consolidado = pd.merge(df_orders, df_customers, on="customer_id", how="inner")
    df_consolidado = pd.merge(df_consolidado, df_payments, on="order_id", how="left")
    df_consolidado = pd.merge(df_consolidado, df_reviews, on="order_id", how="left")
    
    print(f"-> Pareamento concluído com sucesso! Formato da base bruta consolidada: {df_consolidado.shape}")
    
    return df_consolidado

if __name__ == "__main__":
    try:
        df_teste = ler_e_parear_dados()
        print("\nExemplo das primeiras linhas do dataframe extraído:")
        print(df_teste[['order_id', 'customer_state', 'payment_value', 'review_score']].head())
    except Exception as e:
        print(f"\n[ERRO NA EXTRAÇÃO]: {e}")