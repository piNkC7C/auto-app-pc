class TestTaskRunner:
    def __init__(self):
        self.test_task = [
            # {
            #     "_id": "660d038ca45d0000e1003c42",
            #     "type": 0,
            #     "saleId": "",
            #     "instructionNo": 31,
            #     "instructionName": "验证工作台激活状态",
            #     "action": "verify",
            #     "actObjType": "image",
            #     "image": {
            #         "picName": "workstand_act",
            #         "picConfidence": 0.8,
            #         "picLeft": 0.5,
            #         "picTop": 0.5
            #     },
            #     "skipTimes": 1,
            #     "waitTime": 0,
            #     "circleCount": 0,
            #     "circleWaitTime": 0,
            #     "moveClickWaitTime": 0
            # },
            {
                "_id": "660d03a9a45d0000e1003c43",
                "type": 0,
                "saleId": "",
                "instructionNo": 32,
                "instructionName": "点击工作台图标",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "workstand",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "660d03efa45d0000e1003c44",
                "type": 0,
                "saleId": "",
                "instructionNo": 33,
                "instructionName": "验证工作台的小飞助理打开状态",
                "action": "verify",
                "actObjType": "image",
                "image": {
                    "picName": "enter_contact",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 1,
                "waitTime": 0,
                "circleCount": 20,
                "circleWaitTime": 100,
                "moveClickWaitTime": 0
            },
            {
                "_id": "660d0430a45d0000e1003c45",
                "type": 0,
                "saleId": "",
                "instructionNo": 34,
                "instructionName": "点击工作台小飞助理",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "workstand_xiaofei",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 2000,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "660d049fa45d0000e1003c46",
                "type": 0,
                "saleId": "",
                "instructionNo": 35,
                "instructionName": "点击客户id输入框",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "panda",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 100,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "65fbf7f2b494be2f74c49305",
                "type": 0,
                "saleId": "",
                "instructionNo": 8,
                "instructionName": "粘贴文字",
                "action": "paste",
                "actObjType": "text",
                "text": {
                    "content": "wmu-p0CwAAMF9gDChOhuPIY-9qqSWTMw"
                },
                "skipTimes": 0,
                "waitTime": 200,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 0
            },
            {
                "_id": "660d04e0a45d0000e1003c47",
                "type": 0,
                "saleId": "",
                "instructionNo": 36,
                "instructionName": "点击进入会话",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "enter_contact",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "65fd57cfb494be2f74c4930b",
                "type": 0,
                "saleId": "",
                "instructionNo": 13,
                "instructionName": "验证工具栏状态",
                "action": "verify",
                "actObjType": "image",
                "image": {
                    "picName": "zidingyi",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 1,
                "waitTime": 0,
                "circleCount": 20,
                "circleWaitTime": 100,
                "moveClickWaitTime": 0
            },
            {
                "_id": "65fbf802b494be2f74c49307",
                "type": 0,
                "saleId": "",
                "instructionNo": 10,
                "instructionName": "点击工具栏",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "help",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 1000,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            # {
            #     "_id": "66069afdbb5820268bfdc655",
            #     "type": 0,
            #     "saleId": "",
            #     "instructionNo": 26,
            #     "instructionName": "验证小飞助理激活状态",
            #     "action": "verify",
            #     "actObjType": "image",
            #     "image": {
            #         "picName": "xiaofei_act",
            #         "picConfidence": 1,
            #         "picLeft": 0.5,
            #         "picTop": 0.5
            #     },
            #     "skipTimes": 1,
            #     "waitTime": 0,
            #     "circleCount": 20,
            #     "circleWaitTime": 100,
            #     "moveClickWaitTime": 0
            # },
            {
                "_id": "65fd580db494be2f74c4930c",
                "type": 0,
                "saleId": "",
                "instructionNo": 14,
                "instructionName": "点击小飞助理",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "xiaofei",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "66069b0abb5820268bfdc656",
                "type": 0,
                "saleId": "",
                "instructionNo": 27,
                "instructionName": "验证tab咨询激活状态",
                "action": "verify",
                "actObjType": "image",
                "image": {
                    "picName": "zixun_act",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 1,
                "waitTime": 0,
                "circleCount": 20,
                "circleWaitTime": 100,
                "moveClickWaitTime": 0
            },
            {
                "_id": "65fbf806b494be2f74c49308",
                "type": 0,
                "saleId": "",
                "instructionNo": 11,
                "instructionName": "点击tab_咨询",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "zixun",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "65fd59c5b494be2f74c49310",
                "type": 0,
                "saleId": "",
                "instructionNo": 7,
                "instructionName": "点击公司信息",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "company",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 5000,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "65fbf7f8b494be2f74c49306",
                "type": 0,
                "saleId": "",
                "instructionNo": 9,
                "instructionName": "点击发送",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "sendmsg",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "660d03a9a45d0000e1003c43",
                "type": 0,
                "saleId": "",
                "instructionNo": 32,
                "instructionName": "点击工作台图标",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "workstand",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
            {
                "_id": "660d03efa45d0000e1003c44",
                "type": 0,
                "saleId": "",
                "instructionNo": 33,
                "instructionName": "验证工作台的小飞助理打开状态",
                "action": "verify",
                "actObjType": "image",
                "image": {
                    "picName": "enter_contact",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 1,
                "waitTime": 0,
                "circleCount": 20,
                "circleWaitTime": 100,
                "moveClickWaitTime": 0
            },
            {
                "_id": "660d0430a45d0000e1003c45",
                "type": 0,
                "saleId": "",
                "instructionNo": 34,
                "instructionName": "点击工作台小飞助理",
                "action": "move_click",
                "actObjType": "image",
                "image": {
                    "picName": "workstand_xiaofei",
                    "picConfidence": 0.8,
                    "picLeft": 0.5,
                    "picTop": 0.5
                },
                "skipTimes": 0,
                "waitTime": 0,
                "circleCount": 0,
                "circleWaitTime": 0,
                "moveClickWaitTime": 100
            },
        ]
        self.quick_task = {
            "code": 200,
            "data": {
                "keyList": ["'\\x04'", "Key.ctrl_l+Key.enter", "Key.ctrl_r+Key.enter"],
                "keyReleaseList": ["Key.ctrl_l+Key.ctrl_l", "Key.ctrl_r+Key.ctrl_r"],
                "instructionList": {
                    "'\\x04'": [
                        {
                            "_id": "661cc0846e670000d50032c2",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 37,
                            "instructionName": "验证客户档案输入框是否存在",
                            "action": "verify",
                            "actObjType": "image",
                            "image": {
                                "picName": "cusinfo_input",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 1,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "660bcfb3a45d0000e1003c41",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 30,
                            "instructionName": "跳过后续y步（y=skipTimes）",
                            "action": "skip",
                            "actObjType": "task",
                            "skipTimes": 3,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "661cc0b46e670000d50032c3",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 38,
                            "instructionName": "点击客户档案输入框",
                            "action": "move_click",
                            "actObjType": "image",
                            "image": {
                                "picName": "cusinfo_input",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 10
                        }
                    ],
                    "Key.ctrl_r+Key.enter": [
                        {
                            "_id": "65fbf7f8b494be2f74c49306",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 9,
                            "instructionName": "点击发送",
                            "action": "move_click",
                            "actObjType": "image",
                            "image": {
                                "picName": "sendmsg",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 100
                        }
                    ],
                    "Key.ctrl_l+Key.ctrl_l": [
                        {
                            "_id": "66262af045370000c6000577",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 43,
                            "instructionName": "验证客户档案输入框激活状态",
                            "action": "verify",
                            "actObjType": "image",
                            "image": {
                                "picName": "cusinfo_input_act",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 2,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "661cc0846e670000d50032c2",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 37,
                            "instructionName": "验证客户档案输入框是否存在",
                            "action": "verify",
                            "actObjType": "image",
                            "image": {
                                "picName": "cusinfo_input",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 1,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "6600e6e317672e631d388f03",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 25,
                            "instructionName": "跳过后续所有步骤",
                            "action": "skip",
                            "actObjType": "all",
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "66262a7645370000c6000576",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 42,
                            "instructionName": "验证聊天框",
                            "action": "verify",
                            "actObjType": "image",
                            "image": {
                                "picName": "chatroom",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 3,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "6626285845370000c6000573",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 39,
                            "instructionName": "点击发送按钮的上方",
                            "action": "move_click",
                            "actObjType": "image",
                            "image": {
                                "picName": "sendmsg",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": -1.5
                            },
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 100
                        },
                        {
                            "_id": "6626286245370000c6000574",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 40,
                            "instructionName": "全选组合键",
                            "action": "press",
                            "actObjType": "hotkey",
                            "hotkey": [
                                "Ctrl",
                                "a"
                            ],
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "6626286f45370000c6000575",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 41,
                            "instructionName": "向右单键",
                            "action": "press",
                            "actObjType": "key",
                            "key": {
                                "keyName": "right"
                            },
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 0
                        },
                        {
                            "_id": "65fbf80ab494be2f74c49309",
                            "type": 0,
                            "saleId": "",
                            "instructionNo": 12,
                            "instructionName": "点击聊天框",
                            "action": "move_click",
                            "actObjType": "image",
                            "image": {
                                "picName": "chatroom",
                                "picConfidence": 0.8,
                                "picLeft": 0.5,
                                "picTop": 0.5
                            },
                            "skipTimes": 0,
                            "waitTime": 0,
                            "circleCount": 0,
                            "circleWaitTime": 0,
                            "moveClickWaitTime": 100
                        }
                    ]
                }
            }
        }
