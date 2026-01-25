import os
from elasticsearch import Elasticsearch

es = Elasticsearch(
    os.getenv('ELASTICSEARCH_HOST'),
    basic_auth=(os.getenv('ELASTICSEARCH_USER'), os.getenv('ELASTICSEARCH_PASSWORD')),
    verify_certs= os.getenv('ELASTICSEARCH_VERIFY_CERTS') == False  # если сертификат самоподписанный
)


if es.ping():
    print("Успешное подключение к Elasticsearch!")
else:
    print("Ошибка подключения.")
