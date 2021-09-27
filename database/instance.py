from couchbase.options import LockMode
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator

def getBucket(bucket_name:str) -> Bucket:
    cluster = Cluster(
        'couchbase://localhost',
        ClusterOptions(
            PasswordAuthenticator('root', 'jonk2010')
        )
    )
    bucket: Bucket = cluster.bucket(bucket_name)
    return bucket