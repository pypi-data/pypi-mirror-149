from dynata_rex import RespondentGateway

gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'

signed_url = gateway.sign_url(url, url_quoting=True)

# 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&access_key=rex_access_key&expiration=2021-11-24T16%3A12%3A35.991Z&signature=4219cf63406ae429d94dbe9c33027816c264c1e2bf1edbadd2510eb9bf2351c3'
