from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

context_id = 'super-unique-ctx-id'

data = {
    'ctx': 'parent-context-id',           # From survey link 'ctx' parameter
    'gender': 'male',
    'birth_data': '1999-09-09',
    'postal_code': '90210'
}

gateway.create_context(context_id, data)
