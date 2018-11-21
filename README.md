# Readme

Compare various models from Mongo or .txt files simultaneously with specified source. Uses the probability based classifier
from branch `prob-class`. Most similar items are ranked. Different options to compare, can take best mean similarity or
best worst-case similarity. There is a visualizer utility in branch `util-visualize` which can be run in browser alongside
this to see why certain fields show up as similar based on data.

**TODO:** Rework input method into accepting JSON or some other easier format, currently everything is a command line argument

## Output

```
( ... NLL values for values read in ... )

Similarity with field=/EDM/account/email
----------------------------------------
/EDM/account/email /EDM/account/licensePlate -29.07111566597032
/EDM/account/email /EDM/account/fname -19.130900929450018
/EDM/account/email /EDM/account/lname -15.561813589675598
/EDM/account/email /EDM/account/phone -55.375724040051516
/EDM/account/email /EDM/account/email -36.95463635908369
/EDM/account/email /EDM/account/_id -109.97630589803438
-----
Top 3 similar items: 
/EDM/account/lname
/EDM/account/fname
/EDM/account/licensePlate
```
