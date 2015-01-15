"""
Custom S3 storage backends to store files in subfolders.
Use this backend with the boto storage app.

Make sure you use an alternative thumbnailer class for FeinCMS, such as
feincms_sorl_thumbnailer.

Use these settings for S3:

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = '<bucket name>'
AWS_LOCATION = '/media/'
AWS_QUERYSTRING_EXPIRE = 60*60*48
AWS_S3_FILE_OVERWRITE = False

"""

from storages.backends.s3boto import S3BotoStorage


# use concrete class because of sorl
class MediaRootS3BotoStorage(S3BotoStorage):
    location = 'media'


class StaticRootS3BotoStorage(S3BotoStorage):
    location = 'static'
    reduced_redundancy = True
