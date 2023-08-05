
# flask api tool [flaspi]

import sys
from ezpip import load_develop
# flask api tool [flaspi]
flaspi = load_develop("flaspi", "../", develop_flag = True)

# call post api
res = flaspi.call_post_api("http://localhost:80/greeting", {"name": "Hoge"})

print(res)
