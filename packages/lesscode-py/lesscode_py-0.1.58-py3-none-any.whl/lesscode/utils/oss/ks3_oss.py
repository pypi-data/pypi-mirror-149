import tornado.options
from ks3.connection import Connection


class Ks3Oss:
    def __init__(self, **kwargs):
        if not kwargs.get("access_key_id"):
            kwargs.update({"access_key_id": tornado.options.options.ks3_connect_config.get("access_key_id")})
        if not kwargs.get("access_key_secret"):
            kwargs.update({"access_key_secret": tornado.options.options.ks3_connect_config.get("access_key_secret")})
        if not kwargs.get("host"):
            kwargs.update({"host": tornado.options.options.ks3_connect_config.get("host")})
        bucket_name = kwargs.pop("bucket_name", None)
        self.client = Connection(**kwargs)
        if bucket_name is not None:
            self.instance = self.client.get_bucket(bucket_name)
        else:
            self.instance = None

    def create_bucket(self, bucket_name, **kwargs):
        bucket = self.client.create_bucket(bucket_name=bucket_name, **kwargs)
        return bucket

    def save(self, key_name, bucket_name="", content_type="string", **kwargs):
        if self.instance is None:
            self.instance = self.client.get_bucket(bucket_name)
        k = self.instance.new_key(key_name)
        ret = None
        if content_type == "string":
            ret = k.set_contents_from_string(**kwargs)
        elif content_type == "file":
            ret = k.set_contents_from_filename(**kwargs)
        elif content_type == "network":
            ret = k.fetch_object(**kwargs)
        if ret:
            if ret.status == 200:
                return True
            else:
                return False
        else:
            return False

    def get_url(self, key, bucket_name="", region="ks3-cn-beijing", domain="ksyun.com", protocol="https"):
        if self.instance is None:
            self.instance = self.client.get_bucket(bucket_name)
        if self.instance.get_key(key):
            return f'{protocol}://{bucket_name}.{region}.{domain}/{key}'
        else:
            return None

    def get_file(self, key, bucket_name=""):
        if self.instance is None:
            self.instance = self.client.get_bucket(bucket_name)
        key = self.instance.get_key(key)
        contents = key.get_contents_as_string()
        return contents
