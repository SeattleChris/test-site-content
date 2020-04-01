#! /usr/bin/env python
import subprocess
import requests
import os
# from pprint import pprint

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_driver_url = 'https://chromedriver.storage.googleapis.com'
chrome_dl_url = 'https://dl.google.com/linux/direct'
chrome_deb_name = 'google-chrome-stable_current_amd64.deb'
chromedriver_filename = BASE_DIR + '/chromedriver'
env_filename = BASE_DIR + '/chrome.env'
lookup_package = {'pip3': 'python3-pip', }


def get_chrome_info(browser):
    try:
        output = subprocess.check_output(f"{browser} --version", stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print("Google Chrome needs to be installed. ")
        subprocess.check_output(f"wget {chrome_dl_url}/{chrome_deb_name}")
        # subprocess.check_output(f"apt install ./{chrome_deb_name}")
    output = subprocess.check_output(f"{browser} --version", stderr=subprocess.STDOUT, shell=True)
    version = output.rsplit(None, 1)[-1].rsplit(b'.', 1)[0].decode()
    try:
        chrome_location = subprocess.check_output(f"which {browser}", shell=True).decode()
    except Exception as e:
        print("Which had an error. ")
        print(e)
        chrome_location = None
    return (chrome_location, version)


def get_chromedriver(version):
    url = f"{base_driver_url}/LATEST_RELEASE_{version}"
    res = requests.get(url)
    if not res.status_code == 200:
        print(f"Google Chrome version {version}. Unable to find chromedriver with site: ")
        print(url)
        return None
    ver = res.text
    try:
        output = subprocess.check_output("chromedriver --version", stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print("The chromedriver needs to be installed. ")
        output = ''
    local_ver = output.split()[1].decode()
    driver_location = None
    if ver == local_ver:
        print("The correct chromedriver is already installed. ")
        driver_location = subprocess.check_output("which chromedriver", shell=True).decode()
    elif local_ver:
        print("The wrong version of chromedriver is installed. ")
        driver_location = subprocess.check_output("which chromedriver", shell=True).decode()
        output = subprocess.run(f"rm {driver_location}", shell=True)
        driver_location = None
    if not driver_location:
        print("We need to install chromedriver. ")
        url = f"{base_driver_url}/{ver}/chromedriver_linux64.zip"
        res = requests.get(url)
        if not res.status_code == 200:
            print(f"Chromedriver version {ver}. Unable to download. Visit url: ")
            print(f"{base_driver_url}/index.html?path={ver}/")
            return None
        with open(chromedriver_filename, 'wb') as f:
            f.write(res.content)
    elif driver_location != chromedriver_filename:
        print("Driver is in the wrong location. ")
        subprocess.run(f"cp {driver_location} {chromedriver_filename}", shell=True)
    subprocess.run(f"chmod 755 {chromedriver_filename}", shell=True)
    return chromedriver_filename


def save_file_info(chrome, version, driver):
    with open(env_filename, 'w') as f:
        f.write(f"CHROME_VERSION={version}\n")
        f.write(f"CHROME_LOCATION={chrome}")
        f.write(f"CHROMEDRIVER_LOCATION={driver}")
        f.write('\n')
    return env_filename


def get_or_install_program(program, install):
    output = subprocess.run(f"which {program}", shell=True)
    if output.returncode and install:
        print(f"Installing {program}. ")
        package = lookup_package.get(program, program)
        subprocess.run(f"sudo apt install {package}")
        output = subprocess.run(f"which {program}", shell=True)
    location = None if output.returncode else output.stdout
    return location


if __name__ == '__main__':
    # update = subprocess.run("sudo apt update", shell=True)
    pip_info = get_or_install_program('pip3', True)
    chrome, version = get_chrome_info('google-chrome')
    chromedriver = get_chromedriver(version)
    saved_file = save_file_info(chrome, version, chromedriver)
    print(saved_file)
    # pip3 install -r requirements.txt 
    print('Setup chrome done. ')
