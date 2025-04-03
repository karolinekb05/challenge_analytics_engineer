import json
import pandas as pd
from pathlib import Path
import uuid
from datetime import datetime
import logging
import sys

# Configuração inicial do arquivo log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/transform.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('../logs/transform')

# Função para detalhar os dados no arquivo .log
def log_dataframe_info(logger, df, name):
    logger.info(f"\n{'='*50}")
    logger.info(f"DataFrame: {name}")
    logger.info(f"Shape: {df.shape}")
    logger.info("\nPrimeiras 5 linhas:")
    logger.info(f"\n{df.head().to_string()}")
    logger.info(f"\nColunas: {', '.join(df.columns)}")
    logger.info(f"{'='*50}\n")

# Função que faz a leitura do .json e transforma em dataframes para .csv
def transform_json_to_dataframes():
    logger.info("Iniciando processo de transformação dos dados")
    
    try:
        # Caminho do arquivo JSON
        json_path = Path('../json/raw_results.json')
        logger.info(f"Lendo arquivo JSON: {json_path}")
        
        # Ler o arquivo JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Arquivo JSON lido com sucesso. Total de registros: {len(data)}")
        
        # Criar lista para cada dataframe
        products = []
        settings_list = []
        attributes_list = []
        pictures_list = []
        dates_list = []
        domains_list = []
        status_list = []
        
        # Dicionários para controle de duplicatas
        unique_dates = {}
        unique_domains = {}
        unique_status = {}
        
        logger.info("Iniciando processamento dos registros")
        # Processar cada item do JSON
        for idx, item in enumerate(data, 1):
            if idx % 1000 == 0:
                logger.info(f"Processando registro {idx} de {len(data)}")
            
            try:
                # Processar data
                date_created = datetime.fromisoformat(item['date_created'].replace('Z', '+00:00'))
                date_key = date_created.strftime('%Y-%m-%d')
                if date_key not in unique_dates:
                    date_id = str(uuid.uuid4())
                    date_info = {
                        'id': date_id,
                        'date_created': date_created,
                        'year': date_created.year,
                        'month': date_created.month,
                        'day': date_created.day,
                        'quarter': (date_created.month - 1) // 3 + 1,
                        'day_of_week': date_created.weekday(),
                        'is_weekend': date_created.weekday() >= 5,
                        'month_name': date_created.strftime('%B'),
                        'day_name': date_created.strftime('%A'),
                        'is_active': True,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    dates_list.append(date_info)
                    unique_dates[date_key] = date_id
                else:
                    date_id = unique_dates[date_key]
                
                # Processar domínio
                domain_code = item['domain_id']
                if domain_code not in unique_domains:
                    domain_id = str(uuid.uuid4())
                    domain_info = {
                        'id': domain_id,
                        'domain_code': domain_code,
                        'domain_name': domain_code.replace('MLA-', '').replace('_', ' ').title(),
                        'domain_description': f'Domínio {domain_code}',
                        'level': 1,
                        'is_active': True,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    domains_list.append(domain_info)
                    unique_domains[domain_code] = domain_id
                else:
                    domain_id = unique_domains[domain_code]
                
                # Processar status diretamente da chave "status" do JSON
                status_code = item['status']  # Pegando o valor da chave "status"
                is_active = True if status_code.lower() == 'active' else False  # Verifica se é "active" ou "inactive"
                
                if status_code not in unique_status:
                    status_id = str(uuid.uuid4())
                    status_info = {
                        'id': status_id,
                        'status_code': status_code,
                        'status_name': status_code.title(),
                        'status_description': f'Status {status_code}',
                        'is_active': is_active,
                        'product_id': item['id'],
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    status_list.append(status_info)
                    unique_status[status_code] = status_id
                else:
                    status_id = unique_status[status_code]
                
                # DataFrame de produtos
                product = {
                    'id': str(uuid.uuid4()),
                    'product_id': item['id'],
                    'date_id': date_id,
                    'catalog_product_id': item.get('catalog_product_id'),
                    'status_id': status_id,
                    'domain_id': domain_id,
                    'name': item['name'],
                    'children_ids': ','.join(item['children_ids']) if item['children_ids'] else None,
                    'quality_type': item['quality_type'],
                    'priority': item['priority'],
                    'type': item['type'],
                    'site_id': item['site_id'],
                    'keywords': item['keywords'],
                    'is_active': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                products.append(product)
                
                # DataFrame de settings
                settings = {
                    'id': str(uuid.uuid4()),
                    'product_id': item['id'],
                    'listing_strategy_code': item['settings']['listing_strategy'],
                    'listing_strategy_name': item['settings']['listing_strategy'].title(),
                    'exclusive': item['settings']['exclusive'],
                    'is_active': True,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                settings_list.append(settings)
                
                # DataFrame de attributes
                for attr in item['attributes']:
                    attribute = {
                        'id': str(uuid.uuid4()),
                        'product_id': item['id'],
                        'attribute_code': attr['id'],
                        'attribute_name': attr['name'],
                        'value_id': attr.get('value_id'),
                        'value_name': attr.get('value_name'),
                        'is_active': True,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    attributes_list.append(attribute)
                
                # DataFrame de pictures
                for pic in item['pictures']:
                    picture = {
                        'id': str(uuid.uuid4()),
                        'product_id': item['id'],
                        'picture_code': pic['id'],
                        'url': pic['url'],
                        'is_active': True,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    pictures_list.append(picture)
            
            except Exception as e:
                logger.error(f"Erro ao processar registro {idx}: {str(e)}")
                continue
        
        logger.info("Criando dataframes")
        # Criar os dataframes
        df_products = pd.DataFrame(products)
        df_settings = pd.DataFrame(settings_list)
        df_attributes = pd.DataFrame(attributes_list)
        df_pictures = pd.DataFrame(pictures_list)
        df_dates = pd.DataFrame(dates_list)
        df_domains = pd.DataFrame(domains_list)
        df_status = pd.DataFrame(status_list)
        
        logger.info("Dataframes criados com sucesso")
        logger.info(f"Total de registros processados:")
        logger.info(f"- Products: {len(df_products)}")
        logger.info(f"- Settings: {len(df_settings)}")
        logger.info(f"- Attributes: {len(df_attributes)}")
        logger.info(f"- Pictures: {len(df_pictures)}")
        logger.info(f"- Dates: {len(df_dates)}")
        logger.info(f"- Domains: {len(df_domains)}")
        logger.info(f"- Status: {len(df_status)}")
        
        # Logar informações detalhadas dos dataframes
        log_dataframe_info(logger, df_products, "fact_product")
        log_dataframe_info(logger, df_settings, "dim_setting")
        log_dataframe_info(logger, df_attributes, "dim_attribute")
        log_dataframe_info(logger, df_pictures, "dim_picture")
        log_dataframe_info(logger, df_dates, "dim_date")
        log_dataframe_info(logger, df_domains, "dim_domain")
        log_dataframe_info(logger, df_status, "dim_status")
        
        return df_products, df_settings, df_attributes, df_pictures, df_dates, df_domains, df_status
    
    except Exception as e:
        logger.error(f"Erro durante o processo de transformação: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        df_products, df_settings, df_attributes, df_pictures, df_dates, df_domains, df_status = transform_json_to_dataframes()
        
        output_dir = Path('../data/')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Salvar os dataframes em arquivos CSV
        logger = logging.getLogger('transform')
        logger.info("Salvando dataframes em arquivos CSV")
        
        df_products.to_csv(output_dir / 'fact_product.csv', index=False)
        logger.info("fact_product.csv salvo com sucesso")
        
        df_settings.to_csv(output_dir / 'dim_setting.csv', index=False)
        logger.info("dim_setting.csv salvo com sucesso")
        
        df_attributes.to_csv(output_dir / 'dim_attribute.csv', index=False)
        logger.info("dim_attribute.csv salvo com sucesso")
        
        df_pictures.to_csv(output_dir / 'dim_picture.csv', index=False)
        logger.info("dim_picture.csv salvo com sucesso")
        
        df_dates.to_csv(output_dir / 'dim_date.csv', index=False)
        logger.info("dim_date.csv salvo com sucesso")
        
        df_domains.to_csv(output_dir / 'dim_domain.csv', index=False)
        logger.info("dim_domain.csv salvo com sucesso")
        
        df_status.to_csv(output_dir / 'dim_status.csv', index=False)
        logger.info("dim_status.csv salvo com sucesso")
        
        logger.info("Processo de transformação concluído com sucesso")
        
    except Exception as e:
        logger = logging.getLogger('transform')
        logger.error(f"Erro durante a execução do script: {str(e)}")
        sys.exit(1)
