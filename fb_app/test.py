from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign


###### check the campaigns ######
my_app_id = '494912992692817'
my_app_secret = '43e1a8ceea8967f52ae5e298b625da03'
my_access_token = 'EAAHCHukfylEBAOcIAaU0wj6QatAiIw4fMx422dyNpGYtVGmg4a0wiFk1HVuud1GEaCWC9hUo0t2Ddij7Bgp6veERlTSac8OTAbYrkExXg89TXcZA2g5h4YjpeVOXZCoqLS58RPDFXFuFEF4oLrlCqumIJcWld1CkQIpsuYQsjDkSpitBjYTC0YLsZAUX8gZD'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_1001879957083968')
campaigns = my_account.get_campaigns()
print(campaigns)

###### create new campaigns ######
# access_token = 'EAAHCHukfylEBAOcIAaU0wj6QatAiIw4fMx422dyNpGYtVGmg4a0wiFk1HVuud1GEaCWC9hUo0t2Ddij7Bgp6veERlTSac8OTAbYrkExXg89TXcZA2g5h4YjpeVOXZCoqLS58RPDFXFuFEF4oLrlCqumIJcWld1CkQIpsuYQsjDkSpitBjYTC0YLsZAUX8gZD'
# app_secret = '43e1a8ceea8967f52ae5e298b625da03'
# app_id = '494912992692817'
# id = 'act_1001879957083968'
# FacebookAdsApi.init(access_token=access_token)
# fields = []
# params = {
#   'name': 'Store Traffic Campaign',
#   'objective': 'STORE_VISITS',
#   'promoted_object': {'page_id':'103147088486613'},
#   'status': 'PAUSED',
#   'special_ad_categories': [],
# }
# a = AdAccount(id).create_campaign(
#   fields=fields,
#   params=params,
# )
# print(a)

# from facebook_business.adobjects.ad import Ad
# from facebook_business.adobjects.lead import Lead
# from facebook_business.api import FacebookAdsApi

# access_token = '<ACCESS_TOKEN>'
# app_secret = '<APP_SECRET>'
# app_id = '<APP_ID>'
# id = '<AD_GROUP_ID>'
# FacebookAdsApi.init(access_token=access_token)

# fields = [
# ]
# params = {
# }
# print Ad(id).get_leads(
#   fields=fields,
#   params=params,
# )