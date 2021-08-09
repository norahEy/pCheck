import requests
import threading
from multiprocessing import Queue

#marketing idk looks cool ig
head_tag = """
           _   ___     _   
 ___   ___| |_|_  |___| |_ 
| . |_|  _|   |_  |  _| '_|
|  _|_|___|_|_|___|___|_,_|http
|_| 
Proxy-count: 1588 | Version: 1.1 
"""
print(head_tag)


active_proxies = []
active_threads = []

def ProxyCheck(proxy_to_check):
    try:
        r = requests.get("http://api.ipify.org", proxies={"http": proxy_to_check, "https": proxy_to_check}, timeout=50)        
        #print("{} is online {}".format(proxy_to_check, str(r.elapsed)))
        return (proxy_to_check, r.elapsed)
    except:        
        return False

def SetupThreads(Thread_Count=1000):
    for i in range(Thread_Count):
        thread = threading.Thread(target=ProxyWorker)
        active_threads.append(thread)

def StartThreads():
    for thread in active_threads:
        thread.start()

def AwaitActiveThreads():
    for thread in active_threads:
        thread.join()

def ProxyWorker():
    while not proxy_queue.empty():
        Proxy = proxy_queue.get()
        proxy_response = ProxyCheck(Proxy)
        if not proxy_response:
            return
        else:                
            active_proxies.append(proxy_response)
    
def GetProxysToList():
    final_proxy_list = []
    with open("proxy_list.txt", "r") as file:
        proxy_list = file.readlines()
        for proxy in proxy_list:
            final_proxy_list.append(proxy[0:-1])
    return final_proxy_list

def GetProxysToQueue():
    Proxy_List_Queue = Queue()
    Proxy_List = GetProxysToList()
    for line in Proxy_List:
        Proxy_List_Queue.put(line)
    return Proxy_List_Queue

#execute
proxy_queue = GetProxysToQueue()
SetupThreads()
print("Checking Proxys...")
print("This may take a while.")
StartThreads()
AwaitActiveThreads()
print("Done!")
#result
print("{} of 1588 proxys are active.\n".format(str(len(active_proxies))))
print("|Ipv4        |Port |Latency")
for entry in active_proxies:
    print(str(entry))