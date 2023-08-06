from distutils.core import setup
setup(
    name='computer-m', # 对外我们模块的名字
    version='1.0', # 版本号
    description='测试的计算模块', #描述
    author='xiejl', # 作者
    author_email='xiejianglei163@163.com',
    py_modules=['computer.Add','computer.Mul'] # 要发布的模块
)