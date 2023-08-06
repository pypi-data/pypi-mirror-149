from dynata_rex import RespondentGateway

gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'

signed_url = gateway.sign_url(url)

# "https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&access_key=rex_access_key&expiration=2021-11-24T16:12:06.070Z&signature=fa8b5cac82d34bcf8026904b  # noqa
