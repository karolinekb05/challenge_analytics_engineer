# Challenge Analytics Engineer

O objetivo é criar um pipeline de dados que extrai informações da API do Mercado Livre sobre o produto Chromecast, transforma os dados e os carrega em um banco de dados PostgreSQL na AWS. Para finalizar, foi criado um dashboard para analisar os dados obtidos deste pipeline.

## Link do Dashboard: 
A análise dos dados foi feita com a ferramenta Looker Studio, com a conexão de dados do banco PostgreSQL que está hospedado na AWS RDS.

Link: https://lookerstudio.google.com/s/gZfJtPAROC8

## Estrutura do Projeto

```
.
├── data/              # Arquivos CSV gerados pelo transform.py
├── db/                # Arquivos .sql para criação do banco e das tabelas
├── json/              # Arquivos JSON gerados pelo extract.py
├── src/               # Código fonte principal
│   ├── extract.py     # Script de extração da API
│   ├── transform.py   # Script de transformação dos dados
│   └── load.py        # Script de carregamento no PostgreSQL da AWS
├── .env               # Variáveis de ambiente (não versionado)
├── .env.example       # Exemplo de configuração das variáveis de ambiente
├── requirements.txt   # Bibliotecas do projeto
└── .gitignore         # Arquivos ignorados pelo Git

```

## Decisões Técnicas

### 1. Arquitetura ETL
O projeto foi estruturado seguindo o padrão ETL (Extract, Transform, Load):
- **Extract**: Acessa a API oficial do Mercado Livre para extrair dados de busca sobre produtos chromecast;
Sobre a gestão de paginação: como o valor de itens por página era de 50, decidi por trabalhar sempre atualizando o offset até chegar em 10, que totaliza as 500 requisições solicitadas
- **Transform**: Processa os dados JSON em DataFrames, transforma os dados para salvar em arquivos CSV
- **Load**: Carrega os arquivos CSV com os dados transformados no PostgreSQL que está na AWS

### 2. Tecnologias Utilizadas
- **Python**: Linguagem principal para desenvolvimento dos scripts
- **PostgreSQL**: Banco de dados relacional para armazenamento dos dados
- **Ambiente Virtual**: Utilização de `venv` para isolamento de dependências

### 3. Segurança
- Token da API armazenado de forma segura
- Credenciais do banco de dados protegidas

### 4. Modelagem de dados: Star Schema
O banco de dados relacional foi estruturado seguindo a modelagem Star Schema, os motivos são:
- Otimizado para análise de dados
- De acordo com os dados obtidos, esse modelo tornou os dados mais objetivos e de fácil acesso
- É um modelo altamente escalável, futuramente pode-se acrescentar mais dados sobre produtos de forma rápida

## Configuração do Ambiente

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
   - Copie `.env.example` para `.env`
   - Preencha as credenciais necessárias

## Execução

O pipeline pode ser executado em sequência:

1. Extração dos dados:
   ```bash
   python src/extract.py
   ```

2. Transformação dos dados:
   ```bash
   python src/transform.py
   ```

3. Carregamento no banco de dados:
   ```bash
   python src/load.py
   ```

## Considerações

- O token da API do Mercado Livre precisa ser renovado a cada 6 horas
- Os dados temporários (JSON e CSV) são mantidos para debugging e reprocessamento
- Logs são gerados para facilitar o monitoramento e identificação de problemas
