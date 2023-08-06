'''
luckylog
author: 测码课堂-范晔
Email: 1538379200@qq.com
有任何问题或者建议请联系邮箱
v0.0.1
日志模板
目前仅支持自定义消息处理
使用log请直接再文件中导入  from luckylog.luckylog import Logger
如需要保存为文件，则需要导入整个文件获取全局变量 from luckylog import luckylog
执行：Logger.success(xxx)
文件中有两个全局变量，当设置 path 为保存的文件位置和格式，module为选择保存的类型
module = 'success,error,warning,tip' 目前有四种类型的日志消息
目前展示类型：运行时间、函数名称、文件路径、状态、行数,格式固定,固定调用即显示
success：成功； error：错误； warning：警告； tip：提示；

添加装饰器功能：
装饰器使用： from luckylog.luckylog import logger  （注意是小写的l）
装饰器自带两个参数，success和error，代表自定义的成功和失败自定义消息
使用：在需要使用的def放上  @logger(success=xxx,fail=xxx)
如果不定义消息，则默认成功为--Success，失败为--Fail
使用装饰器后可不用带异常错误处理
装饰器不能用在类class上，可能出现报错而日志显示成功的情况

增设全局变量debug_file，当debug_file传入文件路径时(包含文件本身及格式)，系统将判断函数执行正确性，失败则将报错写入路径中的文件
函数运行成功将不会保存并写入文件
debug_file保存内容：运行事件，函数名称，文件路径，报错信息
！！！！！debug_file的保存文件方式，目前仅支持 @logger() 装饰器形式的启用！！！！！

v1.0.0
Logger改为元组形式，可输入不限定参数
装饰器增加Debug模式，from luckylog import luckylog
luckylog.Debug = True   可开启debug模式，默认关闭状态
Debug模式开启，使用装饰器，成功增加返回输入参数，失败增加返回参数和异常报错信息   Arguments/Exception
错误日志增加输入参数

v1.0.3
1、修改书写错误worning改成warning，以前写法仍旧可用
2、修改书写错误erro改成error，方法名替换

v1.0.4
1、修复使用装饰器不能进行值返回的bug
'''

import time
import sys
from functools import wraps
import threading


path = None  # 日志文件保存路径和文件名(Logger写入)
module = None  # 选择保存哪种类型的日志(Logger写入)
debug_file = None  # 保存错误信息的路径和文件名(logger装饰器使用)
Debug: bool = False  # 是否开启调试模式(logger装饰器使用)

'''定义关于日志输出的格式'''


class LogConfig():
    __num = 2

    def conf_success(self, *args, **kwargs) -> str:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        def_name = sys._getframe(self.__num).f_code.co_name
        line = sys._getframe(self.__num).f_lineno
        file_path = sys._getframe(self.__num).f_code.co_filename

        return '(p≧w≦q) === {} FILE_PATH=({}) FUNC-({}) <SUCCESS> LINE-{} *MSG==√{} ==='.format(now_time, file_path,
                                                                                                def_name, line, args,
                                                                                                kwargs)

    def conf_erro(self, *args, **kwargs) -> str:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        def_name = sys._getframe(self.__num).f_code.co_name
        line = sys._getframe(self.__num).f_lineno
        file_path = sys._getframe(self.__num).f_code.co_filename
        return 'φ(゜▽゜*)♪ === {} FILE_PATH=({}) FUNC-({}) <ERRO> LINE-{} *MSG==×{} ==='.format(now_time, file_path,
                                                                                              def_name, line, args,
                                                                                              kwargs)

    def conf_warning(self, *args, **kwargs) -> str:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        def_name = sys._getframe(self.__num).f_code.co_name
        line = sys._getframe(self.__num).f_lineno
        file_path = sys._getframe(self.__num).f_code.co_filename
        return 'o(*￣▽￣*)ブ === {} FILE_PATH=({}) FUNC-({}) <WORNING> LINE-{} *MSG==!{} ==='.format(now_time, file_path,
                                                                                                  def_name, line, args,
                                                                                                  kwargs)

    def conf_normal(self, *args, **kwargs) -> str:
        now_time = time.strftime('%Y-%m-%d %H:%M:%S')
        def_name = sys._getframe(2).f_code.co_name
        line = sys._getframe(2).f_lineno
        file_path = sys._getframe(self.__num).f_code.co_filename
        return 'm（￣︶￣）↗ === {} FILE_PATH=({}) FUNC-({}) <TIP> LINE-{} *MSG=={} ==='.format(now_time, file_path,
                                                                                           def_name, line, args, kwargs)


'''进行是否存入文件的方法，给文字添加颜色'''


