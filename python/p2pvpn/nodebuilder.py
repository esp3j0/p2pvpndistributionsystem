import os
import uuid
import shutil
import ipaddress
class nodes_builder():
    totleNodes = 0
    confDir = ""
    uuid = ""
    network = ""
    netmask = ""
    pwd = ""
    def __init__(self,num,network="10.7.0.0/24"):
        self.totleNodes = num
        self.pwd = os.popen("pwd").readline()[:-1]
        n = network.split('/')
        nw = n[0].split('.')
        zeros = int(int(n[1])/8)
        for i in range(zeros,4):
            nw[i] = '0'
        s = nw[0]+'.'+nw[1]+'.'+nw[2]+'.'+nw[3]
        s = s+'/'+n[1]
        self.network = ipaddress.IPv4Network(s)
    def BuildUuid6(self):
        self.uuid = uuid.uuid4().hex[:6]
    def BuildConfigDir(self):
        os.chdir(self.pwd)
        if not os.path.exists('./configs'):
            os.mkdir('./configs')
        self.confDir = './configs/config-'+self.uuid+'/'
        if not os.path.exists(self.confDir):
            os.mkdir(self.confDir)
            for i in range(1,self.totleNodes+1):
                os.mkdir(self.confDir+str(i))
                os.mkdir(self.confDir+str(i)+'/'+'security')
                os.mkdir(self.confDir+str(i)+'/'+'ed25519')
            return True
        else:
            return False
    def BuildSecurity(self):
        for i in range(1,self.totleNodes+1):
            pathToPrivateKey = self.confDir + str(i) + "/security/" + str(i)+ ".private"
            pathToPublicKey = self.confDir + str(i) + "/security/" + str(i)+ ".public"
            os.system("./gnb_crypto -c -p "+pathToPrivateKey+" -k "+pathToPublicKey)
    def BuildEd25519(self):
        for i in range(1,self.totleNodes+1):
            pathToPublicKey = self.confDir + str(i) + "/security/" + str(i)+ ".public"
            for i in range(1,self.totleNodes+1):
                pathToEd25519 = self.confDir + str(i) + "/ed25519"
                os.system("cp "+pathToPublicKey+" "+pathToEd25519)
    def BuildAddressConf(self):
        for i in range(1,self.totleNodes+1):
            pathToNode = self.confDir + str(i)
            os.system("cp ./defaultConf/address.conf "+ pathToNode)
    def BuildNodeConf(self):
        for i in range(1,self.totleNodes+1):
            pathToNode = self.confDir + str(i)
            os.system("cp ./defaultConf/node.conf "+ pathToNode)
            os.system("sed -i 's/\$nodeid/"+str(i)+"/g' "+pathToNode+"/node.conf")
    def BuildRouteConf(self):
        route = ""
        for i in range(1,self.totleNodes+1):
            route+=str(i)+'|'+(self.network.network_address+i).exploded+'|'+self.netmask+'\n'
        print(route)
        for i in range(1,self.totleNodes+1):
            with open(self.confDir+str(i)+'/route.conf','w') as f:
                f.write(route)
                f.close()
    def BuildBinary(self):
        for i in range(1,self.totleNodes+1):
            os.system("cp -r ./bin/ "+self.confDir+str(i))
        
    def test(self):
        if not self.network.is_private:
            return "提供的网络非私网保留地址，请从10.0.0.0~10.255.255.255或172.16.0.0~172.131.255.255或192.168.0.0!192.168.255.255选取网络"
        if not(self.network.netmask.exploded == '255.255.255.0' or
            self.network.netmask.exploded == '255.255.0.0' or
            self.network.netmask.exploded == '255.0.0.0'):
            return "目前仅支持可选的掩码"
        if self.totleNodes > self.network.num_addresses-2:
            return "节点数量大于网络承载量"
        self.netmask = self.network.netmask.exploded
        return "ok"
    
    def BuildAll(self):
        ok = self.test()
        if  ok == "ok":
            self.BuildUuid6()
            self.BuildConfigDir()
            self.BuildSecurity()
            self.BuildEd25519()
            self.BuildAddressConf()
            self.BuildNodeConf()
            self.BuildRouteConf()
            self.BuildBinary()
            ok = self.uuid
            return "您的网络uuid为:"+ ok + "请到下载页面下载相应节点客户端"
        return ok