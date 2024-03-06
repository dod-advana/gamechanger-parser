# Getting Started

# Config
`config/dockerConf/setupDockerEnv.sh` \
gets vs code packages and builds docker image

# Run
`start.sh` \
after setupDockerEnv has been run successfully, this starts docker with correct port forward and file mount

## Jupyter in browser
navigate to `http://127.0.0.1:8888` \
password is `gamechanger`

## Ipynb in vs-code
open an ipynb file, eg `gamechanger-parser/config/test.ipynb` \
top right, connect to kernel \
select "Existing Jupyter Server..." \
in text box "Enter remote url" type `http://127.0.0.1:8888` \
enter password `gamechanger` \
select `python3` kernel

# Known Issues
Open jupyter tabs or jupyter files in vs-code will spam server with requests that will fail (403 GET) if the server has been stopped and started \
eg `[W 2024-03-06 19:39:33.516 ServerApp] 403 GET /api/sessions?1709753973500 (@192.168.65.1) 0.93ms referer=None` \
To fix, close old browser tabs \
or unfortunately, close and reopen vs-code since there doesn't seem to be a way to stop it from trying to connect to a kernel


# TODO:
1. Refactor files into a more succinct form
2. Add more granular error handling for each of the specific types of errors for a document and how many succeed/fail in a batch
3. Add pytests to protect code
4. Make overall package pip installable