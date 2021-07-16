import pandas as pd
import urllib.request
from sys import argv


url = f"https://www.bcpao.us/api/v1/export?usecodes=0110&zipcodes={argv[1]}&yblow=2012&activeonly=true&sortColumn=saleDate&sortOrder=desc&format=csv"
with urllib.request.urlopen(url) as testfile, open(f"{argv[1]}" ".csv", "w") as f:
    f.write(testfile.read().decode())


homes = pd.read_csv(f"{argv[1]}" ".csv")
homes = homes.loc[homes["MailAddress"] == homes["SiteAddress"]]
just = homes[["MailFormatted1", "MailAddress"]]

## 32907
# just[["Street", "City", "State", "Zip"]] = just.MailAddress.str.extract(
#    "(^\d+\s[A-z]+\s[A-z]+\s[A-z]+[ ])(.+)([a-zA-Z]{2})[ ]([0-9]{5})", expand=True
# )

## 32940
just[["Street", "City", "State", "Zip"]] = just.MailAddress.str.extract(
    "(.+)(PALM BAY|MELBOURNE|PALM SHORES|ROCKLEDGE?)[ ]([a-zA-Z]{2})[ ]([0-9]{5})", expand=True
)

just[["Last", "First"]] = just.MailFormatted1.str.extract("(.+?)[,](.+)?", expand=True)

final = just[["Last", "First", "Street", "City", "State", "Zip"]]
print(final)
final.to_excel(f"{argv[1]}" ".xlsx", index=False, header=True)
