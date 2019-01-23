# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 09:34:40 2019

@author: Artem Los
"""

from helpers import Helpers

from models import Response, RSAPublicKey

response = Response("eyJQcm9kdWN0SWQiOjMzNDksIklEIjoxNjksIktleSI6IklDVkxELVZWU1pSLVpUSUNULVlLR1hMIiwiQ3JlYXRlZCI6MTU0MzkxODMxNiwiRXhwaXJlcyI6MTU0NjUxMDMxNiwiUGVyaW9kIjozMCwiRjEiOmZhbHNlLCJGMiI6ZmFsc2UsIkYzIjpmYWxzZSwiRjQiOmZhbHNlLCJGNSI6ZmFsc2UsIkY2IjpmYWxzZSwiRjciOmZhbHNlLCJGOCI6ZmFsc2UsIk5vdGVzIjpudWxsLCJCbG9jayI6ZmFsc2UsIkdsb2JhbElkIjo0MzQxNCwiQ3VzdG9tZXIiOm51bGwsIkFjdGl2YXRlZE1hY2hpbmVzIjpbeyJNaWQiOiJ0ZXN0IiwiSVAiOiI4NS4yMjkuMjQ1LjIzNiIsIlRpbWUiOjE1NDc3NTc2ODl9XSwiVHJpYWxBY3RpdmF0aW9uIjpmYWxzZSwiTWF4Tm9PZk1hY2hpbmVzIjoxLCJBbGxvd2VkTWFjaGluZXMiOiIiLCJEYXRhT2JqZWN0cyI6W10sIlNpZ25EYXRlIjoxNTQ4MjMzMDk5fQ==",\
                    "muQa+Dt8uJZmgooUNWng5DN9fCW0alCzZIEBV0VDvvcB/Rp0d+4TtLKxzFQ5bKV9CuGfsBDLfqv1gMBFuOAKL3/yH9bd5cXeKcm+JMKlwk1adcSKTX5d1SqL2OIptZ1dwvd/VbUzmMGm5qJ8hU0fJFi5WirldQF8K/0k7ONfpw8STA8jw0nJkUHzYIeAko6dsTW+b/Dk22ECd+FILgxZ1oFyrtfopHMK/kAbRHpdQvikhFlOJh8FlLC/BEyEY5OLzZIPtFNVV0EEQhBL3Nw8ETb0fSaWCdMjaIef2UCNxMJgxWNzoYeSNO6MBLdP9E7ykAeVDZ7aouuSnhzXHF2/yQ==",\
                    0, "")

pubKey = RSAPublicKey("sGbvxwdlDbqFXOMlVUnAF5ew0t0WpPW7rFpI5jHQOFkht/326dvh7t74RYeMpjy357NljouhpTLA3a6idnn4j6c3jmPWBkjZndGsPL4Bqm+fwE48nKpGPjkj4q/yzT4tHXBTyvaBjA8bVoCTnu+LiC4XEaLZRThGzIn5KQXKCigg6tQRy0GXE13XYFVz/x1mjFbT9/7dS8p85n8BuwlY5JvuBIQkKhuCNFfrUxBWyu87CFnXWjIupCD2VO/GbxaCvzrRjLZjAngLCMtZbYBALksqGPgTUN7ZM24XbPWyLtKPaXF2i4XRR9u6eTj5BfnLbKAU5PIVfjIS+vNYYogteQ==",\
                      "AQAB")

print(Helpers.verify_signature(response, pubKey))