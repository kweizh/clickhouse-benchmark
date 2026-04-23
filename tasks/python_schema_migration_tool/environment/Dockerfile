FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL 'https://packages.clickhouse.com/rpm/lts/repodata/repomd.xml.key' | gpg --dearmor -o /usr/share/keyrings/clickhouse-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/clickhouse-keyring.gpg] https://packages.clickhouse.com/deb stable main" | tee /etc/apt/sources.list.d/clickhouse.list && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends clickhouse-server clickhouse-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages clickhouse-connect==0.7.3

RUN mkdir -p /home/user/project && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="ClickHouse python schema migration tool task environment."

# Initialize clickhouse-server so it's ready for testing
CMD ["/bin/bash", "-c", "su -s /bin/bash clickhouse -c 'clickhouse-server --config-file=/etc/clickhouse-server/config.xml --daemon' && trap : TERM INT; sleep infinity & wait"]
