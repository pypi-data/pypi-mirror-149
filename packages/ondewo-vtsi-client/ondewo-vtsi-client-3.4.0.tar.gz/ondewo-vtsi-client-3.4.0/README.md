<p align="center">
    <a href="https://www.ondewo.com">
      <img alt="ONDEWO Logo" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/github/ondewo_logo_github_2.png"/>
    </a>
  <h1 align="center">
    ONDEWO Voice Client
  </h1>
</p>

# Ondewo VTSI Client Python

The vtsi client allows for easy control of the ONDEWO VTSI server. With it, you can configure the connection to text-to-speech, speech-to-text, conversational-ai etc. It allows for making large numbers of voip-calls in parallel, and returns detailed logs regarding the status of the calls.

## Quickstart

1) install all the dependencies (`make install`)
2) set up ssh tunnel to the voip-server machine (`ssh -fNL 40045:localhost:40045 <machine ip>`)

## Ipython example
```
from ondewo.vtsi.voip_server_client import VtsiServerClient

voip_host = 'localhost'
voip_port = '40045'
client = VtsiServerClient.get_minimal_client(voip_host=voip_host, voip_port=voip_port)

ids = client.get_call_ids()
for id in ids:
    status = client.get_instance_status(id)
    try:
        health = status.helth
    except:
        health = None
    try:
        log = status.last_log
    except:
        log = None
    print(f"call: {id}, health: {health}, last_log: {log}")
```

## Script example
```
python script.py
```
