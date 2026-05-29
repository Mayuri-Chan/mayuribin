import uvicorn
from mayuribin import config

if __name__ == "__main__":
    uvicorn.run("mayuribin.mayuribin:mayuribin", host=config["app"]["HOST"], port=config["app"]["PORT"], proxy_headers=True, forwarded_allow_ips="*")
