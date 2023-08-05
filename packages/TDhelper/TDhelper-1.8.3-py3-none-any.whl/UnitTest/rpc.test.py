import __init__
import unittest
import json
from TDhelper.network.http.RPC import RPC

class TestRPC(unittest.TestCase):
    def test_RPC_Register(self):
        pass

    def test_RPC_Call(self):
        m_rpc = RPC("http://127.0.0.1:8000/api/", "349304398403804983048034")
        '''
        print(m_rpc.register(
            service={"name": "test", "description": "测试添加服务",
                    "key": "gg", "httpProtocol": "http://"},
            hosts=[{"host": "127.0.0.1", "port": 8002}, {
                "host": "192.168.0.100", "port": 8000}],
            methods=[{"key": "test_method", "uri": "api/uri/", "method": "POST", "version": "1.0.0", "description": "测试添加方法", "params": [{"key": "test_method_p1", "description": "P1参数", "defaultValue": "0"}]}]))
        #print(m_rpc.call("remote_config","remote_config_register", **{"name":"测试远程配置服务注册","serivce_key":"test_rpc_register"}))
        '''
        serviceConfig = {
            "services": [
                {
                    # 服务配置
                    "service": {
                        "name": "TEST",
                        "description": "TEST",
                        "key": "TEST",
                        "accessSecret": "slkjflkjdfejfoejfoefef",
                        "httpProtocol": "http://"
                    },
                    # 服务器配置
                    "hosts": [
                        {
                            "host": "127.0.0.1",
                            "port": 8004
                        }
                    ],
                    # 方法配置
                    "methods": [
                        # 帐号相关 begin
                        {
                            "key": "TEST" + "_ACCOUNTS_LIST",
                            "uri": "api/accounts/",
                            "method": "GET",
                            "version": "1.0.0",
                            "description": "获取帐号列表",
                            "params": [
                                {
                                    "key": "page",
                                    "descript": "页码",
                                    "defaultValue": "1"
                                }
                            ],
                            "returns": {
                                "valueType": "json",
                                "examples": json.dumps({"state": 200, "msg": {"count": 0, "next": None, "previous": None, "results": []}}),
                                "descriptions":[
                                    {
                                        "key": "state",
                                        "valueDescription": "200:success,\r\n-1:failed."
                                    },
                                    {
                                        "key": "msg",
                                        "valueDescription": "success returns json({count:<int>(total records count),next:<string>(next page url),previous:<string>(previous page url),results:[json(<account>)]}),\r\nfailed returns error msg(<string>)."
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
        '''
        count=0
        for item in serviceConfig["services"]:
            print(m_rpc.register(
                service=item['service'],
                hosts=item['hosts'],
                methods=item['methods']))
        '''
        g = m_rpc.handle("GENERAL_SERVICE")
        ret = g.call(
            "GENERAL_SERVICE_VALIDATE_CODE_VALIDATE",
            **{
                "validateType": 1,
                "triggerEvent": "手机验证码登录",
                "receive": '8615013782894',
                "code": '22222'
            })
        print(ret)
        #m_id= ret['data']['id']
        # ret=g.call('REMOTE_CONFIG_CONFIG_REGISTER',**{"config_key":"test1","config_value":"testvalue","service":m_id})
        # print(ret)

if __name__ == "__main__":
    unittest.main()