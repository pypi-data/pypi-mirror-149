from dynata_rex import OpportunityRegistry

registry = OpportunityRegistry('rex_access_key', 'rex_secret_key')

opportunities = registry.list_opportunities()

opportunity_ids = [opportunity.id for opportunity in opportunities]

registry.ack_opportunities(opportunity_ids)
