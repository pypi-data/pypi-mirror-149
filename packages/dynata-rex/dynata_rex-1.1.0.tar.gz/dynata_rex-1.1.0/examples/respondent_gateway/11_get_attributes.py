from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

country = 'country-code'

page_number = 3  # Page Number Being Requested

page_size = 100  # Number of Items Being Requested

gateway.get_attributes(country, page_number, page_size)

# {
#   "data": [
#       {
#           "active": "true/false",
#           "parameter_id": "unique-parameter-id"
#       }
#   ]
# }
