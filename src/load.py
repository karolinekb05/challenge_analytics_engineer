import pandas as pd
from pathlib import Path
import logging
import sys
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
load_dotenv()

# Configuração inicial do arquivo log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/extract.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('../logs/extract')

# Função que faz conexão com o banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

# Executa os arquivos .sql para criar a estrutura do banco de dados
def execute_sql_files(conn, cursor, logger):
    sql_dir = Path('../db')
    sql_files = [
        'functions.sql',
        'dim_date.sql',
        'dim_domain.sql',
        'dim_status.sql',
        'fact_product.sql',
        'dim_attribute.sql',
        'dim_picture.sql',
        'dim_setting.sql'
    ]
    
    for sql_file in sql_files:
        try:
            with open(sql_dir / sql_file, 'r') as f:
                sql = f.read()
                cursor.execute(sql)
                conn.commit()
                logger.info(f"Arquivo {sql_file} executado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao executar {sql_file}: {str(e)}")
            conn.rollback()
            raise

# Função que carrega os .csv para o banco de dados
def load_csv_files(conn, cursor, logger):
    data_dir = Path('../data/')
    
    # Carrega as dimensões independentes
    independent_dims = ['dim_date', 'dim_domain', 'dim_status']
    for dim in independent_dims:
        csv_file = data_dir / f"{dim}.csv"
        if csv_file.exists():
            try:
                table_name = dim
                df = pd.read_csv(csv_file)
                
                # Converter DataFrame para lista de tuplas
                records = [tuple(x) for x in df.to_numpy()]
                columns = ','.join(df.columns)
                
                # Query de inserção
                query = f"""
                    INSERT INTO {table_name} ({columns})
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """
                
                execute_values(cursor, query, records)
                conn.commit()
                logger.info(f"Arquivo {csv_file.name} carregado com sucesso")
                
            except Exception as e:
                logger.error(f"Erro ao carregar {csv_file.name}: {str(e)}")
                conn.rollback()
                continue
    
    # Depois carrega a tabela de fatos
    fact_file = data_dir / "fact_product.csv"
    if fact_file.exists():
        try:
            df = pd.read_csv(fact_file)
            
            # Tratar o campo children_ids
            df['children_ids'] = df['children_ids'].apply(
                lambda x: '{}' if pd.isna(x) else f"{{{x}}}"
            )
            
            # Tratar o campo keywords
            df['keywords'] = df['keywords'].apply(
                lambda x: '{}' if pd.isna(x) else f"{{{x}}}"
            )
            
            records = [tuple(x) for x in df.to_numpy()]
            columns = ','.join(df.columns)
            
            query = f"""
                INSERT INTO fact_product ({columns})
                VALUES %s
                ON CONFLICT (product_id) DO NOTHING
            """
            
            execute_values(cursor, query, records)
            conn.commit()
            logger.info("Arquivo fact_product.csv carregado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao carregar fact_product.csv: {str(e)}")
            conn.rollback()
            return
    
    # Carrega as dimensões dependentes
    dependent_dims = ['dim_attribute', 'dim_picture', 'dim_setting']
    for dim in dependent_dims:
        csv_file = data_dir / f"{dim}.csv"
        if csv_file.exists():
            try:
                table_name = dim
                df = pd.read_csv(csv_file)
                
                # Verificar se todos os product_id existem em fact_product
                cursor.execute("SELECT product_id FROM fact_product")
                valid_product_ids = {row[0] for row in cursor.fetchall()}
                df = df[df['product_id'].isin(valid_product_ids)]
                
                if len(df) == 0:
                    logger.warning(f"Nenhum registro válido encontrado em {csv_file.name}")
                    continue
                
                # Converter DataFrame para lista de tuplas
                records = [tuple(x) for x in df.to_numpy()]
                columns = ','.join(df.columns)
                
                # Query de inserção
                query = f"""
                    INSERT INTO {table_name} ({columns})
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """
                
                execute_values(cursor, query, records)
                conn.commit()
                logger.info(f"Arquivo {csv_file.name} carregado com sucesso")
                
            except Exception as e:
                logger.error(f"Erro ao carregar {csv_file.name}: {str(e)}")
                conn.rollback()
                continue

def main():
    logger.info("Iniciando processo de carga no banco de dados")
    
    try:
        # Estabelecer conexão com o banco
        conn = get_db_connection()
        cursor = conn.cursor()
        logger.info("Conexão com o banco de dados estabelecida")
        
        # Executar arquivos SQL
        logger.info("Executando arquivos SQL...")
        execute_sql_files(conn, cursor, logger)
        
        # Carregar arquivos CSV
        logger.info("Carregando arquivos CSV...")
        load_csv_files(conn, cursor, logger)
        
        logger.info("Processo de carga concluído com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante o processo de carga: {str(e)}")
        sys.exit(1)
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            logger.info("Conexão com o banco de dados encerrada")

if __name__ == "__main__":
    main()
