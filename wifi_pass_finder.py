import subprocess
import re
import os
netsh_output = subprocess.run(['netsh','wlan','show','profiles'],capture_output=True).stdout.decode()
profile_names = re.findall("All User Profile     : (.*)\r",netsh_output)
wifi_list = []
if len(profile_names) != 0:
    for name in profile_names:
        
        wifi_profile = {}

        profile_info = subprocess.run(['netsh','wlan','show','profile',name],capture_output=True).stdout.decode()
        if re.search('Security key           : Absent', profile_info):
            continue
        else:
            wifi_profile['SSID'] = name
            profile_info_pass = subprocess.run(['netsh','wlan','show','profile',name,'key=clear'],capture_output=True).stdout.decode()
            password = re.search('Key Content            : (.*)\r', profile_info_pass)
            if password == None:
                wifi_profile['PASSWORD'] = None
            else:
                wifi_profile['PASSWORD'] = password[1]
            wifi_list.append(wifi_profile)
print(f'{"SSID":^25}|{"PASSWORD":^25}')
for wifi in wifi_list:
    print(f'{wifi["SSID"]:^25}|{wifi["PASSWORD"]:^25}')
while True:
    try:
        save = input('Do you wanna save it into a file: ')
        save.lower()
        if save not in ['y','yes','n','no']:
            raise ValueError()
        else:
            break
    except(ValueError):
        print('Please only answer with yes or no!')
if save in ['y','yes']:
    with open('wifi_list.txt','w') as file:
        file.write(f'{"SSID":^26}|{"PASSWORD":^25}')
        file.write('\n')
        for wifi in wifi_list:
            file.write(f'{wifi["SSID"]:^25}|{wifi["PASSWORD"]:^25}')
            file.write('\n')
else:
    exit()