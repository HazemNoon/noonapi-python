from noonapi import NoonSession

session = NoonSession("examples/noon_credentials_sensitive.json")

me = session.auth.whoami()
print(me)
