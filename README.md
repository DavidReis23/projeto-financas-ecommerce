# Relatório Científico: Análise Estatística e Pipeline de Dados E-Commerce (Olist)

Este projeto implementa um pipeline de dados reprodutível, robusto e fundamentado em princípios estatísticos e de Ciência de Dados para o ecossistema de e-commerce brasileiro (Olist). O objetivo é garantir a integridade analítica da informação, desde a ingestão bruta até a preparação dos dados para inferências causais futuras.

# Membros:
Luiz Henrique, David Reis e Kauã Sousa 

---

## 1. Camada de Ingestão: Amostragem e Viés (Módulo `extractor.py`)

### População-Alvo Ideal vs. Estrutura de Acesso Real (Access Frame)
* **População-Alvo Ideal:** O universo ideal para compreender o e-commerce brasileiro consistiria em todas as transações comerciais digitais realizadas no território nacional, englobando múltiplos marketplaces, pequenas e grandes empresas, e diferentes perfis sociodemográficos de consumidores e operadores logísticos de forma homogênea.
* **Estrutura de Acesso Real (Access Frame):** A estrutura de acesso real é estritamente restrita aos pedidos integrados e transacionados especificamente através do integrador **Olist** no período de **2016 a 2018**.

### Riscos de Viés de Seleção
A base apresenta riscos severos de **Viés de Seleção**:
1.  **Viés de Plataforma:** O Olist atua conectando pequenas e médias empresas a grandes marketplaces. Portanto, grandes varejistas (com logística própria agressiva) e comércios estritamente locais não estão representados.
2.  **Viés Geográfico:** Há uma concentração natural de vendedores no Sudeste brasileiro. Inferir que o tempo de entrega observado reflete a eficiência de toda a malha logística nacional induz ao erro, pois negligencia barreiras de infraestrutura crônicas de regiões como o Norte e Nordeste.

---

## 2. Análise Exploratória e Tratamento Estatístico (Módulo `cleaner.py`)

### Dicionário de Dados e Modelagem Estatística
A base consolidada final estruturada pelo pipeline adota o seguinte esquema de classificação de variáveis:

| Nome da Variável | Tipo Estatístico | Descrição / Domínio |
| :--- | :--- | :--- |
| `order_id` | Categórica Nominal | Identificador único do pedido (Chave Primária) |
| `customer_state` | Categórica Nominal | Estado federativo de residência do comprador |
| `payment_value` | Quantitativa Contínua | Valor financeiro total despendido na transação (R$) |
| `review_score` | Quantitativa Discreta | Nota de satisfação atribuída pelo cliente (Escala de 1 a 5) |
| `tempo_entrega_dias`| Quantitativa Discreta | Janela temporal calculada em dias entre a compra e a entrega |

### Tratamento de Nulos: O Dilema Viés vs. Variância
* **Estratégia Adotada:** * Para `review_score` (numérica), os valores nulos foram **imputados pela mediana** histórica para blindar a base de distorções. 
    * Para os campos textuais (`review_comment_message` e `review_comment_title`), preencheu-se com string vazia (`""`) mantendo a integridade do tipo. 
    * Para os registros com ausência crônica de datas de entrega (`order_delivered_customer_date`), optou-se pela **exclusão cirúrgica** dos registros.
* **Impacto Teórico (Viés vs. Variância):**
    * **Imputação pela Mediana:** Reduz a *Variância* do dataset, tornando análises futuras menos sensíveis a flutuações extremas. Contudo, pode injetar um pequeno *Viés Sistemático*, artificialmente inflando a concentração de dados em torno da tendência central.
    * **Exclusão de Registros:** Mitiga o *Viés* de injetar dados artificiais em pedidos não entregues (como fraudes ou extravios). Porém, aumenta a *Variância* e reduz o poder estatístico da amostra ao reduzir o número de observações úteis.

### Isolamento Matemático de Outliers via IQR
O pipeline isola o ruído financeiro aplicando o método do Intervalo Interquartil ($IQR$) sobre `payment_value`. Com o $Q1$ em R$ 56,78 e o $Q3$ em R$ 171,09, o $IQR$ calculou-se em 114,31.
Matematicamente, o limite superior de corte foi estabelecido por:
$$\text{Limite Superior} = Q3 + (1.5 \times IQR) = 171.09 + (1.5 \times 114.31) = 342.57$$

Transações acima de **R$ 342,57** foram isoladas para evitar que compras atípicas distorçam as análises de tendências do consumidor médio.

---

## 3. Análise de Domínio: Inferência Causal e Ceteris Paribus

A relação sob investigação científica é: **O aumento no Tempo de Entrega (X) causa uma redução na Nota de Avaliação do Cliente (Y)?**

### a) Correlação não é Causalidade
Uma forte correlação linear negativa entre o tempo de entrega e a nota do cliente não comprova causalidade de forma isolada. A matemática apenas aponta que ambos os fenômenos caminham em sentidos opostos no histórico. No entanto, essa relação pode ser puramente espúria ou gerada por fatores externos não modelados, impossibilitando afirmar que é o tempo de entrega, isoladamente, que gera a insatisfação.

### b) Variáveis de Confusão Omitidas (Confounders)
Caso ignoradas, duas variáveis de confusão destroem a validade da análise:
1.  **Valor do Frete (`freight_value`):** Regiões distantes sofrem com fretes caros e prazos longos. O cliente pode atribuir uma nota baixa pelo descontentamento com o custo do frete, e não pelo tempo de espera em si. O frete afeta simultaneamente o tempo de trânsito e a percepção de valor.
2.  **Categoria do Produto:** Produtos complexos, frágeis ou pesados demandam transportadoras especializadas (maior tempo de entrega) e possuem maior probabilidade intrínseca de sofrer avarias ou frustrar a expectativa de usabilidade do comprador.

### c) Desenho Ideal sob o Princípio do Ceteris Paribus
Para isolar estatisticamente o efeito puro do tempo de entrega sobre a nota ("mantendo todas as outras variáveis constantes"), o desenho ideal exigiria um **Experimento Controlado Aleatorizado (A/B Testing)** ou pareamento por escore de propensão (*Propensity Score Matching*):
* Selecionar-se-iam pedidos com o **mesmo produto**, comprados pelo **mesmo valor**, com o **mesmo custo de frete**, para clientes de um **mesmo perfil socioeconômico e região**.
* Aleatoriamente, um grupo de controle receberia o produto em 5 dias e um grupo de tratamento receberia em 15 dias. Ao mantermos todas as variáveis idênticas (*Ceteris Paribus*), qualquer variação observada em `review_score` seria confiavelmente atribuída ao efeito causal do tempo de entrega.

---

## 4. Visualização Científica e Integridade Visual (Módulo `visualize.py`)

O gráfico automatizado gerado pelo pipeline (`grafico_integridade_satisfacao.png`) cumpre rigorosamente os preceitos de **ética visual** propostos por Edward Tufte:
* **Escala Não-Distorcida:** O eixo Y inicia-se obrigatoriamente no limite inferior real da escala de coleta de dados (1) e termina no limite superior absoluto (5). Ocultar ou truncar a escala para simular uma queda mais íngreme violaria a honestidade estatística.
* **Demonstração de Incerteza:** A visualização inclui o sombreamento do **Intervalo de Confiança (IC) de 95%**. Isso garante transparência científica, deixando claro onde os dados possuem alta precisão e onde a densidade amostral diminui.