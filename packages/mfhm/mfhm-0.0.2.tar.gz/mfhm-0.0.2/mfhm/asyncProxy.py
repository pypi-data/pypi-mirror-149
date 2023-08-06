import os.path
from logging import Logger

from httpx import AsyncClient, Request

from mfhm.log import getLogger
from mfhm.errors import (
    ServiceCenterCommunicationError,
    ParameterError,
    ServiceCallError
)


class AsyncSingleServiceProxyMeghodRequest(object):
    '''
    方法请求对象
    '''
    # 服务接口信息缓存
    # {
    #   serviceName: {
    #       apiName: {'url': apiUrl, methods: []}
    #   }
    # }
    __cache = {}

    def __init__(
            self, 
            serviceName: str,
            apiName: str,
            method: str,  
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:AsyncClient = AsyncClient(timeout=5), 
            **kwargs,
    ) -> None:
        '''
        Args:
        '''
        self.__serviceName = serviceName
        self.__apiName = apiName
        self.__method = method.upper()
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__centerBaseUri = f'{self.__centerProtocol}://{self.__centerHost}:{self.__centerPort}'
        self.__logger = logger
        self.__httpClient = httpClient
        # self.__args = args
        self.__kwargs = kwargs
    
    @classmethod
    def __havePathParameter(cls, url:str) -> bool:
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
    
    async def __request(self):
        apiUrl = None
        apiMethods = None

        # 如果缓存中已存在接口信息, 使用缓存中的的接口信息
        if self.__serviceName in self.__class__.__cache:
            if self.__apiName in self.__class__.__cache[self.__serviceName]:
                apiUrl = self.__class__.__cache[self.__serviceName][self.__apiName]['url']
                apiMethods = self.__class__.__cache[self.__serviceName][self.__apiName]['methods']

        # 如果本地缓存没有目标服务接口信息, 向服务中心查询并存入本地缓存
        if not apiUrl or not apiMethods:
            url = f'{self.__centerBaseUri}/api/{self.__serviceName}/{self.__apiName}'
            try:
                response = await self.__httpClient.get(url)
                responseData = response.json()
                apiUrl = responseData['apiUrl']
                apiMethods = [method.upper() for method in responseData['apiMethods']]
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

            # 将接口信息存入缓存
            if not self.__serviceName in self.__class__.__cache:
                self.__class__.__cache[self.__serviceName] = {}
            if not self.__apiName in self.__class__.__cache[self.__serviceName]:
                self.__class__.__cache[self.__serviceName] = {}
            self.__class__.__cache[self.__serviceName][self.__apiName] = {
                'url': apiUrl,
                'methods': apiMethods
            }

        # 调用目标服务接口并获取响应
        # 如果URL中存在路径参数, 需要从 self.__kwargs['pathparams'] 参数中
        # 取值替换, 拼接为实际请求URL
        if self.__class__.__havePathParameter(apiUrl):
            if not 'pathparams' in self.__kwargs:
                errorMessage = f'There are path parameters in the URL, please use "pathparams" to specify: {apiUrl}'
                raise ParameterError(errorMessage)
            if not isinstance(self.__kwargs['pathparams'], dict):
                raise ParameterError(f'"pathparams" parameter value should be a {dict}')
            apiUrl = apiUrl.format(**self.__kwargs['pathparams'])
            # pathparams参数是框架的自定义参数, 用于FastAPI路由中的路径参数填充
            # 但在httpx中是不存在的参数, 传递给httpx发送请求前需要将其移除
            del self.__kwargs['pathparams']

        if not self.__method in apiMethods:
            errorMessage = f'The target API supports {apiMethods}, but uses "{self.__method}"'
            raise ServiceCallError(errorMessage)
        
        request = Request(method=self.__method, url=apiUrl, **self.__kwargs)
        try:
            return await self.__httpClient.send(request=request)
        except Exception as err:
            raise ServiceCallError(err)

    def __await__(self):
        return self.__request().__await__()


class AsyncSingleServiceProxyMeghod(object):

    def __init__(
            self, 
            serviceName: str,
            apiName:str,
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:AsyncClient = AsyncClient(timeout=5), 
    ) -> None:
        '''
        Args:
        '''
        self.__serviceName = serviceName
        self.__apiNeme = apiName
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__logger = logger
        self.__httpClient = httpClient

    def __getattr__(self, method:str):
        return lambda **kwargs : AsyncSingleServiceProxyMeghodRequest(
            serviceName=self.__serviceName,
            apiName=self.__apiNeme,
            method=method,
            centerProtocol=self.__centerProtocol,
            centerHost=self.__centerHost,
            centerPort=self.__centerPort,
            logger=self.__logger,
            httpClient=self.__httpClient,
            **kwargs
        )


class AsyncSingleServiceProxy(object):

    def __init__(
            self, 
            serviceName: str,
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:AsyncClient = AsyncClient(timeout=5), 
    ) -> None:
        '''
        Args:
        '''
        self.__serviceName = serviceName
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__logger = logger
        self.__httpClient = httpClient

    def __getattr__(self, apiName:str):
        return AsyncSingleServiceProxyMeghod(
            serviceName=self.__serviceName,
            apiName=apiName,
            centerProtocol=self.__centerProtocol,
            centerHost=self.__centerHost,
            centerPort=self.__centerPort,
            logger=self.__logger,
            httpClient=self.__httpClient
        )


class AsyncServiceProxy(object):

    def __init__(
            self, 
            centerProtocol:str = 'http',
            centerHost:str = '127.0.0.1',
            centerPort:int = 21428,
            logger:Logger = getLogger(os.path.basename(os.path.abspath(__file__))),
            httpClient:AsyncClient = AsyncClient(timeout=5), 
    ) -> None:
        '''
        Args:
        '''
        self.__centerProtocol = centerProtocol
        self.__centerHost = centerHost
        self.__centerPort = centerPort
        self.__logger = logger
        self.__httpClient = httpClient

    def __getattr__(self, serviceName:str):
        return AsyncSingleServiceProxy(
            serviceName=serviceName,
            centerProtocol=self.__centerProtocol,
            centerHost=self.__centerHost,
            centerPort=self.__centerPort,
            logger=self.__logger,
            httpClient=self.__httpClient
        )
