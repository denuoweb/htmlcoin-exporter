#!/usr/bin/env python3

from prometheus_client import (
    Gauge, Counter
)
from typing import (
    Optional, Dict
)


# Difficulty metrics
HTMLCOIN_DIFFICULTY: Gauge = Gauge(
    "htmlcoin_difficulty", "The current difficulty"
)

# Hash per second metrics
HTMLCOIN_HASH_PS_GAUGES: Dict[int, Gauge] = { }


def hash_ps_gauge(num_blocks: int) -> Gauge:
    gauge: Optional[Gauge] = HTMLCOIN_HASH_PS_GAUGES.get(num_blocks)

    def hashps_gauge_suffix(nblocks):
        if nblocks < 0:
            return f"_neg{-nblocks}"
        if nblocks == 120:
            return ""
        return f"_{nblocks}"

    if gauge is None:
        desc_end: str = (
            "since the last difficulty change" if num_blocks == -1 else f"for the last {num_blocks} blocks"
        )
        gauge: Gauge = Gauge(
            f"htmlcoin_hash_ps{hashps_gauge_suffix(num_blocks)}",
            f"Estimated network hash rate per second {desc_end}",
        )
        HTMLCOIN_HASH_PS_GAUGES[num_blocks] = gauge
    return gauge


# Memory info metrics
HTMLCOIN_MEMINFO_USED: Gauge = Gauge(
    "htmlcoin_meminfo_used", "Number of bytes used"
)
HTMLCOIN_MEMINFO_FREE: Gauge = Gauge(
    "htmlcoin_meminfo_free", "Number of bytes available in current arenas"
)
HTMLCOIN_MEMINFO_TOTAL: Gauge = Gauge(
    "htmlcoin_meminfo_total", "Total number of bytes managed"
)
HTMLCOIN_MEMINFO_LOCKED: Gauge = Gauge(
    "htmlcoin_meminfo_locked", "Amount of bytes that succeeded locking. If this number is smaller than total, "
                           "locking pages failed at some point and key data could be swapped to disk."
)
HTMLCOIN_MEMINFO_CHUNKS_USED: Gauge = Gauge(
    "htmlcoin_meminfo_chunks_used", "Number of allocated chunks"
)
HTMLCOIN_MEMINFO_CHUNKS_FREE: Gauge = Gauge(
    "htmlcoin_meminfo_chunks_free", "Number of unused chunks"
)

# Blockchain info metrics
HTMLCOIN_BLOCKS: Gauge = Gauge(
    "htmlcoin_blocks", "The current number of blocks processed in the server"
)
HTMLCOIN_SIZE_ON_DISK: Gauge = Gauge(
    "htmlcoin_size_on_disk", "The estimated size of the block and undo files on disk"
)
HTMLCOIN_VERIFICATION_PROGRESS: Gauge = Gauge(
    "htmlcoin_verification_progress", "Estimate of verification progress [0..1]"
)

# Latest block stats metrics
HTMLCOIN_LATEST_BLOCK_SIZE: Gauge = Gauge(
    "htmlcoin_latest_block_size", "Size of latest block in bytes"
)
HTMLCOIN_LATEST_BLOCK_TXS: Gauge = Gauge(
    "htmlcoin_latest_block_txs", "Number of transactions in latest block"
)
HTMLCOIN_LATEST_BLOCK_HEIGHT: Gauge = Gauge(
    "htmlcoin_latest_block_height", "Height or index of latest block"
)
HTMLCOIN_LATEST_BLOCK_WEIGHT: Gauge = Gauge(
    "htmlcoin_latest_block_weight", "Weight of latest block according to BIP 141"
)
HTMLCOIN_LATEST_BLOCK_INPUTS: Gauge = Gauge(
    "htmlcoin_latest_block_inputs", "Number of inputs in transactions of latest block"
)
HTMLCOIN_LATEST_BLOCK_OUTPUTS: Gauge = Gauge(
    "htmlcoin_latest_block_outputs", "Number of outputs in transactions of latest block"
)
HTMLCOIN_LATEST_BLOCK_VALUE: Gauge = Gauge(
    "htmlcoin_latest_block_value", "Htmlcoin value of all transactions in the latest block"
)
HTMLCOIN_LATEST_BLOCK_FEE: Gauge = Gauge(
    "htmlcoin_latest_block_fee", "Total fee to process the latest block"
)

