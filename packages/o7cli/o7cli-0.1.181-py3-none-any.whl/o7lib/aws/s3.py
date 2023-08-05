#!/usr/bin/env python
#************************************************************************
# Copyright 2021 O7 Conseils inc (Philippe Gosselin)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#************************************************************************
"""Module to manage S3 function"""

#--------------------------------
#
#--------------------------------
import pprint
import logging

import o7lib.util.input
import o7lib.util.terminal
import o7lib.util.table
import o7lib.aws.base


logger=logging.getLogger(__name__)

#*************************************************
#
#*************************************************
class S3(o7lib.aws.base.Base):
    """Class to manage S3 operations"""

    #  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

    #*************************************************
    #
    #*************************************************
    def __init__(self, profile = None, region = None):
        super().__init__(profile=profile, region=region)
        self.cS3 = self.session.client('s3')



    #*************************************************
    #
    #*************************************************
    def LoadBuckets(self):
        """Load all Buckets in account"""

        logger.info('LoadBuckets')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
        resp = self.cS3.list_buckets()
        #pprint.pprint(resp)

        buckets = resp.get('Buckets',[])
        logger.info(f'LoadBuckets: Number of Bucket found: {len(buckets)}')

        for bucket in buckets:
            resp = self.cS3.get_bucket_location( Bucket=bucket['Name'])
            bucket['Region'] = resp.get('LocationConstraint','NA')
            if bucket['Region'] is None:
                bucket['Region'] = 'us-east-1'

        return buckets


    #*************************************************
    #
    #*************************************************
    def UploadFile(self, bucket, key, filePath):
        """Upload a file to a bucket"""

        logger.info(f'UploadFile {bucket=} {key=} {filePath=}')

        ret = None

        with open(filePath, 'rb') as fileobj:
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_fileobj
            resp = self.cS3.upload_fileobj(fileobj, Bucket=bucket, Key=key,)
            logger.info(f'UploadFile: Done {resp=}')
            ret = f'https://s3-external-1.amazonaws.com/{bucket}/{key}'

        return ret

    #*************************************************
    #
    #*************************************************
    def DisplayBuckets(self, buckets):
        """Display the list buckets"""

        self.ConsoleTitle(left='S3 List of Buckets')
        print('')

        param = {
            'columns' : [
                {'title' : 'id',      'type': 'i',    },
                {'title' : 'Name',    'type': 'str',      'dataName': 'Name'},
                {'title' : 'Created', 'type': 'datetime', 'dataName': 'CreationDate'},
                {'title' : 'Region',  'type': 'str', 'dataName': 'Region'},
            ]
        }
        o7lib.util.table.Table(param=param, datas=buckets).Print()


        return


    #*************************************************
    #
    #*************************************************
    def MenuBuckets(self):
        """S3 main menu"""

        while True :

            buckets = self.LoadBuckets()
            self.DisplayBuckets(buckets)
            typ, key = o7lib.util.input.InputMulti('Option -> Back(b) Raw(r) Details(int): ')

            if typ == 'str':
                if key.lower() == 'b':
                    break
                if key.lower() == 'r':
                    pprint.pprint(buckets)
                    o7lib.util.input.WaitInput()

            if typ == 'int' and  0 < key <= len(buckets):
                pprint.pprint(buckets[key - 1])
                o7lib.util.input.WaitInput()


#*************************************************
#
#*************************************************
if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)-5.5s] [%(name)s] %(message)s"
    )

    theS3 = S3()
    theS3.MenuBuckets()
