from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

context_id = 'super-unique-ctx-id'

gateway.expire_context('super-unique-ctx-id')

# {
#    'id': 'super-unique-ctx-id',
#    'items': {
#        'ctx': 'parent-context-id',
#        'gender': 'male',
#        'birth_data': '1999-09-09',
#        'postal_code': '90210'
#     },
#     'expiration': '2021-11-30T16:10:44Z'
# }
