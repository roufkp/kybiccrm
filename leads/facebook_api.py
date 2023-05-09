# Tod Do :
#     install facebook_business
#     import necessory extensions
#     authenticate (login)
#     read campaigns and store in db
#     display campaigns in website and give facebook tag
#     read leads from each campaigns
#     store and display like all other leads



import facebook


access_token= "EAATXK5AW2nwBALbzbRMcTP2INBtGZB4ZAGPzNw7dEZCcJqXYxaMGBqTeSbheExmgwW28gU96tRaQoRJl8bow8a8ruX9w5n3WqXaqFmb4ACTfd1yxgnJe0I22Xix2teyozayXYVCbQLjODEgPW0hVuR6uLxusv9pvksZBvTV7WNCUazZCaZAFPa"
campaign_id= ""


def get_campaign_data(campaign_id, access_token):
    graph = facebook.GraphAPI(access_token=access_token, version="3.0")
    campaign = graph.get_object(id=campaign_id, fields="leads{field_data}")
    return campaign['leads']['data']
