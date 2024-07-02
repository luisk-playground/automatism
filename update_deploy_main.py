import yaml

# Definir los nuevos jobs como diccionarios
remove_branch_protection_job = {
    'remove_branch_protection': {
        'runs-on': 'ubuntu-latest',
        'steps': [
            {
                'name': 'Remove protection from old branch',
                'env': {
                    'GH_TOKEN': '${{ secrets.GH_PAT }}'
                },
                'run': 'curl -s -X DELETE -H "Authorization: token $GH_TOKEN" '
                       '"https://api.github.com/repos/${{ github.repository }}/branches/development/protection"'
            }
        ]
    }
}

apply_branch_protection_job = {
    'apply_branch_protection': {
        'needs': ['sync_develop'],
        'runs-on': 'ubuntu-latest',
        'steps': [
            {
                'name': 'Get current branch protection settings',
                'id': 'payload',
                'env': {
                    'GH_TOKEN': '${{ secrets.GH_PAT }}',
                    'REPO': '${{ github.repository }}'
                },
                'run': 'json=\'{'
                       '"enforce_admins": true,'
                       '"required_pull_request_reviews": {'
                       '"dismiss_stale_reviews": false,'
                       '"require_code_owner_reviews": true,'
                       '"require_last_push_approval": false,'
                       '"required_approving_review_count": 1'
                       '},'
                       '"restrictions": null,'
                       '"required_status_checks": null'
                       '}\''
                       'echo json=$json >> $GITHUB_OUTPUT'
                       'echo $json'
            },
            {
                'name': 'Apply protection to new branch',
                'env': {
                    'GH_TOKEN': '${{ secrets.GH_PAT }}',
                    'REPO': '${{ github.repository }}',
                    'BRANCH': 'development'
                },
                'run': 'curl -s -X PUT -H "Authorization: token $GH_TOKEN" '
                       '-H "Accept: application/vnd.github.luke-cage-preview+json" '
                       '"https://api.github.com/repos/${{ github.repository }}/branches/development/protection" '
                       '-d \'${{ steps.payload.outputs.json }}\''
                       'echo "Branch protection applied to $BRANCH"'
            },
            {
                'name': 'Verify new branch protection settings',
                'env': {
                    'GH_TOKEN': '${{ secrets.GH_PAT }}',
                    'REPO': '${{ github.repository }}',
                    'BRANCH': 'development'
                },
                'run': 'PROTECTION_SETTINGS=$(curl -s -H "Authorization: token $GH_TOKEN" '
                       '"https://api.github.com/repos/${{ github.repository }}/branches/development/protection")'
                       'if [[ $PROTECTION_SETTINGS == *"Not Found"* ]]; then '
                       'echo "Branch protection not found for $BRANCH"'
                       'exit 1'
                       'fi'
                       'echo "Branch protection found: $PROTECTION_SETTINGS"'
            }
        ]
    }
}

# Cargar el archivo deploy-main.yml
with open('./.github/workflows/deploy-main.yml', 'r') as file:
    data = yaml.safe_load(file)

# Añadir la dependencia needs al job sync_develop
if 'sync_develop' in data['jobs']:
    data['jobs']['sync_develop']['needs'] = ['remove_branch_protection']

# Añadir los nuevos jobs en el orden correcto
new_jobs_order = {
    'remove_branch_protection': remove_branch_protection_job['remove_branch_protection'],
    'sync_develop': data['jobs']['sync_develop'],
    'apply_branch_protection': apply_branch_protection_job['apply_branch_protection'],
    'CI-CD-main': data['jobs']['CI-CD-main']
}

data['jobs'] = new_jobs_order

# Guardar los cambios en el archivo deploy-main.yml
with open('./.github/workflows/deploy-main.yml', 'w') as file:
    yaml.dump(data, file, sort_keys=False)
