
# 1. define groups / channels
config = {
    "telegram_name": "xxx",
    "groups": {
        58xxxxx: {
            "name": "xxx",
            "sync": True,
            "build": True
        },
    },
    "defaults":{
        "api_id": "14xxx",
        "api_hash": "91xxx",
        "proxy": {
            "enable": False,
            "protocol": "socks5",
            "addr": "127.0.0.1",
            "port": 1081
        },
        "publish_rss_feed": False # True maybe except
    }
}