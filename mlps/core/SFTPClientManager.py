# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.
import json
from typing import List

from mlps.common.sftp.PySFTPClient import PySFTPClient
from mlps.common.Constants import Constants
from mlps.common.Common import Common


class SFTPClientManager(object):
    # class : SFTPClientManager
    def __init__(self, service: str, username: str, password: str):
        self.logger = Common.LOGGER.getLogger()
        self.service: List[str] = service.split(":")
        self.username = username
        self.password = password

        self.sftp_client = PySFTPClient(self.service[0], int(self.service[1]),
                                        self.username, self.password)

        self.logger.info("initialized service - [{}] SFTP Client Initialized.".format(service))

    def get_client(self) -> PySFTPClient:
        return self.sftp_client

    def rename(self, src, dst) -> None:
        self.sftp_client.rename(src, dst)

    def close(self) -> None:
        self.sftp_client.close()

    def load_json_data(self, filename):
        json_data = None
        f = None
        try:
            f = self.get_client().open(filename, "r")
            json_data = json.loads(f.read())
        except Exception as e:
            self.logger.error(e, exc_info=True)
            self.logger.error(f"file path : {filename}")
        finally:
            f.close()
        return json_data

    def load_json_oneline(self, filename):
        f = self.get_client().open(filename, "r")
        data = None
        while True:
            try:
                data = f.readline()
                if data is None or data == "":
                    yield "#file_end#"
                    break
                else:
                    yield json.loads(data)
            except Exception as e:
                self.logger.error(data)

        f.close()


if __name__ == '__main__':
    sm = SFTPClientManager("10.1.35.118:22", "Kmw/y3YWiiO7gJ/zqMvCuw==", "jTf6XrqcYX1SAhv9JUPq+w==")
    gee = sm.load_json_oneline("/eyeCloudAI/data/processing/ape/division/99429867778487988_0.done")

    while True:
        print(next(gee))
