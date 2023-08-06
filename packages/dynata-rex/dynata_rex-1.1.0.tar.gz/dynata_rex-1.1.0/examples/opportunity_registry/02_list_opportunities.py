from dynata_rex import OpportunityRegistry

registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')

opportunities = registry.list_opportunities()

# Returns a list of Opportunities
# [Opportunity(id=1,...), Opportunity(id=2,...), Opportunity(id=1,...)]
