# -*- coding: UTF-8 -*-
##Version: 0.0.1
日志模板
目前仅支持自定义消息处理
使用log请直接再文件中导入  from luckylog import Logger
如需要保存为文件，则需要导入整个文件获取全局变量  import logger
执行：Logger.sccess(xxx)
文件中有两个全局变量，当设置 path 为保存的文件位置和格式，module为选择保存的类型
module = 'success,error,warning,tip' 目前有四种类型的日志消息
目前展示类型：运行时间、函数名称、文件路径、状态、行数,格式固定,固定调用即显示
success：成功； error：错误； warning：警告； tip：提示；

添加装饰器功能：
装饰器使用： from luckylog import logger  （注意是小写的l）
装饰器自带两个参数，success和fail，代表自定义的成功和失败自定义消息
使用：在需要使用的def放上  @logger(success=xxx,fail=xxx)
如果不定义消息，则默认成功为--Success，失败为--Fail
使用装饰器后可不用带异常错误处理
装饰器不能用在类class上，可能出现报错而日志显示成功的情况

增设全局变量debug_file，当debug_file传入文件路径时(包含文件本身及格式)，系统将判断函数执行正确性，失败则将报错写入路径中的文件
函数运行成功将不会保存并写入文件
debug_file保存内容：运行事件，函数名称，文件路径，报错信息
！！！！！debug_file的保存文件方式，目前仅支持 @logger() 装饰器形式的启用！！！！！

## v1.0.0
Logger改为元组形式，可输入不限定参数
装饰器增加Debug模式，from luckylog import luckylog
luckylog.Debug = True   可开启debug模式，默认关闭状态
Debug模式开启，使用装饰器，成功增加返回输入参数，失败增加返回参数和异常报错信息   Arguments/Exception
错误日志增加输入参数

## v1.0.3
1、修改书写错误worning改成warning，以前写法仍旧可用
2、修改书写错误erro改成error，方法名替换

## v1.0.4
1、修复装饰器使用不能获取返回值的bug
