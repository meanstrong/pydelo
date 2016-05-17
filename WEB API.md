# 基本说明

## API验证

目前支持两种方式的验证：

1. 在调用login登陆后，会返回一个sign值，在以后的api接口调用中添加到cookie即可，例如：

   ```shell
   $ curl -d "username=demo&password=123456" http://127.0.0.1:9998/api/users/login
   {
     "data": {
       "sign": "UnbvXIf06L3wtSwHMw3C"
     },
     "rc": 0
   }
   $curl -b "sign=UnbvXIf06L3wtSwHMw3C" http://127.0.0.1:9998/api/projects
   {
     "data": {
       "count": 1, 
       "projects": [
         {
           ...
         }
       ]
     },
     "rc": 0
   }
   ```

2. 每个用户都会有一个apikey的字段，把该字段放在url的params里面即可，例如：

   ```shell
   $ curl http://127.0.0.1:9998/api/projects?apikey=FWi14sULr0CwdYqhyBwQfbpdSEV7M8dp
   {
     "data": {
       "count": 1, 
       "projects": [
         {
           ...
         }
       ]
     },
     "rc": 0
   }
   ```


# 登陆

### 登陆
```
path: /api/login
method: POST
params: 
data:
  username: 用户名
  password: 密码
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      sign: 放入cookies中sign字符串
    }
  }
```
# 账户

### 更新账户密码

```
path: /api/accounts/password
method: PUT
data:
  password: 新密码
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```



# 部署（deploys）

### 获取所有部署
```
path: /api/deploys
method: GET
params:
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      count: 总数量
      deploys:
      [
        {
          branch: 本次部署的git分支名称
          comment: 备注
          host_id: 本次部署的host id
          id: 本次部署id
          mode: 本次部署的方式（0：branch的方式；1：tag的方式；2：回滚的方式）
          progress: 本次部署的进度（0 ~ 100）
          project_id: 本次部署的project id
          softln_filename: 本次部署的软连接文件名
          status: 本次部署的status（0：失败；1：成功；2：running）
          created_at: 本次部署创建时间
          updated_at: 本次部署最近更新时间
          user_id: 本次部署的user id
          version: 本次部署的version（当mode为branch方式时表示commit，当mode为tag时表示tag）
          user: {
            apikey: us用户的apikey, 
            created_at: 用户的创建时间, 
            email: 用户的邮箱地址, 
            id: 用户id, 
            name: 用户名称, 
            password: 用户密码, 
            phone: 用户电话, 
            role: 用户角色, 
            updated_at: 用户最近更新时间
          }，
          project: {
            after_checkout:  project代码checkout之后执行的shell
            after_deploy: project部署完成之后执行的shell
            after_rollback:  project回滚完成之后执行的shell
            before_checkout:  project代码checkout之前执行的shell
            before_rollback: project回滚之前执行的shell
            checkout_dir:  project代码checkout的地址
            created_at: project创建时间
            deploy_dir:  project部署的地址
            deploy_history_dir:  project部署的历史版本保存地址
            id:  project id
            name: project名称
            repo_url: project的git地址
            updated_at: project最近更新时间
          },
          host: {
            created_at: host创建时间, 
            id: host id, 
            name: host名称, 
            ssh_host: host ssh连接的IP地址, 
            ssh_pass: host ssh连接的用户密码, 
            ssh_port: host ssh连接的端口号, 
            ssh_user: host ssh连接的用户, 
            updated_at: host最近更新时间
          }
        },
      ]
    }
  }
```
### 创建部署
```
path: /api/deploys
method: POST
params:
  project_id: project id
  host_id: host id
data:
  mode:部署的方式（0：branch的方式；1：tag的方式；2：回滚的方式）
  branch:部署的git分支名称(当mode=0时传此值)
  tag:部署的git tag名称(当mode=1时传此值)
  commit:部署的git分支commit(当mode=0时传此值)
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      id: 本次部署的id
    }
  }
```
### 重新部署
```
path: /api/deploys/:id
method: PUT
params:
  :id: 某次部署的id
data:
  action:部署的方式（"redeploy":完全重新部署；"rollback":回滚至此次部署）
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      id: 部署的id
    }
  }
```
### 获取某次部署的详情
```
path: /api/deploys/:id
method: GET
params:
  :id: 某次部署的id
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      branch: 本次部署的git分支名称
      comment: 备注
      host_id: 本次部署的host id
      id: 本次部署id
      mode: 本次部署的方式（0：branch的方式；1：tag的方式；2：回滚的方式）
      progress: 本次部署的进度（0 ~ 100）
      project_id: 本次部署的project id
      softln_filename: 本次部署的软连接文件名
      status: 本次部署的status（0：失败；1：成功；2：running）
      created_at: 本次部署创建时间
      updated_at: 本次部署最近更新时间
      user_id: 本次部署的user id
      version: 本次部署的version（当mode为branch方式时表示commit，当mode为tag时表示tag）
      user: {
        apikey: us用户的apikey, 
        created_at: 用户的创建时间, 
        email: 用户的邮箱地址, 
        id: 用户id, 
        name: 用户名称, 
        password: 用户密码, 
        phone: 用户电话, 
        role: 用户角色, 
        updated_at: 用户最近更新时间
      }，
      project: {
        after_checkout:  project代码checkout之后执行的shell
        after_deploy: project部署完成之后执行的shell
        after_rollback:  project回滚完成之后执行的shell
        before_checkout:  project代码checkout之前执行的shell
        before_rollback: project回滚之前执行的shell
        checkout_dir:  project代码checkout的地址
        created_at: project创建时间
        deploy_dir:  project部署的地址
        deploy_history_dir:  project部署的历史版本保存地址
        id:  project id
        name: project名称
        repo_url: project的git地址
        updated_at: project最近更新时间
      },
      host: {
        created_at: host创建时间, 
        id: host id, 
        name: host名称, 
        ssh_host: host ssh连接的IP地址, 
        ssh_pass: host ssh连接的用户密码, 
        ssh_port: host ssh连接的端口号, 
        ssh_user: host ssh连接的用户, 
        updated_at: host最近更新时间
      }
    },
  }
```
# 项目（projects）