class Logger():
    __lock = threading.RLock()

    @staticmethod
    def success(*args, **kwargs):
        Logger.__lock.acquire()
        print('\033[1;50;32m{}\033[0m'.format(LogConfig().conf_success(*args, **kwargs)))
        if path and ('success' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(LogConfig().conf_success(*args) + '\n')
        else:
            pass
        Logger.__lock.release()

    @staticmethod
    def error(*args, **kwargs):
        Logger.__lock.acquire()
        print('\033[1;50;31m{}\033[0m'.format(LogConfig().conf_erro(*args, **kwargs)))
        if path and ('error' or 'erro' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(LogConfig().conf_erro(*args, **kwargs) + '\n')
        else:
            pass
        Logger.__lock.release()

    @staticmethod
    def warning(*args, **kwargs):
        Logger.__lock.acquire()
        print('\033[1;50;33m{}\033[0m'.format(LogConfig().conf_warning(*args, **kwargs)))
        if path and ('warning' or 'worning' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(LogConfig().conf_warning(*args, **kwargs) + '\n')
        else:
            pass
        Logger.__lock.release()

    @staticmethod
    def tip(*args, **kwargs):
        Logger.__lock.acquire()
        print('\033[1;50;34m{}\033[0m'.format(LogConfig().conf_normal(*args, **kwargs)))
        if path and ('tip' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(LogConfig().conf_normal(*args, **kwargs) + '\n')
        else:
            pass
        Logger.__lock.release()


'''
下面是作为装饰器的方法配置
因为调用不能准确获取运行的行数，所以重新创建新的class，不继承直接另写
'''


class __Getlog():
    def success(self, now_time, file_path, def_name, line, msg, info):
        if Debug:
            msg_value = '(p≧w≦q) === {} FILE_PATH=({}) FUNC-({}) <SUCCESS> LINE-{} Arguments={} *MSG==√{}==='.format(
                now_time, file_path, def_name, line, info, msg)
        else:
            msg_value = '(p≧w≦q) === {} FILE_PATH=({}) FUNC-({}) <SUCCESS> LINE-{} *MSG==√{} ==='.format(now_time,
                                                                                                         file_path,
                                                                                                         def_name, line,
                                                                                                         msg)
        print('\033[1;50;32m{}\033[0m'.format(msg_value))
        if path and ('success' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(msg_value + '\n')
        else:
            pass

    def error(self, now_time, file_path, def_name, line, msg, info, erro):
        if Debug:
            msg_value = 'φ(゜▽゜*)♪ === {} FILE_PATH=({}) FUNC-({}) <ERRO> LINE-{} Arguments={} *MSG==×{} \n Exception:{}===='.format(
                now_time, file_path, def_name, line, info, msg, erro)
        else:
            msg_value = 'φ(゜▽゜*)♪ === {} FILE_PATH=({}) FUNC-({}) <ERRO> LINE-{} *MSG==×{} ===='.format(
                now_time, file_path, def_name, line, msg)
        print('\033[1;50;31m{}\033[0m'.format(msg_value))
        if path and ('erro' in module):
            with open(path, 'a', encoding='utf-8') as f:
                f.writelines(msg_value + '\n')
        else:
            pass


'''
装饰器模块：
在def上使用 @logger()，括号中可填入自定义成功失败消息，不填写则显示默认
当Debug模式为True时，成功会增加显示输入的参数，失败会增加显示参数和异常报错
使用装饰器则无需在def中使用try方法
'''


def logger(success='Success', fail='Fail'):
    def get_logger(func):
        @wraps(func)
        def get_func(*args, **kwargs):
            def get_args(*args, **kwargs):
                save_arg = locals()
                return save_arg

            __lcok = threading.RLock()
            __lcok.acquire()
            try:
                res = func(*args, **kwargs)
                argument = get_args(*args, **kwargs)
                now_time = time.strftime('%Y-%m-%d %H:%M:%S')
                def_name = func.__name__
                line = sys._getframe(1).f_lineno
                file_path = sys._getframe(1).f_code.co_filename
                __Getlog().success(now_time, file_path, def_name, line, success, argument)
                return res
            except Exception as e:
                now_time = time.strftime('%Y-%m-%d %H:%M:%S')
                def_name = func.__name__
                argument = get_args(*args, *kwargs)
                line = sys._getframe(1).f_lineno
                file_path = sys._getframe(1).f_code.co_filename
                __Getlog().error(now_time, file_path, def_name, line, fail, argument, e)
                if debug_file:
                    with open(debug_file, 'a', encoding='utf-8') as d_file:
                        d_file.writelines(
                            '========{0} *FUNC_NAME=({1}) *FILE_PATH=({2})========\n*Arguments={3}\n*ERRO_INFO=({4})'.format(
                                now_time, def_name, file_path, argument, e) + '\n' + '\n')
                else:
                    pass
            __lcok.release()

        return get_func

    return get_logger
