import os.path
from logging import Logger

from httpx import Client, Request, Response

from mfhm.log import Logger, getLogger
from mfhm.errors import (
    ServiceCenterCommunicationError,
    ParameterError,
    ServiceCallError
)


class SingleServiceProxyMeghod(object):
    '''
    单个服务代理的HTTP方法调用对象
    '''

    def __init__(
            self, 
            url:str,
            methods:list,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:Client = Client(timeout=5)
    ) -> None:
        '''
        Args:
            url: 目标接口地址
            methods: 目标接口支持的HTTP方法
            logger: 日志对象
            httpClient: httpx客户端
        '''
        self.__url = url
        self.__methods = [method.upper() for method in methods]
        self.__logger = logger
        self.__httpClient = httpClient

    @staticmethod
    def __havePathParameter(url:str) -> bool:
        '''
        判断URL中是否存在路径参数

        Args:
            url: 待判断URL
        '''
        start = False
        for u in url:
            if u == '{':
                start = True
            if u == '}' and start:
                return True

        return False

    def __request(self, method:str, *args, **kwargs) -> Response:
        '''
        请求目标服务
        '''
        # 如果URL中存在路径参数, 需要从 pathparams 参数中
        # 取值替换, 拼接为实际请求URL
        if self.__havePathParameter(self.__url):
            if not 'pathparams' in kwargs:
                errorMessage = f'There are path parameters in the URL, please use "pathparams" to specify: {self.__url}'
                raise ParameterError(errorMessage)
            if not isinstance(kwargs['pathparams'], dict):
                raise ParameterError(f'"pathparams" parameter value should be a {dict}')
            self.__url = self.__url.format(**kwargs['pathparams'])
            # pathparams参数是框架的自定义参数, 用于FastAPI路由中的路径参数填充
            # 但在httpx中是不存在的参数, 正式发送请求前需要将其移除
            del kwargs['pathparams']

        # 如果调用了目标接口不支持的HTTP方法类型, 抛出错误
        method = method.upper()
        if not method in self.__methods:
            errorMessage = f'The target API supports {self.__methods}, but uses "{method}"'
            raise ServiceCallError(errorMessage)

        # 向目标发送请求并获取响应
        request = Request(method=method, url=self.__url, *args, **kwargs)
        try:
            return self.__httpClient.send(request=request)
        except Exception as err:
            raise ServiceCallError(err)
        
    def __getattr__(self, __method:str):
        '''
        '''
        return lambda *args, **kwargs : self.__request(__method, *args, **kwargs)


class SingleServiceProxy(object):
    '''
    单个服务代理
    '''
    def __init__(
            self, 
            serviceName:str,
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:Client = Client(timeout=5)
    ) -> None:
        '''
        Args:
            serviceName: 目标服务名称
            centerProtocol: 服务中心协议类型
            centerHost: 服务中心主机地址
            centerPort: 服务中心端口
            logger: 日志对象
            httpClient: httpx客户端
        '''
        self.__serviceName = serviceName
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__centerBaseUri = f'{self.__centerProtocol}://{self.__centerHost}:{self.__centerPort}'
        self.__logger = logger
        self.__httpClient = httpClient

    def __getattr__(self, __apiName: str) -> SingleServiceProxyMeghod:
        '''
        向服务中心查询目标服务接口信息并实例化HTTP方法调用实例
        '''
        url = f'{self.__centerBaseUri}/api/{self.__serviceName}/{__apiName}'
        try:
            response = self.__httpClient.get(url)
            responseData = response.json()
        except Exception as err:
            errorMessage = f'Unable to communicate with service center: {err}'
            self.__logger.error(errorMessage)
            raise ServiceCenterCommunicationError(errorMessage)

        if not response.status_code == 200:
            errorMessage = f'Unable to communicate with service center:\n'
            errorMessage += f'    HTTP code: {response.status_code}\n'
            errorMessage += f'    Data: {response.text}'
            self.__logger.error(errorMessage)
            raise ServiceCenterCommunicationError(errorMessage)

        # 接口调用实例
        return SingleServiceProxyMeghod(
            url=responseData['apiUrl'],
            methods=responseData['apiMethods'],
            logger=self.__logger,
            httpClient=self.__httpClient
        )


class ServiceProxy(object):
    '''
    服务代理
    '''
    def __init__(
            self, 
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient: Client = Client(timeout=5)
    ) -> None:
        '''
        Args:
            centerProtocol: 服务中心协议类型
            centerHost: 服务中心主机地址
            centerPort: 服务中心端口
            logger: 日志对象
            httpClient: httpx客户端
        '''
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__logger = logger
        self.__httpClient = httpClient
        self.__cache = {}
            
    def __getattr__(self, __serviceName: str) -> SingleServiceProxy:
        '''
        属性名称作为服务名称, 实例化单个服务代理

        Args:
            __serviceName: 目标服务名称
        '''
        if not __serviceName in self.__cache:
            self.__cache[__serviceName] = SingleServiceProxy(
                serviceName=__serviceName,
                centerProtocol=self.__centerProtocol,
                centerHost=self.__centerHost,
                centerPort=self.__centerPort,
                logger=self.__logger,
                httpClient=self.__httpClient
            )

        return self.__cache[__serviceName]