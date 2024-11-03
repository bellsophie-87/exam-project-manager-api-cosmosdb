from azure.cosmos import CosmosClient, exceptions, PartitionKey

COSMOS_ENDPOINT = ''
COSMOS_KEY = ''

DATABASE_NAME = 'GestorProyectosDB'
CONTAINE_NAME_PROJECTS = 'projects'
CONTAINE_NAME_USERS = 'users'

# Inicializar el cliente de Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Crear o obtener la base de datos
try:
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(DATABASE_NAME)


# Crear o obtener el contenedor de los ususarios
try:
    users_container = database.create_container_if_not_exists(
        id=CONTAINE_NAME_USERS,
        partition_key = PartitionKey(path = "/id"),
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    users_container = database.get_container_client(CONTAINE_NAME_USERS)

# Crear o obtener el contenedor de los proyectos
try:
    projects_container = database.create_container_if_not_exists(
        id=CONTAINE_NAME_PROJECTS,
        partition_key = PartitionKey(path = "/id"),
        offer_throughput=400
    )
except exceptions.CosmosResourceExistsError:
    projects_container = database.get_container_client(CONTAINE_NAME_PROJECTS)
