import minio

client = minio.Minio('192.168.196.221:9000', 'hmcz', '1987yang', secure=False)
client.list_buckets()