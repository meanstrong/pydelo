import random
import string
from hashlib import md5
from web.services.users import users
from web.services.projects import projects

users.create(name="root",
             password=md5("123456".encode("utf-8")).hexdigest().upper(),
             apikey=''.join(random.choice(string.letters+string.digits) for _
                            in range(32)),
             role=1)
users.create(name="demo",
             password=md5("123456".encode("utf-8")).hexdigest().upper(),
             apikey=''.join(random.choice(string.letters+string.digits) for _
                            in range(32)))
projects.create(name="pydelo",
                repo_url="https://github.com/meanstrong/pydelo",
                checkout_dir="/data/home/rocky/pydelo/test/checkout",
                target_dir="/data/home/rocky/pydelo/test/target",
                deploy_dir="/data/home/rocky/pydelo/test/deploy",
                deploy_history_dir="/data/home/rocky/pydelo/history")
