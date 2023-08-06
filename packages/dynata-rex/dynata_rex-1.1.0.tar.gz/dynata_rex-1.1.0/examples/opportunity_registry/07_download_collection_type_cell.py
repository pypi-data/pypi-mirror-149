from dynata_rex import OpportunityRegistry

registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')

collection_id = 'abcdefg'

data = registry.download_collection(collection_id)
