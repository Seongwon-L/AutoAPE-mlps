# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import Tuple, List
import numpy as np
import json

from mlps.common.Common import Common
from mlps.common.Constants import Constants
from mlps.info.FieldInfo import FieldInfo
from dataconverter.core.ConvertAbstract import ConvertAbstract
from dataconverter.core.ConvertFactory import ConvertFactory
from pycmmn.rest.RestManager import RestManager


class DataLoaderAbstract(object):
    LOGGER = Common.LOGGER.getLogger()

    def __init__(self, job_info, sftp_client):
        self.job_info = job_info
        self.sftp_client = sftp_client

    @staticmethod
    def _convert(line, fields, functions) -> Tuple[list, list, dict]:
        features = list()
        labels = list()

        for idx, field in enumerate(fields):
            if True:  # not field.multiple():
                name = field.field_name
                value = line.get(name, "")
            # else:
            #     value = list()
            #     for name in field.field_name.split("@COMMA@"):
            #         value.append(line.get(name, ""))

            # TODO : 한 필드에 2개의 함수가 있을 경우 잘 동작하는지 확인
            for fn in functions[idx]:
                value = fn.apply(value)

            if field.label():
                labels += value
            else:
                if name == "image":
                    features = value[0]
                else:
                    features += value
        return features, labels, line

    @classmethod
    def build_functions(cls, fields: List[FieldInfo]) -> List[List[ConvertAbstract]]:
        functions: List[List[ConvertAbstract]] = list()
        for field in fields:
            cvt_fn_list: List[ConvertAbstract] = list()
            for fn_info in field.get_function():
                cvt_fn_list.append(ConvertFactory.create_cvt_fn(
                    cvt_fn_info=fn_info,
                    logger=cls.LOGGER,
                    cvt_dict=RestManager.get_cnvr_dict(
                        rest_url_root=Constants.REST_URL_ROOT, logger=cls.LOGGER
                    )
                ))
            functions.append(cvt_fn_list)
        return functions

    def make_inout_units(self, features, fields: List[FieldInfo]):
        input_units = np.shape(features)[1:]
        output_units = self.get_output_units(fields)
        self.job_info.set_input_units(input_units)
        self.job_info.set_output_units(output_units)
        self.LOGGER.info("input_units : {}".format(input_units))
        self.LOGGER.info("output_units : {}".format(output_units))

    def get_output_units(self, fields: List[FieldInfo]):
        for field_info in fields:
            self.LOGGER.info(field_info.is_label)
            self.LOGGER.info(field_info.stat_dict)
            if field_info.is_label:
                try:
                    return len(field_info.stat_dict.get("unique", {}))
                except Exception as e:
                    self.LOGGER.error(e, exc_info=True)
                    return 1

    def write_dp_result(self, features, labels, file_path):
        rst_dict = dict()
        save_path = file_path.rsplit('/', 2)[0]

        self.LOGGER.info("features[0]: {}".format(features[0]))
        self.LOGGER.info("labels[0]: {}".format(labels[0]))

        rst_dict['features'] = features
        rst_dict['targets'] = labels

        f = self.sftp_client.get_client().open(
            f"{save_path}/{self.job_info.get_hist_no()}_{self.job_info.get_task_idx()}.dp",
            'w'
        )

        try:
            f.write(json.dumps(rst_dict, indent=2))
        except Exception as e:
            self.LOGGER.error(e, exc_info=True)
        finally:
            f.close()

    def read(self, file_list: List[str], fields: List[FieldInfo]) -> List:
        raise NotImplementedError
