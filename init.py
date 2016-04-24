import random, string
from web.services.users import users
from web.services.projects import projects

apikey = ''.join(random.choice(string.letters+string.digits) for _ in range(32))
users.create(name="demo1",
             password="123456",
             apikey=apikey)
#projects.create(name="pydelo",
#                repo_url="",
#                checkout_dir="/data/home/rocky/pydelo/test/checkout",
#                deploy_dir="/data/home/rocky/pydelo/test/deploy",
#                deploy_history_dir="/data/home/rocky/pydelo/history")
