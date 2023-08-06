# bloggart

#### 介绍
极速构建博客，内嵌server/database，适合全栈

#### 软件架构
软件架构说明


#### 安装教程

1.  pip3 install -i https://mirrors.aliyun.com/pypi/simple/ tornado
2.  xxxx
3.  xxxx

#### 使用说明

1.  直接使用`bloggart`命令
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

# 直接用

# 间接用

二次开发

# 注意

安全性完全没有

## 发布

```bash
python3 -m venv bloggart-venv/
source bloggart-venv/bin/activate.fish

# 调试好之后
python3 -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ setuptools wheel
python3 setup.py sdist bdist_wheel

pip3 freeze > requirements.txt
# requirements添加一个peppercorn
echo 'peppercorn' >> requirements.txt
pip3 download -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ -d dist/

cd dist/
dir2pi -S .
scp -r simple/ root@39.97.232.223:/root/pypi/
pip3 install -i http://www.hohohaha.cn:8000/simple/ bloggart==0.0.2 --trusted-host www.hohohaha.cn
```

## 上传到pypi

```bash
python3 setup.py sdist bdist_wheel
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ twine
python3 -m twine upload dist/*
```