# List banned metrics
HTMLCOIN_BAN_CREATED: Gauge = Gauge(
    "htmlcoin_ban_created", "Time the ban was created", labelnames=["address", "reason"]
)
HTMLCOIN_BANNED_UNTIL: Gauge = Gauge(
    "htmlcoin_banned_until", "Time the ban expires", labelnames=["address", "reason"]
)

# Network info metrics
HTMLCOIN_SERVER_VERSION: Gauge = Gauge(
    "htmlcoin_server_version", "The server version"
)
HTMLCOIN_PROTOCOL_VERSION: Gauge = Gauge(
    "htmlcoin_protocol_version", "The protocol version of the server"
)
HTMLCOIN_CONNECTIONS: Gauge = Gauge(
    "htmlcoin_connections", "The number of connections or peers"
)
HTMLCOIN_CONNECTIONS_IN: Gauge = Gauge(
    "htmlcoin_connections_in", "The number of connections in"
)
HTMLCOIN_CONNECTIONS_OUT: Gauge = Gauge(
    "htmlcoin_connections_out", "The number of connections out"
)
HTMLCOIN_WARNINGS: Counter = Counter(
    "htmlcoin_warnings", "Number of network or blockchain warnings detected"
)

# Chain tx stats metrics
HTMLCOIN_TX_COUNT: Gauge = Gauge(
    "htmlcoin_tx_count", "Number of TX since the genesis block"
)

# Mempool info metrics
HTMLCOIN_MEMPOOL_BYTES: Gauge = Gauge(
    "htmlcoin_mempool_bytes", "Size of mempool in bytes"
)
HTMLCOIN_MEMPOOL_SIZE: Gauge = Gauge(
    "htmlcoin_mempool_size", "Number of unconfirmed transactions in mempool"
)
HTMLCOIN_MEMPOOL_USAGE: Gauge = Gauge(
    "htmlcoin_mempool_usage", "Total memory usage for the mempool"
)
HTMLCOIN_MEMPOOL_UNBROADCAST: Gauge = Gauge(
    "htmlcoin_mempool_unbroadcast", "Number of transactions waiting for acknowledgment"
)

# Chain tips metrics
HTMLCOIN_NUM_CHAIN_TIPS: Gauge = Gauge(
    "htmlcoin_num_chain_tips", "Number of known blockchain branches"
)

# Estimate smart fee metrics
HTMLCOIN_ESTIMATED_SMART_FEE_GAUGES: Dict[int, Gauge] = { }


def estimate_smart_fee_gauge(num_blocks: int) -> Gauge:
    gauge: Optional[Gauge] = HTMLCOIN_ESTIMATED_SMART_FEE_GAUGES.get(num_blocks)
    if gauge is None:
        gauge: Gauge = Gauge(
            f"htmlcoin_estimate_smart_fee_{num_blocks}",
            f"Estimated smart fee per kilobyte for confirmation in {num_blocks} blocks"
        )
        HTMLCOIN_ESTIMATED_SMART_FEE_GAUGES[num_blocks] = gauge
    return gauge


# Network totals metrics
HTMLCOIN_TOTAL_BYTES_RECV: Gauge = Gauge(
    "htmlcoin_total_bytes_recv", "Total bytes received"
)
HTMLCOIN_TOTAL_BYTES_SENT: Gauge = Gauge(
    "htmlcoin_total_bytes_sent", "Total bytes sent"
)

# Uptime metrics
HTMLCOIN_UPTIME: Gauge = Gauge(
    "htmlcoin_uptime", "The number of seconds that the server has been running"
)

# Htmlcoin exporters metrics
EXPORTER_ERRORS: Counter = Counter(
    "htmlcoin_exporter_errors", "Number of errors encountered by the exporter", labelnames=["type"]
)
PROCESS_TIME: Counter = Counter(
    "htmlcoin_exporter_process_time", "Time spent processing metrics from htmlcoin node"
)
