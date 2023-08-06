from dynata_rex import OpportunityRegistry
registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')

# List opportunities from the registry
opportunities = registry.list_opportunities()

opportunity = opportunities[0]

opportunity_json = opportunity.json()
