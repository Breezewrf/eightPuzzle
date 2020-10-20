<div><img src="https://img.shields.io/pypi/pyversions/Django" align="right"><img src="https://img.shields.io/apm/l/vim-mode" align="right">
</div>

# <font color=#43C size=8 face="黑体">eightPuzzle</font>
- [x] README
  - [x] 徽章（可以是使用的语言或者其他）
  - [x] 运行环境
  - [x] 编译方法
  - [x] 使用方法

- [x] .gitignore
- [x] Commit信息（需要有意义的提交信息占比90%）
- [x] 使用分支管理提交代码，使用pull request
- [x] 开源协议
- [ ] 持续集成
- [x] Issues模板

# 运行环境：

`python3`

`pip install opencv-python`

`pip install simpleguitk`

**需要手动设置source root**

# 编译方法：

## 1、大比拼

./PK 目录下的为大比拼所用到的文件

```
│  ai7.py  -- 初始的ai算法，速度较慢
│  ai9.py  -- 改进后的ai算法，采用优先队列
		    - 提供接口函数ai(initState, goalState, swap, step)以便大比拼调用
		      返回交换位置和所有路径
│  clip.py -- 将path中的所有图片裁剪九等分存入topath文件夹
│  utils.py-- 测试时使用的代码
		    - 提供了函数用以生成图片识别所用的索引
		    - 提供了函数用以生成图片对应序列
│  interface.py
           --此文件是用于ai大比拼的具体代码
│  logs.txt-- 测试时的部分log
```

## 2、GUI

运行main_v3.py即可