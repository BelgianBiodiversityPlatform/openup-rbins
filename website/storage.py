from storages.backends.s3boto import S3BotoStorage

# To allow FileField/ImageField deletion: http://www.laplacesdemon.com/2013/07/11/solving-django-storage-notimplementederror-for-amazon-s3/
class FixedS3BotoStorage(S3BotoStorage):
    def path(self, name):
        return self._normalize_name(name)
