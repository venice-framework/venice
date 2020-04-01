## view connectors

curl kafka-connect:8083/connectors

## getting tasks for a connector

replace postgres-sink-1 with your connector name
curl kafka-connect:8083/connectors/postgres-sink-1/tasks | jq

## Restart connector task

curl -s -X PUT host:port/connectors/postgres-sink-1/resume
