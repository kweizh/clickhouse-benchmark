FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL 'https://builds.clickhouse.com/master/amd64/clickhouse' -o /usr/local/bin/clickhouse && \
    chmod +x /usr/local/bin/clickhouse && \
    ln -s /usr/local/bin/clickhouse /usr/local/bin/clickhouse-server && \
    ln -s /usr/local/bin/clickhouse /usr/local/bin/clickhouse-client

RUN pip3 install --break-system-packages clickhouse-connect

RUN mkdir -p /home/user/project && chmod 0755 /home/user && chmod 0755 /home/user/project

LABEL Author="any-task-builder"
LABEL Description="ClickHouse task environment with clickhouse-server and clickhouse-connect installed."

# Container contents:
#   - clickhouse-server and clickhouse-client binaries
#   - python3 and clickhouse-connect library
#   - /home/user/project directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
