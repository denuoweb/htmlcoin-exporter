#!/usr/bin/env python3

from prometheus_client import Gauge

import decimal

from .rpc import RPC
from .config import Config
from .metrics import (
    # Difficulty
    HTMLCOIN_DIFFICULTY,
    # Hash per second
    HTMLCOIN_HASH_PS_GAUGES, hash_ps_gauge,
    # Memory info
    HTMLCOIN_MEMINFO_USED, HTMLCOIN_MEMINFO_FREE, HTMLCOIN_MEMINFO_TOTAL, HTMLCOIN_MEMINFO_LOCKED,
    HTMLCOIN_MEMINFO_CHUNKS_USED, HTMLCOIN_MEMINFO_CHUNKS_FREE,
    # Blockchain info
    HTMLCOIN_BLOCKS, HTMLCOIN_SIZE_ON_DISK, HTMLCOIN_VERIFICATION_PROGRESS,
    # Latest block
    HTMLCOIN_LATEST_BLOCK_SIZE, HTMLCOIN_LATEST_BLOCK_TXS, HTMLCOIN_LATEST_BLOCK_HEIGHT, HTMLCOIN_LATEST_BLOCK_WEIGHT,
    HTMLCOIN_LATEST_BLOCK_INPUTS, HTMLCOIN_LATEST_BLOCK_OUTPUTS, HTMLCOIN_LATEST_BLOCK_VALUE, HTMLCOIN_LATEST_BLOCK_FEE,
    # List banned metrics
    HTMLCOIN_BAN_CREATED, HTMLCOIN_BANNED_UNTIL,
    # Network info
    HTMLCOIN_SERVER_VERSION, HTMLCOIN_PROTOCOL_VERSION, HTMLCOIN_WARNINGS, 
    HTMLCOIN_CONNECTIONS, HTMLCOIN_CONNECTIONS_IN, HTMLCOIN_CONNECTIONS_OUT,
    # Chain tx stats
    HTMLCOIN_TX_COUNT,
    # Mempool info
    HTMLCOIN_MEMPOOL_BYTES, HTMLCOIN_MEMPOOL_SIZE, HTMLCOIN_MEMPOOL_USAGE, HTMLCOIN_MEMPOOL_UNBROADCAST,
    # Chain tips
    HTMLCOIN_NUM_CHAIN_TIPS,
    # Estimate smart fee
    HTMLCOIN_ESTIMATED_SMART_FEE_GAUGES, estimate_smart_fee_gauge,
    # Network_totals,
    HTMLCOIN_TOTAL_BYTES_RECV, HTMLCOIN_TOTAL_BYTES_SENT,
    # Uptime
    HTMLCOIN_UPTIME
)


