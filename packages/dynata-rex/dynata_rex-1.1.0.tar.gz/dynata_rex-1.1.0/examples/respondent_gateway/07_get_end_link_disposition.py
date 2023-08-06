from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')


############################################
# Get Disposition of a Survey from Endlink #
############################################

termination = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"  # noqa

disposition = gateway.get_respondent_disposition(termination)

# >>> <GatewayDispositionsEnum.TERMINATION: 2>

disposition.name

# >>> 'TERMINATION'

disposition.value

# >>> 2


#####################################################
# Get Disposition + Status of a Survey from Endlink #
#####################################################

termination = "https://respondent.fake.rex.dynata.com/end?ctx=XXXX&transaction_id=123456&disposition=2&status=1&access_key=rex_access_key&expiration=2021-11-24T19:23:23.439Z&signature=d351ff102b3ae6252d47fd54b859ecaf38c2701f214c233848bbdf64c0bc7fe1"  # noqa

status = gateway.get_respondent_status(termination)

# <GatewayStatusEnum.TERMINATION_DYNATA: (<GatewayDispositionsEnum.TERMINATION: 2>, 1)>  # noqa

status.name

# >>> 'TERMINATION_DYNATA'

status.value

# >>> (<GatewayDispositionsEnum.TERMINATION: 2>, 1)
