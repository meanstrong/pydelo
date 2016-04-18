from web.services.users import users
from web.services.projects import projects

users.create(name="root",
             password="123456")
projects.create(name="pydelo",
                repo_url="",
                checkout_dir="/data/home/rocky/pydelo/test/checkout",
                deploy_dir="/data/home/rocky/pydelo/test/deploy",
                deploy_history_dir="/data/home/rocky/pydelo/history")
