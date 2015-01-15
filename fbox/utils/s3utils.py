"""
Custom S3 storage backends to store files in subfolders.
Use this backend with the boto storage app.
"""

from storages.backends.s3boto import S3BotoStorage


MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')


class StaticRootS3BotoStorage(S3BotoStorage):
    location = 'static'
    reduced_redundancy = True
