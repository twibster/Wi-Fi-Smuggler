import subprocess, qrcode

def get_password(result):
    password = result.split(":")[1:]
    if len(password)>1: 
        password[0] = password[0][1:]
        password[-1] = password[-1][:-1]
        return ":".join(password)
    else:
        return password[0][1:-1]

def get_connected_ssid():
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
    result = result.decode('utf-8')  # Convert bytes to string

    # Search for the SSID name
    ssid = None
    for line in result.split('\n'):
        if 'SSID' in line:
            return line.split(':')[-1][1:-1]
    return ssid

def get_saved_networks():
        WIFIs= {}
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

        with open("Saved-WIFI.txt",'w') as SSIDs:
            for i in profiles:
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
                    for result in results:
                        if "Authentication" in result:
                            authentication = result.split(":")[1][1:-1]
                            if authentication == "Open":
                                password = ""
                                break
                        elif "Key Content" in result:
                            password = get_password(result)
                            break
                    SSIDs.write(i + ":" + password + ":" + authentication + "\n")
                    WIFIs[i] = [password, authentication]
                except Exception as e:
                    with open("Errors.txt","a") as errors:
                        errors.write(str(e)+"\n"+"\n")
                    continue
        return WIFIs
    
def main():
    map_auth={
        "WPA2-Personal":"WPA",
        "WPA-Personal":"WPA"
    }
    
    WIFIs= get_saved_networks()
    SSID = get_connected_ssid()
    if SSID:
        qr = qrcode.make(f"WIFI:S:{SSID};T:{WIFIs[SSID][0]};P:{map_auth[WIFIs[SSID][1]]};;")
        qr.save(f"{SSID}.png")
        qr.show()
    return

main()


