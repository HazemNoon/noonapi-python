from noonapi import NoonSession

session = NoonSession("noon_credentials_sensitive.json")

me = session.auth.whoami()
print(me)
