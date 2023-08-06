import json
import asyncio
import os.path
from urllib.parse import urljoin
from time import sleep
from os import makedirs, getpid
from threading import Thread
from typing import Dict, List

import httpx
from fastapi import FastAPI, Request, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from mfhm.log import getLogger
from mfhm.errors import PathError


# -------------------------------------------------
# 服务上线参数校验模型
class ServiceOnlineMethodModel(BaseModel):
    path:str = Field(..., min_length=1, max_length=10240)
    methods:List[str]


class ServiceOnlineModel(BaseModel):
    name:str = Field(..., min_length=1, max_length=500)
    port:int = Field(..., ge=1, le=65535)
    methods: Dict[str, ServiceOnlineMethodModel]


class ServiceCenter(object):
    '''
    服务中心
    '''

    def __init__(
            self, 
            host:str = '0.0.0.0', 
            port:int = 21428,
            pingTestInterval:int = 10,
            pingTestTimeout:int = 5,
            cacheSaveInterval:int = 60,
            dataDir:str = None,
            cacheFilename:str = 'centerCache.json',
            logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            asyncHttpClient = httpx.AsyncClient()
    ) -> None:
        '''
        Args:
            host: 服务中心主机地址
            port: 服务中心监听端口
            pingTestInterval: ping测试时间间隔, 服务中心会定时向服务发送一个ping
                              测试请求用于测试服务是否在线, 并且会根据该ping测试
                              的响应时长作为负载均衡的的调度依据, 该值单位为秒
            pingTestTimeout: ping测试的超时时间, 如果被托管的服务未在该指定时间内
                             响应服务中心的ping测试请求, 则服务中心会将该服务视为
                             已掉线, 该服务的信息将会从服务中心移除并等待重新上线,
                             该参数值单位为秒且值不能大于参数pingTestInterval的
                             值
            cacheSaveInterval: 缓存定时保存时间间隔, 单位为秒. 服务中心将所有的服务
                               数据存储在内存中, 当服务中心意外掉线或重启时会造成托
                               管的服务数据丢失, 所以会定时将服务数据定时持久化到磁
                               盘中
            dataDir: 数据存储目录
            cacheFilename: 缓存文件名称
            logger: 日志对象
            asyncHttpClient: HTTPX的异步会话客户端
        '''
        self.host = host
        self.port = port
        self.pingTestInterval = pingTestInterval
        self.pingTestTimeout = pingTestTimeout
        self.cacheSaveInterval = cacheSaveInterval
        self.dataDir = dataDir
        self.cacheFilename = cacheFilename
        self.logger = logger
        self.asyncHttpClient = asyncHttpClient
        self.pid = None

        # 本地缓存, 用于存储服务信息, 格式如下
        # {
        #     serviceName: [
        #         {
        #             'host': serviceHost,
        #             'port': servicePort,
        #             'ping': pingTestValue,
        #             'methods': {
        #                 apiName: {
        #                     'path': 'apiUrlPath',
        #                     'methods': 'apiHttpMethods'
        #                 },
        #                 .......
        #             }
        #         },
        #         .........
        #     ],
        #     .......
        # }
        self.__cache = {}
        self.loadCache()

        self.app = FastAPI()
        # 服务关闭后写立即保存缓存
        self.app.add_event_handler('shutdown', self.saveCache)
        # 绑定路由处理函数
        self.app.add_api_route('/online', self.online, methods=['POST'], name='online')
        self.app.add_api_route('/offline/{name}/{port}', self.offline, methods=['DELETE'], name='offline')
        self.app.add_api_route('/service/{name}', self.serviceInfo, methods=['GET'], name='service')
        self.app.add_api_route('/api/{name}/{apiName}', self.apiInfo, methods=['GET'], name='api')

        # 缓存定时保存线程
        cacheSaveThread = Thread(target=self.__cycleSaveCache, daemon=True)
        cacheSaveThread.start()

        # ping定时测试线程
        pingTestThread = Thread(target=self.__runPingTest, daemon=True)
        pingTestThread.start()

    @property
    def dataDir(self):
        return self.__dataDir

    @dataDir.setter
    def dataDir(self, value:str):
        # 未指定数据存储目录时, 使用当前目录下的data目录作为数据目录
        if value == None:
            self.__dataDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            self.__makeSureDir(self.__dataDir)
            return None

        if not isinstance(value, str):
            raise ValueError(f'dataDir参数应该是{str}类型的值')

        # 如果提供了一个已存在的路径
        if os.path.exists(value):
            # 且路径是文件的
            if os.path.isfile(value):
                raise PathError(f'"{value}" 路径指向了一个文件, 无法将此路径作为数据存储目录')
        # 否则创建目录
        else:
            self.__makeSureDir(value)

        self.__dataDir = value
            
    @staticmethod
    def __makeSureDir(dirPath:str) -> None:
        '''
        确保目录存在, 如果dirPath已存在则忽略, 否则将会创建目录
        '''
        try:
            makedirs(dirPath)
        except Exception as err:
            pass

    def __cycleSaveCache(self) -> None:
        '''
        周期调用缓存保存方法将缓存保存到磁盘
        '''
        while True:
            self.saveCache()
            sleep(self.cacheSaveInterval)

    def __deleteService(self, name:str, host:str, port:int) -> bool:
        '''
        从缓存中删除一个服务信息

        Args:
            name: 服务名称
            host: 服务主机地址
            port: 服务端口
        '''
        name = name.strip()
        for serviceName in self.__cache:
            # 找到指定名称的服务
            if serviceName == name:
                # 找到主机地址和端口一致的服务信息
                for oneServiceData in self.__cache[serviceName]:
                    if oneServiceData['host'] == host and oneServiceData['port'] == port:
                        # 从缓存中移除改服务信息
                        self.__cache[serviceName].remove(oneServiceData)
                        return True
        return False

    async def __onePingTest(self, name:str, serviceData: dict) -> None:
        '''
        向单个被托管服务发送ping测试

        Args:
            name: 服务名称
            serviceData: 服务信息数据       
        '''
        host = serviceData['host']
        port = serviceData['port']
        url = f'http://{host}:{port}/ping'
        try:
            response = await self.asyncHttpClient.get(url, timeout=self.pingTestTimeout)
            self.logger.debug(f'Ping test: [{name}]{url}')
        except Exception as err:
            # 测试失败时讲服务视为已掉线, 从缓存中移除服务数据
            self.__deleteService(name=name, host=host, port=port)
            self.logger.warning(f'ping test failed [{name}]{url}, remove service data: {err}')
            return None
        
        # 响应时长
        serviceData['ping'] = response.elapsed.total_seconds()

    async def __pingTest(self):
        '''
        向服被托管服务发送ping测试并记录响应时长
        '''
        while True:
            for serviceName in self.__cache:
                for serviceData in self.__cache[serviceName]:
                    await self.__onePingTest(name=serviceName, serviceData=serviceData)
            await asyncio.sleep(self.pingTestInterval)

    def __runPingTest(self):
        '''
        启动ping测试
        '''
        asyncio.run(self.__pingTest())

    def saveCache(self) -> bool:
        '''
        将缓存保存到磁盘

        Args:
            saveDir: 保存目录的路径
            cacheFilename: 保存的文件名称

        Returns:
            True: 保存成功
            False: 保存失败
        '''
        saveFilePath = os.path.join(self.dataDir, self.cacheFilename)

        try:        
            with open(saveFilePath, 'w', encoding='utf-8') as f:
                json.dump(self.__cache, f)
        except Exception as err:
            self.logger.warning(f'Cache save failure, all service data lost after service restart/exit: {err}')
            return False

        return True

    def loadCache(self) -> bool:
        '''
        从磁盘加载缓存
        '''
        cacheFilePath = os.path.join(self.dataDir, self.cacheFilename)
        if os.path.isfile(cacheFilePath):
            try:
                with open(cacheFilePath, 'r', encoding='utf-8') as f:
                    self.__cache = json.load(f)
                return True
            except Exception as err:
                self.logger.critical(f'Cache load failure: {err}')

        return False

    async def online(self, request:Request, serviceData: ServiceOnlineModel):
        '''
        服务上线

        Args:
            request: 请求对象, 用于获取客户端的请求信息
            serviceData: 待上线服务的信息数据, 格式如下:
                        {
                            'name': '服务名称',
                            'port': '服务端口',
                            'methods': {
                                '方法名称': {
                                    'path': '该方法调用地址的path'
                                }
                            }
                        }

        Returns:
            HTTP Code 200: 请求处理成功, 返回一个JSON {'code': xx, 'message': 'xxx'}
                code: 状态码
                     0: 服务上线成功
                    -1: 服务已上线, 不能重复上线
                message: 各状态码对应的提示消息
            HTTP Code 422: 请求参数错误
            HTTP Code 500: 服务内部错误
        '''
        result = {'code': 0, 'message': 'ok'}
        serviceData = serviceData.dict()

        serviceHost = request.client.host

        # 如果请求上线的服务已在缓存中存在同名服务
        serviceName = serviceData['name'].strip()
        if serviceName in self.__cache:
            # 通过服务地址和服务端口判断是否为同一个服务
            for cacheServiceData in self.__cache[serviceName]:
                if serviceHost == cacheServiceData['host'] and serviceData['port'] == cacheServiceData['port']:
                   result['code'] = -1
                   result['message'] = 'Service is online'
                   return result
        else:
            self.__cache[serviceName] = []
        
        # 上线成功, 向缓存中写入服务信息
        self.__cache[serviceName].append({
            'host': serviceHost,
            'port': serviceData['port'],
            'ping': -1,
            'methods': serviceData['methods']
        })

        return result 

    async def offline(
            self, 
            request:Request,
            name:str = Path(..., min_length=1, max_length=500), 
            port:int = Path(..., ge=1, le=65535)
    ):
        '''
        服务下线

        Args:
            request: 请求对象, 用于获取客户端的请求信息
            name: 待下线的服务名称
            port: 待下线的服务的端口

        Returns:
            HTTP Code 200: 请求处理成功, 返回一个JSON {'code': xx, 'message': 'xx'}
                code: 状态码
                     0: 服务下线成功
                    -1: 下线服务不存在
            HTTP Code 422: 请求参数错误
            HTTP Code 500: 服务内部错误
        '''
        result = {'code': 0, 'message': 'ok'}

        name = name.strip()
        host = request.client.host

        if not self.__deleteService(name=name, host=host, port=port):
            result['code'] = -1
            result['message'] = 'Service not online'

        return result

    async def serviceInfo(self, name:str = Path(..., min_length=1, max_length=500)):
        '''
        服务信息获取接口

        Returns:
            HTTP Code 404: 服务接口不存在, 返回一个包含错误信息的JSON
            HTTP Code 422: 请求参数错误
            HTTP Code 200: 请求处理成功, 返回一个包含接口信息的JSON
            HTTP Code 500: 服务内部错误
        '''
        result = {
            'code': 0, 
            'message': 'ok',
            'name': '',
            'host': '',
            'port': '',
            'methods': {}
        }

        name = name.strip()

        if name in self.__cache:
            # 找到ping值最小的服务
            pingValue = None
            minPingValueServiceData = None

            for serviceData in self.__cache[name]:
                # 使用首个服务数据作为初始值
                if pingValue == None:
                    pingValue = serviceData['ping']
                    minPingValueServiceData = serviceData
                # 两个以上服务时进行ping值对比
                elif serviceData['ping'] < pingValue:
                    pingValue = serviceData['ping']
                    minPingValueServiceData = serviceData

            if minPingValueServiceData:
                result['name'] = name
                result['host'] = minPingValueServiceData['host']
                result['port'] = minPingValueServiceData['port']
                result['methods'] = minPingValueServiceData['methods']
                return result

        result['code'] = -1
        result['message'] = 'Service not online'
        return JSONResponse(
            status_code=404, 
            content=result
        )

    async def apiInfo(
            self,
            name:str = Path(..., min_length=1, max_length=500),
            apiName:str = Path(..., min_length=1, max_length=500)
    ):
        '''
        服务接口信息获取接口

        Returns:
            HTTP Code 404: 服务接口不存在, 返回一个包含错误信息的JSON
            HTTP Code 422: 请求参数错误
            HTTP Code 200: 请求处理成功, 返回一个包含接口信息的JSON
            HTTP Code 500: 服务内部错误
        '''
        result = {'code': 0, 'message': 'ok', 'apiUrl': '', 'apiMethods': []}

        name = name.strip()
        apiName = apiName.strip()

        if name in self.__cache:
            # 找到ping值最小的服务
            pingValue = None
            minPingValueServiceData = None

            for serviceData in self.__cache[name]:
                # 使用首个服务数据作为初始值
                if pingValue == None:
                    pingValue = serviceData['ping']
                    minPingValueServiceData = serviceData
                # 两个以上服务时进行ping值对比
                elif serviceData['ping'] < pingValue:
                    pingValue = serviceData['ping']
                    minPingValueServiceData = serviceData

            # 从服务中查询API信息
            if minPingValueServiceData:
                for methodName in minPingValueServiceData['methods']:
                    if methodName == apiName:
                        apiPath = serviceData['methods'][methodName]['path']
                        result['apiUrl'] = urljoin(f'http://{serviceData["host"]}:{serviceData["port"]}', apiPath)
                        result['apiMethods'] = serviceData['methods'][methodName]['methods']
                        return result

        result['code'] = -1
        result['message'] = 'Service not online'
        return JSONResponse(
            status_code=404, 
            content=result
        )

    def start(self):
        '''
        启动服务
        '''
        import uvicorn 
        self.pid = getpid()

        # 覆盖uvicorn默认日志配置, 转用log模块提供的日志处理程序, 
        # 统一日志格式
        logConfig = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    '()': 'mfhm.log.Formatter'
                }
            },
            'handlers': {
                'default': {
                    'formatter': 'default',
                    'class': 'mfhm.log.ConsoleHighlightedHandler',
                }
            },
            'loggers': {
                'uvicorn': {
                    'handlers': ['default'],
                    'level': 'INFO'
                },
                'uvicorn.error': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False
                },
                'uvicorn.access': {
                    'handlers': ['default'],
                    'level': 'INFO',
                    'propagate': False
                }
            }
        }

        uvicorn.run(self.app, host=self.host, port=self.port, debug=False, log_config=logConfig)

