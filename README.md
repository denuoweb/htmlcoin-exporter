
# Htmlcoin Exporter

A [Prometheus](https://prometheus.io) exporter for Htmlcoin nodes.

## Installation

To get started, just fork this repository, clone it locally, and build docker image:

```shell
docker build --tag htmlcoin/htmlcoin-exporter:latest .
```

Or, after cloning it locally, and run:

```shell
python -m pip install -r requirements.txt
```

To use the pre-built image just pull it:

```shell
docker pull htmlcoin/htmlcoin-exporter:latest
```

For the versions available, see the [tags on docker hub](https://hub.docker.com/r/htmlcoin/htmlcoin-exporter/tags) repository.

## Quick Usage
 
To run htmlcoin-exporter from source code:

```shell
python moniter.py
```

Or, to run htmlcoin-exporter from docker:

```shell
docker run -d -p 6363:6363 \
  -e HTMLCOIN_RPC_HOST="0.0.0.0" \
  -e HTMLCOIN_RPC_PORT="4889" \
  -e HTMLCOIN_RPC_USER="<htmlcoind_username>" \
  -e HTMLCOIN_RPC_PASSWORD="<htmlcoind_password>" \
  -e REFRESH_SECONDS=5 \
  HTMLCOIN/HTMLCOIN-exporter:latest
```

Then visit [http://localhost:6363](http://localhost:6363) to view the metrics.

## Screenshot

On Prometheus

![Prometheus Screenshot](https://raw.githubusercontent.com/htmlcoin/htmlcoin-exporter/master/screenshots/prometheus.png)

On Grafana

![Grafana Screenshot](https://raw.githubusercontent.com/htmlcoin/htmlcoin-exporter/master/screenshots/grafana.png)

## Environment Variables

Here are the following environment variables with default values:

| Keys              | Description                                                           | Default Values |
|-------------------|-----------------------------------------------------------------------|----------------|
| HTMLCOIN_RPC_HOST     | Bind to given address to listen for JSON-RPC connections              | ``0.0.0.0``    |
| HTMLCOIN_RPC_PORT     | Listen for JSON-RPC connections on port                               | ``4889``       |
| HTMLCOIN_RPC_USER     | Username for JSON-RPC connections                                     | ``htmlcoin``       |
| HTMLCOIN_RPC_PASSWORD | Password for JSON-RPC connections                                     | ``testpasswd`` |
| HASH_PS_BLOCKS        | Estimated network hash rate per second                                | ``-1,1,120``   |
| SMART_FEE_BLOCKS      | Estimated smart fee per kilobyte for confirmation in {nblocks} blocks | ``2,3,5,20``   |
| METRICS_ADDRESS       | Bind to given address to listen for Htmlcoin-Exporter connections.    | ``0.0.0.0``    |
| METRICS_PORT          | Listen for Htmlcoin-Exporter connections on port                      | ``6363``       |
| TIMEOUT               | The maximum time allocated to collect data in seconds                 | ``15``         |
| REFRESH_SECONDS       | Refreshing time set to collect data in seconds                        | ``5``          |
| LOGGING_LEVEL         | Determines which severity of messages it will pass to its handlers    | ``INFO``       |

## Prometheus Config

The prometheus.yml settings looks like:

```yaml
scrape_configs:
  - job_name: "htmlcoin-exporter"
    static_configs:
      - targets: ["0.0.0.0:6363"]

```

## Exported Metrics

Here are available exported metrics:

| Metric                                | Meaning                                                                                                                                                 | Type    |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| ``htmlcoin_difficulty``                   | The current difficulty                                                                                                                                  | Gauge   |
| ``htmlcoin_hash_ps_{nblocks}``            | Estimated network hash rate per second                                                                                                                  | Gauge   |
| ``htmlcoin_meminfo_used``                 | Number of bytes used                                                                                                                                    | Gauge   |
| ``htmlcoin_meminfo_free``                 | Number of bytes available in current arenas                                                                                                             | Gauge   |
| ``htmlcoin_meminfo_total``                | Total number of bytes managed                                                                                                                           | Gauge   |
| ``htmlcoin_meminfo_locked``               | Amount of bytes that succeeded locking. If this number is smaller than total, locking pages failed at some point and key data could be swapped to disk. | Gauge   |
| ``htmlcoin_meminfo_chunks_used``          | Number of allocated chunks                                                                                                                              | Gauge   |
| ``htmlcoin_meminfo_chunks_free``          | Number of unused chunks                                                                                                                                 | Gauge   |
| ``htmlcoin_blocks``                       | The current number of blocks processed in the server                                                                                                    | Gauge   |
| ``htmlcoin_size_on_disk``                 | The estimated size of the block and undo files on disk                                                                                                  | Gauge   |
| ``htmlcoin_verification_progress``        | Estimate of verification progress [0..1]                                                                                                                | Gauge   |
| ``htmlcoin_latest_block_size``            | Size of latest block in bytes                                                                                                                           | Gauge   |
| ``htmlcoin_latest_block_txs``             | Number of transactions in latest block                                                                                                                  | Gauge   |
| ``htmlcoin_latest_block_height``          | Height or index of latest block                                                                                                                         | Gauge   |
| ``htmlcoin_latest_block_weight``          | Weight of latest block according to BIP 141                                                                                                             | Gauge   |
| ``htmlcoin_latest_block_inputs``          | Number of inputs in transactions of latest block                                                                                                        | Gauge   |
| ``htmlcoin_latest_block_outputs``         | Number of outputs in transactions of latest block                                                                                                       | Gauge   |
| ``htmlcoin_latest_block_value``           | Htmlcoin value of all transactions in the latest block                                                                                                      | Gauge   |
| ``htmlcoin_latest_block_fee``             | Total fee to process the latest block                                                                                                                   | Gauge   |
| ``htmlcoin_ban_created``                  | Time the ban was created                                                                                                                                | Gauge   |
| ``htmlcoin_banned_until``                 | Time the ban expires                                                                                                                                    | Gauge   |
| ``htmlcoin_server_version``               | The server version                                                                                                                                      | Gauge   |
| ``htmlcoin_protocol_version``             | The protocol version of the server                                                                                                                      | Gauge   |
| ``htmlcoin_connections``                  | The number of connections or peers                                                                                                                      | Gauge   |
| ``htmlcoin_connections_in``               | The number of connections in                                                                                                                            | Gauge   |
| ``htmlcoin_connections_out``              | The number of connections out                                                                                                                           | Gauge   |
| ``htmlcoin_warnings``                     | Number of network or blockchain warnings detected                                                                                                       | Counter |
| `htmlcoin_tx_count`                       | Number of TX since the genesis block                                                                                                                    | Gauge   |
| ``htmlcoin_mempool_bytes``                | Size of mempool in bytes                                                                                                                                | Gauge   |
| ``htmlcoin_mempool_size``                 | Number of unconfirmed transactions in mempool                                                                                                           | Gauge   |
| ``htmlcoin_mempool_usage``                | Total memory usage for the mempool                                                                                                                      | Gauge   |
| ``htmlcoin_mempool_unbroadcast``          | Number of transactions waiting for acknowledgment                                                                                                       | Gauge   |
| ``htmlcoin_num_chain_tips``               | Number of known blockchain branches                                                                                                                     | Gauge   |
| ``htmlcoin_estimate_smart_fee_{nblocks}`` | Estimated smart fee per kilobyte for confirmation in {nblocks} blocks                                                                                   | Gauge   |
| ``htmlcoin_total_bytes_recv``             | Total bytes received                                                                                                                                    | Gauge   |
| ``htmlcoin_total_bytes_sent``             | Total bytes sent                                                                                                                                        | Gauge   |
| ``htmlcoin_uptime``                       | The number of seconds that the server has been running                                                                                                  | Gauge   |
| ``htmlcoin_exporter_errors``              | Number of errors encountered by the exporter                                                                                                            | Counter |
| ``htmlcoin_exporter_process_time``        | Time spent processing metrics from htmlcoin node                                                                                                            | Counter |

## License

Distributed under the [MIT](https://github.com/htmlcoin/htmlcoin-exporter/blob/master/LICENSE) license. See ``LICENSE`` for more information.
