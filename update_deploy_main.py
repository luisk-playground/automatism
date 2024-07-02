import yaml

# Leer el archivo deploy-main.yml y extraer los valores de ecr_repository y microservice
with open('.github/workflows/deploy-main.yml', 'r') as file:
    deploy_main = yaml.safe_load(file)

ecr_repository = deploy_main['jobs']['CI-CD-main']['with']['ecr_repository']
microservice = deploy_main['jobs']['CI-CD-main']['with']['microservice']

# Leer el archivo deploy-main-new.yml
with open('deploy-main-new.yml', 'r') as file:
    deploy_main_new = yaml.safe_load(file)

# Reemplazar los valores de ##VALUE_ECR_REPOSITORY## y ##VALUE_MICROSERVICE##
deploy_main_new['jobs']['CI-CD-main']['with']['ecr_repository'] = ecr_repository
deploy_main_new['jobs']['CI-CD-main']['with']['microservice'] = microservice

# Sobrescribir deploy-main.yml con el contenido actualizado
with open('.github/workflows/deploy-main.yml', 'w') as file:
    yaml.dump(deploy_main_new, file, sort_keys=False)

print("Archivo .github/workflows/deploy-main.yml actualizado con éxito.")