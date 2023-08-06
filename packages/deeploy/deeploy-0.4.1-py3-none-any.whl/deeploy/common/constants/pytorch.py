PYTORCH_CONFIG_FILE = """inference_address=http://0.0.0.0:8085
management_address=http://0.0.0.0:8081
metrics_address=http://0.0.0.0:8082
enable_metrics_api=true
metrics_format=prometheus
number_of_netty_threads=4
job_queue_size=10
service_envelope=kfserving
model_store=/mnt/models/model-store
model_snapshot={"name":"startup.cfg","modelCount":1,"models":{"model":{"1.0":{"defaultVersion":true,"marName":"model.mar","minWorkers":1,"maxWorkers":5,"batchSize":1,"maxBatchDelay":5000,"responseTimeout":120}}}}

""" # noqa