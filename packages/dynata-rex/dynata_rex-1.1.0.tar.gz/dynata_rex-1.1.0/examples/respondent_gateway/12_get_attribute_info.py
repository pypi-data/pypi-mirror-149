from dynata_rex import RespondentGateway
gateway = RespondentGateway('rex_access_key', 'rex_secret_key')

attribute_id = 123  # Some-Number

gateway.get_attribute_info(attribute_id)

# {
#     "id": "unique-parameter-id",
#     "name": "Example Question Name",
#     "description": "Example Question Description",
#     "display_mode": "Single-Punch/Multi-Punch",
#     "parent_dependencies": [
#         {
#             "answer_ids": [
#                 {
#                     "id": "unique-answer-id"
#                 }
#             ],
#             "parameter_id": "unique-parameter-id"
#         }
#     ],
#     "expiration_duration": "36000",
#     "is_active": "true/false",
#     "countries": [
#         {
#             "code": "country-code"
#         }
#     ],
#     "question": {
#         "text": "question-text",
#         "translations": [
#             {
#                 "locale": "locale",
#                 "text": "translation-text"
#             }
#         ]
#     },
#     "answers": [
#         {
#             "id": "unique-answer-id",
#             "text": "answer-text",
#             "countries": [
#                 {
#                     "code": "country-code"
#                 }
#             ],
#             "translations": [
#                 {
#                     "locale": "locale",
#                     "text": "translation-text"
#                 }
#             ]
#         }
#     ]
# }
