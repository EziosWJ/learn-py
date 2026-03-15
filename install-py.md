# 过程记录

### uv
```shell

curl -LsSf https://astral.sh/uv/install.sh | sh

source ~/.bashrc


uv --version
#uv 0.10.10

uv python install 3.12

uv python list

```

### mirrors

```shell

# 全局

mkdir -p ~/.config/uv
nano ~/.config/uv/uv.toml

```

```toml
[[index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

### 新建项目

```shell
wangjian@WJPC:~/py/learn-django$ uv init
Initialized project `learn-django`
wangjian@WJPC:~/py/learn-django$ uv venv
Using CPython 3.12.13
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
wangjian@WJPC:~/py/learn-django$ source .venv/bin/activate
(learn-django) wangjian@WJPC:~/py/learn-django$ 
```

### uv command

| 命令                    | 作用           |
| --------------------- | ------------ |
| uv init               | 创建 Python 项目 |
| uv venv               | 创建虚拟环境       |
| uv add django         | 安装依赖         |
| uv remove django      | 删除依赖         |
| uv sync               | 同步依赖         |
| uv pip list           | 查看依赖         |
| uv run python main.py | 运行脚本         |
