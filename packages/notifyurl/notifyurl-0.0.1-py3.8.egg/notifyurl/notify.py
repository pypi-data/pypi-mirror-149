import configparser
import argparse
import requests
import os

def send(url, content: str) -> None:
    params = {
        "msg_type": "text",
        "content": {"text": content},
    }
    resp = requests.post(url=url, json=params)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") and result["code"] != 0:
        print(result["msg"])
        return
    print("notification sent")

def main():
    parser = argparse.ArgumentParser()
    config = configparser.ConfigParser()
    if os.path.isfile("config.ini"):
        config.read("config.ini")
        hook_url = config["default"]["url"]
    else:
        print("please set url:")
        hook_url = input()
        config["default"] = {"url": hook_url}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    parser.add_argument("cmd", help="the task to excecute")

    args = parser.parse_args()

    os.system(args.cmd)
    send(url=hook_url, content="cmd complete")


if __name__ == '__main__':
    main()
