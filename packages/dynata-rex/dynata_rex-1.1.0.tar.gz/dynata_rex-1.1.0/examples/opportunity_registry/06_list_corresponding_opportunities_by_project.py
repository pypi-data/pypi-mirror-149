from dynata_rex import OpportunityRegistry
registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')


opportunities = registry.list_opportunities()

opportunity = opportunities[0]

# Get a list of corresponding opportunities from a project_id
corresponding = registry.list_project_opportunities(opportunity.project_id)
