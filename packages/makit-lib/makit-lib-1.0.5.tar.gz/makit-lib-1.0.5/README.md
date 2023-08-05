# makit

#### 介绍

主要提供一些实用的工具类和方法。

#### 安装教程

pip install makit-lib

#### 使用说明

1. logging

    重写了logging模块，扩展level更加简单，写入文件也更加优雅

    ```python
    from makit.lib.logging import Logger

    logger = Logger().write_file('d:\\mylog.log')

    ```
    不需要像原有模块那样很麻烦地增加handler

    自定义level:
    ```python
    from makit.logging import Logger, Level, Fore

    class MyLogger(Logger):
        MyLevel = Level('MyLevel', value=23, color=Fore.LIGHTBLACK_EX)

    ```

2. fn.run 用来正确执行函数，即使参数给多了或者次序错乱也没关系，此方法会处理

    ```python
    from makit.lib import fn

    def hello(name):
        print('hello', name)


    fn.run(hello, name='Nobo', extra=12)
    ```

3. repeat 用来做一些循环控制

    ```python
    # 循环最多100次，持续最多1小时
    for i in repeat(100, duration=3600):
        print(i)
    ```

    ```python
    from makit.lib.loop import Repeat


    def condition(i):
        print(i)
        return i > 49

    Repeat(max_times=100, duration=3600).until(condition)
    ```
    以上代码会运行至50结束

4. 序列化支持
   
    serialize 可以方便对一个对象进行实例化，将其转换为字典

    ```python
    from makit.lib import serialize

    class MyClass:
        def __init__(self):
            self.name = 'myclass'
    
    d = serialize(MyClass(), fields=['name'], exclude_fields=[])
    ```
