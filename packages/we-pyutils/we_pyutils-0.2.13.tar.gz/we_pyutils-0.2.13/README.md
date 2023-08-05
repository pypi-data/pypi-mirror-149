# we_pyutils

> WE Python Utils

## 上传

```sh
python setup.py bdist_egg # 生成类似 edssdk-0.0.1-py2.7.egg，支持 easy_install
python setup.py sdist     # 生成类似 edssdk-0.0.1.tar.gz，支持 pip
twine upload dist/we_pyutils-0.2.X.tar.gz
```

## 配置

初始环境配置

```shell
py -m pip install --upgrade build
py -m pip install --upgrade twine
```

生成并上传

```shell
py -m build
#py -m twine upload --repository testpypi dist/*
py -m twine upload dist/*
```
