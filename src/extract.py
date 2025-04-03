import requests
import logging
import json
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

# Header da requisição com o token do .env
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TOKEN_API_MELI')}"
}

# URL da API do ML
url_api_meli = 'https://api.mercadolibre.com/products/search?'

# Função para salvar os dados obtidos em um arquivo .json
def salvar_json(dados):
    logger.info("Salvando os dados em um arquivo JSON...")
    # Caminho para salvar o arquivo json
    json_save = '../json/'
    with open(f'{json_save}raw_results.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    logger.info("Arquivo salvo com sucesso!")

def extract_api():
    total_response = []
    max_results = 500  # O número total de resultados
    max_pages = 10  # Limitar a 10 páginas
    offset = 0

    # Parâmetros da requisição
    params = {
        'q': 'chromecast',
        'site_id': 'MLA',
        'limit': 50,  # Cada página terá 50 itens
        'offset': offset
    }

    # Função para realizar a requisição
    def fetch_data(status):
        # Status 'active' ou 'inactive'
        params['status'] = status
        try:
            response = requests.get(url_api_meli, headers=headers, params=params)
            data = response.json()
            
            # Dados que estão na chave 'result'
            if 'results' in data:
                novos_resultados = data['results']
                total_response.extend(novos_resultados)
                logger.info(f"Status {status}: Adicionados {len(novos_resultados)} resultados. Total: {len(total_response)}")
                return len(novos_resultados)
            else:
                logger.error(f"Resposta não contém resultados para o status {status}")
                return 0
        except Exception as e:
            logger.error(f"Ocorreu um erro durante a requisição para o status {status}: {e}")
            return 0

    # Loop para percorrer as páginas
    for page in range(max_pages):
        logger.info(f"Buscando produtos na página {page+1} com status 'active'...")
        # Buscar produtos com status 'active' para a página
        params['offset'] = page * 50  # O offset de cada página (50 resultados por página)
        fetch_data('active')

        if len(total_response) >= max_results:
            break

    # Se não completou os 500 resultados com 'active', buscar 'inactive'
    if len(total_response) < max_results:
        logger.info("Buscando produtos com status 'inactive' para completar os resultados...")
        for page in range(max_pages):
            if len(total_response) >= max_results:
                break  # Se já completou os 500 resultados, sai do loop

            logger.info(f"Buscando produtos na página {page+1} com status 'inactive'...")
            params['offset'] = page * 50  # Atualiza o offset para cada página
            fetch_data('inactive')

    logger.info(f"Total de resultados obtidos: {len(total_response)}")
    return total_response

if __name__ == "__main__":
    logger.info("Iniciando a extração de dados...")
    data = extract_api()
    # Verifica se tem os dados antes de salvar
    if data:
        salvar_json(data)
        logger.info(f"Extração de dados finalizada! Total de resultados: {len(data)}")
    else:
        logger.error("Falha na extração dos dados, verifique!")
