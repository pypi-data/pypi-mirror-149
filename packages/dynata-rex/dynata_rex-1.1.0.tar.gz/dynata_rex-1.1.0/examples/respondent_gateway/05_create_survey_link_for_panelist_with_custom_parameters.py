from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

url = 'https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en'
date_of_birth = '1990-01-01'
gender = 'male'
postal_code = '90210'
respondent_id = 'very-unique-respondent-id'
ttl = 10  # in seconds

custom_params = {
    'custom_parameter': 'custom_value',
    'another_custom_parameter': 'another_custom_value'
}

signed_link = gateway.create_respondent_url(url,
                                            date_of_birth,
                                            gender,
                                            postal_code,
                                            respondent_id,
                                            additional_params=custom_params,
                                            ttl=ttl)

# https://respondent.fake.rex.dynata.com/start?ctx=XXXX&language=en&custom_parameter=custom_value&another_custom_parameter=another_custom_value&birth_date=1990-01-01&gender=male&postal_code=90210&respondent_id=very-unique-respondent-id&access_key=rex_access_key&expiration=2021-12-02T13:48:55.759Z&signature=cf443326b73fb8af14c590e18d79a970fc3f73327c2d140c324ee1ce3020d064  # noqa
