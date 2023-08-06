# 将项目打包/构建为Python包

## 1. 创建虚拟环境 env

```bash
python -m venv env
```

## 2. 安装打包工具 Flit

```bash
python -m pip install flit==3.7.1
```

## 3. 构建Python包(.whl)

```bash
flit build  
```

