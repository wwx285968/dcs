# -*- coding: utf-8 -*-
"""
@file: edit_detector_controller
@desc:
@author: Jaden Wu
@time: 2021/10/20 9:25
"""
from datetime import datetime

from dcs.usecases.add_detectors_case import AddDetectorsCase, detector_id
from dcs.usecases.get_detectors_case import GetDetectorsCase
from dcs.usecases.modify_detector_case import ModifyDetectorCase
from dcs.usecases.delete_detectors_case import DeleteDetectorsCase
from dcs.usecases.modify_monitor_case import ModifyMonitorCase
from dcs.adapter.sqls.repo import DetectorRepo, MonitorRepo


to_view = {
    "decimal_point": str,
    "install_time": lambda it: str(it.date())
}


to_case = {
    "decimal_point": int,
    "install_time": lambda it: datetime.strptime(it, "%Y-%m-%d")
}


def identity(item):
    return item


edit_detector_model = (
    "area",
    "address_code",
    "position",
    "decimal_point",
    "material",
    "unit",
    "install_time"
)


class EditDetectorsController(object):
    def __init__(self, view, session):
        self.view = view

        self.detector_repo = DetectorRepo(session)
        self.monitor_repo = MonitorRepo(session)
        self.detectors_from_repo = []  # 主要为了保存行数与设备在数据库的id的对应关系
        self.monitor_code = ""

    def update_edit_table(self):
        del self.detectors_from_repo[:]
        detectors_from_repo = GetDetectorsCase(self.detector_repo).get_detectors(self.monitor_code)
        self.detectors_from_repo.extend(detectors_from_repo)
        edit_detectors_list = []
        for dev in self.detectors_from_repo:
            detector_info = {k: to_view.get(k, identity)(dev.get(k, "")) for k in edit_detector_model}
            edit_detectors_list.append(detector_info)
        ModifyMonitorCase(self.monitor_repo).modify_monitor_by_code(
            self.monitor_code,
            {"detector_num": len(edit_detectors_list)}
        )
        self.view.update_edit_table(edit_detectors_list)

    def set_monitor_code(self, monitor_code):
        self.monitor_code = monitor_code
        self.update_edit_table()

    def add_detector_rows(self, area, monitor_code, detector_num):
        add_res = AddDetectorsCase(self.detector_repo).add_detectors(area, monitor_code, detector_num)
        self.update_edit_table()
        return add_res

    def modify_detector_row(self, row, col, content):
        _id = self.detectors_from_repo[row][detector_id]
        new_detector_info = {edit_detector_model[col]: content}
        modify_res = ModifyDetectorCase(self.detector_repo).modify_detector(_id, new_detector_info)
        self.update_edit_table()
        return modify_res

    def delete_detector_rows(self, rows):
        _id_list = map(lambda r: self.detectors_from_repo[r][detector_id], rows)
        delete_res = DeleteDetectorsCase(self.detector_repo).delete_detectors(_id_list)
        self.update_edit_table()
        return delete_res
