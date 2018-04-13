import boto3
import rom.config as config

class boto(object):

    __session = None
    __bucket = config.bucketRoms
    __s3 = None

    def __init__(self):
        self.__session= boto3.session.Session(
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key
        )
        self.__s3= self.__session.resource('s3')

    def put(self, dest_file, bin_file):
        print("Put >> {}".format(dest_file))
        object_file = self.__s3.Object(self.__bucket, dest_file)
        output = object_file.put(Body=bin_file.read())

if __name__ == '__main__':
    b = boto()