### 获取所有项目

```
path: /api/projects
method: GET
params:
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: [
      {
        after_checkout:  project代码checkout之后执行的shell
        after_deploy: project部署完成之后执行的shell
        after_rollback:  project回滚完成之后执行的shell
        before_checkout:  project代码checkout之前执行的shell
        before_rollback: project回滚之前执行的shell
        checkout_dir:  project代码checkout的地址
        created_at: project创建时间
        deploy_dir:  project部署的地址
        deploy_history_dir:  project部署的历史版本保存地址
        id:  project id
        name: project名称
        repo_url: project的git地址
        updated_at: project最近更新时间
      },
      ...
    ]
  }
```

### 创建项目

```
path: /api/projects
method: POST
params:
  after_checkout:  project代码checkout之后执行的shell
  after_deploy: project部署完成之后执行的shell
  after_rollback:  project回滚完成之后执行的shell
  before_checkout:  project代码checkout之前执行的shell
  before_rollback: project回滚之前执行的shell
  checkout_dir:  project代码checkout的地址
  deploy_dir:  project部署的地址
  deploy_history_dir:  project部署的历史版本保存地址
  name: project名称
  repo_url: project的git地址
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

### 获取某个项目

```
path: /api/projects/:id
method: GET
params:
  :id 项目id
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      after_checkout:  project代码checkout之后执行的shell
      after_deploy: project部署完成之后执行的shell
      after_rollback:  project回滚完成之后执行的shell
      before_checkout:  project代码checkout之前执行的shell
      before_rollback: project回滚之前执行的shell
      checkout_dir:  project代码checkout的地址
      created_at: project创建时间
      deploy_dir:  project部署的地址
      deploy_history_dir:  project部署的历史版本保存地址
      id:  project id
      name: project名称
      repo_url: project的git地址
      updated_at: project最近更新时间
    }
  }
```

### 更新某个项目

```
path: /api/projects/:id
method: PUT
params:
  :id 项目id
  after_checkout:  project代码checkout之后执行的shell
  after_deploy: project部署完成之后执行的shell
  after_rollback:  project回滚完成之后执行的shell
  before_checkout:  project代码checkout之前执行的shell
  before_rollback: project回滚之前执行的shell
  checkout_dir:  project代码checkout的地址
  deploy_dir:  project部署的地址
  deploy_history_dir:  project部署的历史版本保存地址
  name: project名称
  repo_url: project的git地址
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

### 获取某个项目的git分支列表

```
path: /api/projects/:id/branches
method: GET
params:
  :id 项目id
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: 分支列表，如：["master", "dev"]
  }
```

### 获取某个项目的git某个分支的commit列表

```
path: /api/projects/:id/branches/:branch/commits
method: GET
params:
  :id 项目id
  :branch 分支名称
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: [
      {
        abbreviated_commit 简短commit
        author_name 提交commit的author名
        subject 提交commit的备注
      },
      ...
    ]
  }
```

