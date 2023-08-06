from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

# Verify a signed /end link URL with your credentials

#############
# Valid URL #
#############
end_url = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"  # noqa

gateway.verify_url(end_url)

# >>> True

#####################
# Missing Signature #
#####################

missing_signature = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z"  # noqa

gateway.verify_url(missing_signature)

# >>> False

###############################
# Altered Parameters          #
# (Term --> Complete Attempt) #
###############################
# Disposition changed to 1 (from 2) and status to 0 (from 1)

altered_parameters = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=1&status=0&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"  # noqa

gateway.verify_url(altered_parameters)

# >>> False
