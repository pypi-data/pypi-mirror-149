import os.path
from os import getpid
from logging import Logger

from fastapi import FastAPI
from httpx import Client

from mfhm.log import getLogger
from mfhm.errors import OnlineError, ServiceStartError


class Service(FastAPI):
    '''
    微服务类, 表示一个微服务
    '''
    def __init__(
            self, 
            serviceName:str,
            serviceHost:str = '0.0.0.0',
            servicePort:int = 30176,
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:Client = Client(timeout=5),
            *args, 
            **kwargs
    ):
        '''
        Args:
            serviceName: 服务名称
            serviceHost: 服务主机地址
            servicePort: 服务端口
            centerProtocol: 服务中心使用的协议
            centerHost: 服务中心地址
            centerPort: 服务中心端口
            logger: 日志对象
            httpClient: HTTPX客户端
        '''
        super().__init__(*args, **kwargs)
        self.serviceName = serviceName
        self.serviceHost = serviceHost
        self.servicePort = servicePort
        self.centerProtocol = centerProtocol
        self.centerHost = centerHost
        self.centerPort = centerPort
        self.centerBaseUri = f'{self.centerProtocol}://{self.centerHost}:{self.centerPort}'
        self.logger = logger
        self.httpClient = httpClient
        self.pid = None

        # 注册内置路由
        self.add_api_route('/ping', self.ping, methods=['GET'], name='ping')

        # 服务退出时发送下线请求
        self.add_event_handler('shutdown', self.offline)

    def online(self) -> None:
        '''
        向服务中心发出上线请求
        '''
        # 当前服务的所有路由
        methods = {}
        for route in self.routes:
            methods[route.name] = {'path': route.path, 'methods': list(route.methods)}

        url = f'{self.centerBaseUri}/online'
        try:
            response = self.httpClient.post(url, json={
                'name': self.serviceName,
                'port': self.servicePort,
                'methods': methods
            })
            responseData = response.json()
        except Exception as err:
            errorMessage = f'Service online failure, unable to communicate properly with the service center: {err}'
            self.logger.critical(errorMessage)
            raise OnlineError(errorMessage)

        if not response.status_code == 200:
            errorMessage = f'The service has failed to go live, and the service center has returned an error:\n'
            errorMessage += f'    HTTP code: {response.status_code}\n'
            errorMessage += f'    Data: {responseData}\n'
            self.logger.critical(errorMessage)
            raise OnlineError(errorMessage)

        if not responseData['code'] == 0:
            errorMessage = f'The service has failed to go live, and the service center has returned an error:\n'
            errorMessage += f'    Status code: {responseData["code"]}\n'
            errorMessage += f'    Message: {responseData["message"]}\n'
            self.logger.critical(errorMessage)
            raise OnlineError(errorMessage)

    def offline(self) -> None:
        '''
        服务下线
        '''
        url = f'{self.centerBaseUri}/offline/{self.serviceName}/{self.servicePort}'
        try:
            self.httpClient.delete(url)
        except Exception as err:
            self.logger.warning(f'Service offline failed: {err}')

    async def ping(self):
        '''
        服务内置路由, 用于响应服务中心的ping测试
        '''
        return {'code': 0, 'message': 'ok'}

    def start(self, debug: bool = True):
        '''
        启动服务

        Args:
            host: 服务监听地址
            port: 监听端口
            debug: 是否处于Debug模式
        '''
        try:
            import uvicorn
        except Exception as err:
            errorMessage = 'uvicorn is not installed, the service will not start, you may need to use "python3 -m pip install uvicorn[standard]" to install it'
            self.logger.critical(errorMessage)
            raise ServiceStartError(errorMessage)
        
        # 存储进程服务PID
        self.pid = getpid()

        # 向服务中心提交上线请求
        self.online()

        # 覆盖uvicorn默认日志配置, 转用log模块提供的日志处理程序
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
        uvicorn.run(
            self, 
            host=self.serviceHost, 
            port=self.servicePort, 
            debug=debug, 
            log_config=logConfig
        )