def collect() -> None:

    with RPC(
        url=f"http://{Config.HTMLCOIN_RPC_HOST}:{Config.HTMLCOIN_RPC_PORT}",
        rpc_user=Config.HTMLCOIN_RPC_USER,
        rpc_password=Config.HTMLCOIN_RPC_PASSWORD
    ) as rpc:

        # Set difficulty values
        difficulty: dict = rpc.get_difficulty()
        HTMLCOIN_DIFFICULTY.set(difficulty["proof-of-stake"])

        # Set hash per second values
        for hash_ps_block in Config.HASH_PS_BLOCKS:
            hash_ps: int = rpc.get_network_hash_ps(num_blocks=hash_ps_block)
            if hash_ps is not None:
                gauge: Gauge = hash_ps_gauge(num_blocks=hash_ps_block)
                gauge.set(hash_ps)

        # Set memory info values
        memory_info: dict = rpc.get_memory_info()
        HTMLCOIN_MEMINFO_USED.set(memory_info["locked"]["used"])
        HTMLCOIN_MEMINFO_FREE.set(memory_info["locked"]["free"])
        HTMLCOIN_MEMINFO_TOTAL.set(memory_info["locked"]["total"])
        HTMLCOIN_MEMINFO_LOCKED.set(memory_info["locked"]["locked"])
        HTMLCOIN_MEMINFO_CHUNKS_USED.set(memory_info["locked"]["chunks_used"])
        HTMLCOIN_MEMINFO_CHUNKS_FREE.set(memory_info["locked"]["chunks_free"])
        
        # Set blockchain info values
        blockchain_info: dict = rpc.get_blockchain_info()
        HTMLCOIN_BLOCKS.set(blockchain_info["blocks"])
        # HTMLCOIN_DIFFICULTY.set(blockchain_info["difficulty"])
        HTMLCOIN_SIZE_ON_DISK.set(blockchain_info["size_on_disk"])
        HTMLCOIN_VERIFICATION_PROGRESS.set(blockchain_info["verificationprogress"])
        
        # Set latest block stats values
        latest_block_stats: dict = rpc.get_block_stats(
            blockchain_info["bestblockhash"], "total_size", "total_weight", "totalfee", "txs", "height", "ins", "outs", "total_out"
        )
        if latest_block_stats is not None:
            HTMLCOIN_LATEST_BLOCK_SIZE.set(latest_block_stats["total_size"])
            HTMLCOIN_LATEST_BLOCK_TXS.set(latest_block_stats["txs"])
            HTMLCOIN_LATEST_BLOCK_HEIGHT.set(latest_block_stats["height"])
            HTMLCOIN_LATEST_BLOCK_WEIGHT.set(latest_block_stats["total_weight"])
            HTMLCOIN_LATEST_BLOCK_INPUTS.set(latest_block_stats["ins"])
            HTMLCOIN_LATEST_BLOCK_OUTPUTS.set(latest_block_stats["outs"])
            HTMLCOIN_LATEST_BLOCK_VALUE.set(latest_block_stats["total_out"] / decimal.Decimal(1e8))
            HTMLCOIN_LATEST_BLOCK_FEE.set(latest_block_stats["totalfee"] / decimal.Decimal(1e8))
        
        # Set network info values
        list_banned: list = rpc.list_banned()
        for banned in list_banned:
            HTMLCOIN_BAN_CREATED.labels(
                address=banned["address"], reason=banned.get("ban_reason", "manually added")
            ).set(banned["ban_created"])
            HTMLCOIN_BANNED_UNTIL.labels(
                address=banned["address"], reason=banned.get("ban_reason", "manually added")
            ).set(banned["banned_until"])
        
        # Set network info values
        network_info: dict = rpc.get_network_info()
        HTMLCOIN_SERVER_VERSION.set(network_info["version"])
        HTMLCOIN_PROTOCOL_VERSION.set(network_info["protocolversion"])
        if network_info["warnings"]:
            HTMLCOIN_WARNINGS.inc()
        HTMLCOIN_CONNECTIONS.set(network_info["connections"])
        if "connections_in" in network_info:
            HTMLCOIN_CONNECTIONS_IN.set(network_info["connections_in"])
        if "connections_out" in network_info:
            HTMLCOIN_CONNECTIONS_OUT.set(network_info["connections_out"])

        # Set chain tx stats values
        chain_tx_stats: dict = rpc.get_chain_tx_stats()
        HTMLCOIN_TX_COUNT.set(chain_tx_stats["txcount"])

        # Set mempool info values
        mempool_info: dict = rpc.get_mempool_info()
        HTMLCOIN_MEMPOOL_BYTES.set(mempool_info["bytes"])
        HTMLCOIN_MEMPOOL_SIZE.set(mempool_info["size"])
        HTMLCOIN_MEMPOOL_USAGE.set(mempool_info["usage"])
        if "unbroadcastcount" in mempool_info:
            HTMLCOIN_MEMPOOL_UNBROADCAST.set(mempool_info["unbroadcastcount"])

        # Set chain tips values
        chain_tips: list = rpc.get_chain_tips()
        HTMLCOIN_NUM_CHAIN_TIPS.set(len(chain_tips))

        # Set estimate smart fee values
        for smart_fee_block in Config.SMART_FEE_BLOCKS:
            estimated_smart_fee: dict = rpc.estimate_smart_fee(num_blocks=smart_fee_block)
            if estimated_smart_fee.get("feerate") is not None:
                gauge: Gauge = estimate_smart_fee_gauge(num_blocks=smart_fee_block)
                gauge.set(estimated_smart_fee["feerate"])
        
        # Set network totals values
        network_totals: dict = rpc.get_network_totals()
        HTMLCOIN_TOTAL_BYTES_RECV.set(network_totals["totalbytesrecv"])
        HTMLCOIN_TOTAL_BYTES_SENT.set(network_totals["totalbytessent"])

        # Set uptime values
        uptime: int = rpc.get_uptime()
        HTMLCOIN_UPTIME.set(uptime)
