from azure.cosmos import CosmosClient, exceptions, PartitionKey

COSMOS_ENDPOINT = ''
COSMOS_KEY = ''

DATABASE_NAME = 'exam-db'
CONTAINE_NAME = 'projects'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)


# Crear o obtener el contenedor
try:
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key = PartitionKey(path = "/id"),
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(CONTAINER_NAME)
