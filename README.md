# Python template

## 环境设置

### 安装 Python

```bash
wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz
```

### 安装 cookiecutter

cookiecutter 是一个用于生成项目模板的工具。它可以使用已有的 github repo 作为模版生成新的项目。

```bash
cookiecutter gh:Anniext/cookiecutter
```

### 安装 pre-commit

pre-commit 是一个代码检查工具，可以在提交代码前进行代码检查。

```bash
pipx install pre-commit
```

安装成功后运行 `pre-commit install` 即可。

### 安装 typos

typos 是一个拼写检查工具。

```bash
cargo install typos-cli
```

### 安装 git cliff

git cliff 是一个生成 changelog 的工具。

```bash
cargo install git-cliff
```

读取cliff.toml 生成更变日志

```bash
git cliff --output CHANGELOG.md
```
