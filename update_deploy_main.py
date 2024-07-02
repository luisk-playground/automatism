import re

# Función para leer el archivo y obtener los valores necesarios
def get_values(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    ecr_repository = ""
    microservice = ""

    for line in lines:
        if "ecr_repository" in line:
            ecr_repository = line.split(":")[1].strip()
        elif "microservice" in line:
            microservice = line.split(":")[1].strip()

    return ecr_repository, microservice

# Función para reemplazar los valores en el nuevo archivo
def replace_values(file_path, ecr_repository, microservice):
    with open(file_path, 'r') as file:
        content = file.read()

    content = re.sub(r"##VALUE_ECR_REPOSITORY##", ecr_repository, content)
    content = re.sub(r"##VALUE_MICROSERVICE##", microservice, content)

    return content

# Leer los valores del archivo existente
ecr_repository, microservice = get_values('.github/workflows/deploy-main.yml')

# Reemplazar los valores en el nuevo archivo
updated_content = replace_values('deploy-main-new.yml', ecr_repository, microservice)

# Sobreescribir el archivo original con el contenido actualizado
with open('.github/workflows/deploy-main.yml', 'w') as file:
    file.write(updated_content)

print("Archivo .github/workflows/deploy-main.yml actualizado con éxito.")