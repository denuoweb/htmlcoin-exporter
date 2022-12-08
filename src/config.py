#!/usr/bin/env python3

import typing
import os


class Config(object):
    
    HTMLCOIN_RPC_HOST: str = os.environ.get("HTMLCOIN_RPC_HOST", default="0.0.0.0")
    HTMLCOIN_RPC_PORT: int = int(os.environ.get("HTMLCOIN_RPC_PORT", default="4889"))  # Htmlcoin testnet default port
    HTMLCOIN_RPC_USER: str = os.environ.get("HTMLCOIN_RPC_USER", default="htmlcoin")
    HTMLCOIN_RPC_PASSWORD: str = os.environ.get("HTMLCOIN_RPC_PASSWORD", default="testpasswd")

    HASH_PS_BLOCKS: typing.List[int] = [
        int(block) for block in os.environ.get("HASH_PS_BLOCKS", default="-1,1,120").split(",") if block != str()
    ]
    SMART_FEE_BLOCKS: typing.List[int] = [
        int(block) for block in os.environ.get("SMART_FEE_BLOCKS", default="2,3,5,20").split(",") if block != str()
    ]

    METRICS_ADDRESS: str = os.environ.get("METRICS_ADDRESS", default="0.0.0.0")
    METRICS_PORT: int = int(os.environ.get("METRICS_PORT", default="6363"))

    TIMEOUT: float = float(os.environ.get("TIMEOUT", default=15))
    REFRESH_SECONDS: int = int(os.environ.get("REFRESH_SECONDS", default=5))
    LOGGING_LEVEL: str = os.environ.get("LOGGING_LEVEL", default="INFO")
