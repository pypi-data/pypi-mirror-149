from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

context_id = 'super-unique-ctx-id'

context = gateway.get_context(context_id)

# {
#    'id': 'super-unique-ctx-id',
#    'items': {
#        'ctx': 'parent-context-id',
#        'gender': 'male',
#        'birth_data': '1999-09-09',
#        'postal_code': '90210'
#     }
# }