### 获取某个项目的git tag列表

```
path: /api/projects/:id/tags
method: GET
params:
  :id 项目id
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: tag列表，如["v1.0", "v2.0"]
  }
```

# 主机（hosts）

### 创建主机

```
path: /api/hosts
method: POST
params:
  name: host名称, 
  ssh_host: host ssh连接的IP地址, 
  ssh_pass: host ssh连接的用户密码, 
  ssh_port: host ssh连接的端口号, 
  ssh_user: host ssh连接的用户, 
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

### 获取所有主机列表

```
path: /api/hosts
method: GET
params:
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: 
    [
      {
        created_at: host创建时间, 
        id: host id, 
        name: host名称, 
        ssh_host: host ssh连接的IP地址, 
        ssh_pass: host ssh连接的用户密码, 
        ssh_port: host ssh连接的端口号, 
        ssh_user: host ssh连接的用户, 
        updated_at: host最近更新时间
      },
    ...
    ]
  }
```

### 获取某个主机

```
path: /api/hosts/:id
method: GET
params:
  :id 主机id
  offset: 数据偏移量
  limit: 数据个数
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data: {
      created_at: host创建时间, 
      id: host id, 
      name: host名称, 
      ssh_host: host ssh连接的IP地址, 
      ssh_pass: host ssh连接的用户密码, 
      ssh_port: host ssh连接的端口号, 
      ssh_user: host ssh连接的用户, 
      updated_at: host最近更新时间
    },
    ...
  }
```

### 更新某个主机

```
path: /api/hosts/:id
method: PUT
params:
  name: host名称, 
  ssh_host: host ssh连接的IP地址, 
  ssh_pass: host ssh连接的用户密码, 
  ssh_port: host ssh连接的端口号, 
  ssh_user: host ssh连接的用户, 
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

# 用户（users）

### 创建用户

```
path: /api/users
method: POST
params: 
  email: 用户的邮箱地址,  
  name: 用户名称, 
  phone: 用户电话, 
  role: 用户角色, 
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

### 获取所有用户

```
path: /api/users
method: GET
params: 
  offset: 数据偏移量
  limit: 数据个数 
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    [
      {
        apikey: us用户的apikey, 
        created_at: 用户的创建时间, 
        email: 用户的邮箱地址, 
        id: 用户id, 
        name: 用户名称, 
        password: 用户密码, 
        phone: 用户电话, 
        role: 用户角色, 
        updated_at: 用户最近更新时间
      },
      ...
    ]
  }
```

### 获取某个用户

```
path: /api/users/:id
method: GET
params: 
  :id 用户id
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    {
      apikey: us用户的apikey, 
      created_at: 用户的创建时间, 
      email: 用户的邮箱地址, 
      id: 用户id, 
      name: 用户名称, 
      password: 用户密码, 
      phone: 用户电话, 
      role: 用户角色, 
      updated_at: 用户最近更新时间
    },
  }
```

### 获取用户拥有的主机列表

```
path: /api/users/:id/hosts
method: GET
params: 
  :id 用户id
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    [
      {
        created_at: host创建时间, 
        id: host id, 
        name: host名称, 
        ssh_host: host ssh连接的IP地址, 
        ssh_pass: host ssh连接的用户密码, 
        ssh_port: host ssh连接的端口号, 
        ssh_user: host ssh连接的用户, 
        updated_at: host最近更新时间
      },
      ...
    ]
  }
```

### 更新用户所拥有的主机列表

```
path: /api/users/:id/hosts
method: PUT
params: 
  :id 用户id
data:
  hosts[] 主机id列表
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

### 获取用户拥有的项目列表

```
path: /api/users/:id/projects
method: GET
params: 
  :id 用户id
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
    data:
    [
      {
        after_checkout:  project代码checkout之后执行的shell
        after_deploy: project部署完成之后执行的shell
        after_rollback:  project回滚完成之后执行的shell
        before_checkout:  project代码checkout之前执行的shell
        before_rollback: project回滚之前执行的shell
        checkout_dir:  project代码checkout的地址
        created_at: project创建时间
        deploy_dir:  project部署的地址
        deploy_history_dir:  project部署的历史版本保存地址
        id:  project id
        name: project名称
        repo_url: project的git地址
        updated_at: project最近更新时间
      },
      ...
    ]
  }
```

### 更新用户所拥有的项目列表

```
path: /api/users/:id/projects
method: PUT
params: 
  :id 用户id
data:
  projects[] 项目id列表
result:
  {
    rc: 错误码（0表示OK）
    msg: 错误信息
  }
```

