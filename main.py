#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# GitHub: https://github.com/esmailiyan/v2ray_config_generator.git

"""Get random configs from multiple sources."""
import subprocess
from subprocess import run
#checking For Requirements
libs = run('pip freeze'.split(' '),stdout=subprocess.PIPE,text=True).stdout
if ('requests==' not in libs) or ('rich==' not in libs):
    print("INSTALLING REQUIREMENTS, PLEASE WAIT...")
    run("pip install rich".split(' '),stdout=subprocess.DEVNULL)
    run("pip install requests".split(' '),stdout=subprocess.DEVNULL)

import base64
import datetime
import os
import random
import sys

import requests
from rich import print as rprint
from rich.progress import track

# URLs for configs not encoded in a base64 string
DECODED_URLS = [
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/awesome-vpn/awesome-vpn/master/all",
]

# URLs for configs encoded in a base64 string
ENCODED_URLS = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/AzadNetCH/Clash/main/V2Ray.txt",
    "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
    "https://raw.fastgit.org/ripaojiedian/freenode/main/sub",
    "https://github.xiaoku666.tk/https://raw.githubusercontent.com/ripaojiedian/freenode/main/sub",
    "https://raw.githubusercontent.com/learnhard-cn/free_proxy_ss/main/v2ray/v2raysub",
]
COLORS = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
NOW = datetime.datetime.now()
QR_DIR = "./qr_codes"
LOGO="""
██████╗░███████╗░█████╗░░█████╗░██████╗░███████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
██║░░██║█████╗░░██║░░╚═╝██║░░██║██║░░██║█████╗░░
██║░░██║██╔══╝░░██║░░██╗██║░░██║██║░░██║██╔══╝░░
██████╔╝███████╗╚█████╔╝╚█████╔╝██████╔╝███████╗
╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═════╝░╚══════╝"""

def get_config(url):
    """Get config from URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


def decode_base64(string):
    """Decode base64 encoded string."""
    try:
        decoded_string = base64.b64decode(string).decode()
        return decoded_string
    except Exception as e:
        print(f"Decode Error: {e}")
        return None

# Get all configs
def get_cleaned_configs(vmess=False):
    """Get cleaned configs."""
    configs = []
    all_urls = DECODED_URLS + ENCODED_URLS
    for url in track(all_urls, description="Getting configs..."):
        if url in DECODED_URLS:
            config = get_config(url)
            if config!=None:
                configs.extend(config.splitlines())
        elif url in ENCODED_URLS:
            decoded_config = decode_base64(get_config(url))
            if decoded_config:
                configs.extend(decoded_config.splitlines())
    if vmess:
        configs = [config for config in configs if "vmess" in config]
    return configs

# download and save the configs
def save_configs(configs):
    """Save configs to file."""
    file_name = f"./configs_{NOW.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(configs))
    rprint(f"[bold green]Config file saved to {file_name}[/bold green]")


# get random color for the config
def get_random_color(word):
    """Returns a random color wrapped around the given word."""
    random_color = random.choice(COLORS)
    return f"[{random_color}]{word}[{random_color}]"


# generate some random configs, default 5
def get_random_config(configs, random_configs=5):
    """Returns a list of random configs from the given list of whole configs."""
    random_configs = random.sample(configs, random_configs)
    return random_configs


def main():
    """Main function."""
    # Display usage message if no options are provided
    rprint(f"[bold cyan]{LOGO}[/bold cyan]")
    print_to_terminal = False
    while(True):
        rprint("[bold yellow]Configs will be saved in the current directory.\n Would you like to print some of configs in the terminal too?(Y/N)[/bold yellow]")
        yn= input().lower()
        if yn=='y':
            print_to_terminal=True
            rprint("[bold green]OK.[/bold green]")
            break
        elif yn=='n':
            rprint("[bold green]OK.[/bold green]")
            break
        else:
            rprint("[bold red]I didn't understand![/bold red]")
    configs = get_cleaned_configs()
    # Display the number of configs downloaded
    configs_length = len(configs)
    rprint(f"[bold yellow]{configs_length} Configs downloaded.[/bold yellow]\n")
    # Exit if no configs are found
    if configs_length == 0:
        rprint("[bold red]No configs found.Press Enter to exit...[/bold red]")
        input()
        sys.exit(1)
    # Save configs to a file
    # Print random configs with random colors
    counter=0
    if print_to_terminal:
        for config in configs:
            rprint(get_random_color(config))
            rprint("")
            counter+=1
            if counter>=10: break
    save_configs(configs)
    rprint("[bold green]\n\nDone! Press Enter To Close App...[/bold green]")
    input()
    sys.exit(1)

if __name__ == "__main__":
    main()