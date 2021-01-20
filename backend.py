import typing
from enum import Enum

import fastapi

from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
import json
import subprocess

app = fastapi.FastAPI()

origins = ["http://localhost:8501", "localhost:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CiscoCommands(str, Enum):
    version = "getversion"
    interfaces = "getinterfaces"


@app.get("/cisco/{cisco_command}", tags=["cisco"])
async def read_cisco_data(cisco_command: CiscoCommands):
    from netmiko import ConnectHandler
    import configparser

    config = configparser.ConfigParser()

    try:
        config.read("secrets.ini")

    except Exception as error:
        print(error)

    myusername = config["auth"]["username"]
    mypassword = config["auth"]["password"]
    mydevice = config["auth"]["mydevice"]

    print(
        "this is from the secrets.ini file. --> {}, {}, {}".format(
            myusername, mypassword, mydevice
        )
    )

    device = {}
    device["device_type"] = "cisco_ios"
    device["ip"] = mydevice
    device["username"] = myusername
    device["password"] = mypassword

    conn = ConnectHandler(**device)
    # output = conn.send_command("show version | i uptime")
    if cisco_command == CiscoCommands.version:
        output = conn.send_command("show version | i uptime")
        output_json = {"results": output}
        return output_json

    if cisco_command == CiscoCommands.interfaces:
        output = conn.send_command("show interface status")
        output_json = {"results": output}
        return output_json
