from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'
date_of_birth = '1990-01-01'
gender = 'male'
postal_code = '90210'
respondent_id = 'very-unique-respondent-id'
ttl = 10  # in seconds

signed_link = gateway.create_respondent_url(url,
                                            date_of_birth,
                                            gender,
                                            postal_code,
                                            respondent_id,
                                            ttl=ttl)

# https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&birth_date=1990-01-01&gender=male&postal_code=90210&respondent_id=very-unique-respondent-id&access_key=rex_access_key&expiration=2021-11-29T15:35:12.993Z&signature=4353e8c4ca8f8fb75530214ac78139b55ca3f090438c639476b8584afe1396e6 # noqa