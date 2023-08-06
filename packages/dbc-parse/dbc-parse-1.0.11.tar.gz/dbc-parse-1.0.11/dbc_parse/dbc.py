# -*- coding: utf-8 -*-
# Create Time: 2022/2/13 11:08
# Author: nzj
# Function：
import os
import re
from collections import defaultdict
from typing import Optional, Union


class DBCSignal:
    def __init__(self, sig_name):
        self.real_signal_name: Optional[str] = sig_name
        self.user_define_signal_name: Optional[str] = None
        self.can_name: Optional[str] = None
        self.node_name: Optional[str] = None
        self.msg_name: Optional[str] = None
        self.msg_id: Optional[int] = None
        self.max_value: Optional[float] = 0
        self.min_value: Optional[float] = 0
        self.default_value: Optional[float] = None
        self.factor: Optional[float] = 1
        self.offset: Optional[float] = 0
        self.explanation = None
        self.length_bit: Optional[int] = None
        self.start_bit: Optional[int] = None
        self.value_table: Optional[dict[int, str]] = None  # 保存信号的真值
        self.signal_send_type: Optional[int] = None  # 0-周期报文；1-事件报文


class DBCMessage:
    def __init__(self, msg_name, msg_id):
        self.can_name: Optional[str] = None
        self.node_name: Optional[str] = None
        self.msg_id: int = msg_id
        self.msg_name: str = msg_name
        self.msg_send_type: Optional[int] = None  # 0-周期报文；1-事件报文
        self.msg_cycle_time: Optional[int] = None
        self.signal_list: list[DBCSignal] = []


class DBCCan:
    def __init__(self, can_name):
        self.can_name: str = can_name
        self.message_list: list[DBCMessage] = []


class IDBC:
    """解析DBC文件数据"""

    def __init__(self, DBC_file_path):
        self.DBC_file_path: str = DBC_file_path
        self.can_list: list[DBCCan] = []
        self.replace_signal_list: list[list[str, str]] = []

    def get_file_list(self) -> list[Optional[str]]:
        """根据路径，获得路径下所有.dbc结尾的文件列表

        Returns:
            包含所有以.dbc结尾的文件列表
        """
        dir_files = os.listdir(self.DBC_file_path)
        file_list = []
        for file in dir_files:
            if file.endswith(".dbc"):
                file_list.append(os.path.join(self.DBC_file_path, file))
        if len(file_list) == 0:
            print("{}目录未找到DBC文件".format(self.DBC_file_path))
            return []
        else:
            return file_list

    def get_dbc_src_obj(self):
        f_file_list = self.get_file_list()
        new_pattern = re.compile(r'([A-Z]{4}).dbc', re.DOTALL)
        if f_file_list:
            for f_dbcfile in f_file_list:
                can_name = new_pattern.findall(f_dbcfile)[0]
                f_can_obj = DBCCan(can_name)
                self.can_list.append(f_can_obj)
                if not can_name:
                    print("文件：{}未找到对应的DBC名称".format(f_dbcfile))
                with open(f_dbcfile, "r", encoding='utf-8', errors='ignore') as f:
                    while True:
                        f_line = f.readline()
                        # print(f_line)
                        if not f_line:
                            break
                        if f_line.startswith("BO_ "):
                            f_msg = f_line.split(' ')
                            f_msg_name = f_msg[2].split(':')[0]
                            f_msg_id = hex(int(f_msg[1]))
                            this_msg = DBCMessage(f_msg_name, f_msg_id)
                            this_msg.can_name = can_name
                            this_msg.node_name = f_msg[4][:-1]
                            f_can_obj.message_list.append(this_msg)
                        if f_line.startswith(" SG_ "):
                            f_signal = f_line[1:].split(' ')
                            f_sig_name = f_signal[1]
                            f_start_bit = f_signal[3].split('|')[0]
                            f_length_bit = f_signal[3].split('|')[1].split('@')[0]
                            f_sig_max_value = float(f_signal[5][1:-1].split("|")[1])
                            f_sig_min_value = float(f_signal[5][1:-1].split("|")[0])
                            f_factor = float(f_signal[4][1:-1].split(',')[0])
                            f_offset = float(f_signal[4][1:-1].split(',')[1])
                            if f_sig_max_value < f_sig_min_value:
                                print('[error dbc_file模块-{}信号最大值小于最小值]'.format(f_sig_name))
                            if f_signal[2] == ":":
                                this_sig = DBCSignal(f_sig_name)
                                f_now_msg = f_can_obj.message_list[-1]
                                this_sig.can_name = f_can_obj.can_name
                                this_sig.node_name = f_now_msg.node_name
                                this_sig.msg_id = f_now_msg.msg_id
                                this_sig.msg_name = f_now_msg.msg_name
                                this_sig.max_value = f_sig_max_value
                                this_sig.min_value = f_sig_min_value
                                this_sig.factor = f_factor
                                this_sig.offset = f_offset
                                this_sig.length_bit = int(f_length_bit)
                                this_sig.start_bit = self.get_start_bit(int(f_start_bit))
                                f_now_msg.signal_list.append(this_sig)
                        if f_line.startswith("BA_ \"GenSigStartValue\""):  # 得到信号的默认值
                            f_tokens = f_line.split(' ')
                            f_msg_id = f_tokens[3]
                            f_sig_name = f_tokens[4]
                            f_default_value = f_tokens[5].split(';')[0]
                            f_flag_num = 0
                            for f_msg in f_can_obj.message_list:
                                if eval(f_msg.msg_id) == eval(f_msg_id):
                                    for f_sig in f_msg.signal_list:
                                        if f_sig.real_signal_name == f_sig_name:
                                            f_sig.default_value = float(f_default_value) * f_sig.factor + f_sig.offset
                                            f_flag_num += 1
                                            break
                                    if f_flag_num == 1:
                                        break
                            if f_flag_num == 0:
                                print("dbc_file error:查找信号默认值，该默认值下未找到{0}信号".format(f_sig_name))
                        if f_line.startswith("BA_ \"SystemSignalLongSymbol\""):
                            replace_signal = f_line.split(' ')[4]
                            new_name_signal = f_line.split(' ')[5][1:-3]
                            self.replace_signal_list.append([replace_signal, new_name_signal])

                        if f_line.startswith("BA_ \"GenMsgSendType\" BO_"):
                            f_signal_id = hex(int(f_line.split(' ')[3]))
                            f_msg_send_type = f_line.split(' ')[4][:-2]
                            for f_msg in f_can_obj.message_list:
                                if f_signal_id == f_msg.msg_id:
                                    f_msg.msg_send_type = int(f_msg_send_type)
                                    for f_signal in f_msg.signal_list:
                                        f_signal.signal_send_type = int(f_msg_send_type)

                        if f_line.startswith("BA_ \"GenMsgCycleTime\" BO_"):
                            f_signal_id = hex(int(f_line.split(' ')[3]))
                            f_msg_cycle_time = f_line.split(' ')[4][:-2]
                            for f_msg in f_can_obj.message_list:
                                if f_signal_id == f_msg.msg_id:
                                    f_msg.msg_cycle_time = int(f_msg_cycle_time)

                        if f_line.startswith('VAL_ '):
                            all_content_list = f_line.split(' ')
                            signal_id = hex(int(all_content_list[1]))
                            signal_real_name = all_content_list[2]
                            signal_value_table_pattern = re.compile(r'(\d+)\s*["]\s*([^"]+)["]*', re.DOTALL)
                            find_lists = signal_value_table_pattern.findall(f_line)
                            for f_msg in f_can_obj.message_list:
                                if signal_id == f_msg.msg_id:
                                    for f_signal in f_msg.signal_list:
                                        if f_signal.real_signal_name == signal_real_name:
                                            f_signal.value_table = {int(signal_value): signal_explaination
                                                                    for signal_value, signal_explaination in find_lists}
                                            break

            self.replace_dbc_signal()

    def replace_dbc_signal(self):
        """将要替换的旧的信号名称替换为新的信号名称"""
        for f_replace_sig_list in self.replace_signal_list:
            f_old_sig_name = f_replace_sig_list[0]
            f_new_sig_name = f_replace_sig_list[1]
            for f_can in self.can_list:
                for f_msg in f_can.message_list:
                    for f_sig in f_msg.signal_list:
                        if f_sig.real_signal_name == f_old_sig_name:
                            f_sig.real_signal_name = f_new_sig_name

    @staticmethod
    def get_start_bit(inter_start_bit):
        int_value = inter_start_bit // 8
        remind_value = (inter_start_bit - int_value * 8) % 8
        return 7 - remind_value + 8 * int_value

    def get_all_signals(self) -> dict[str, list[DBCSignal]]:
        """获取当前DBC中所有signal属性

        Returns:
            返回以signal真实名为key，DBC中所有有这个signal的报文等的属性信息列表为key的dict

        """
        return_dic: dict[str, list[DBCSignal]] = defaultdict(list)
        for f_can in self.can_list:
            for f_msg in f_can.message_list:
                for f_sig in f_msg.signal_list:
                    return_dic[f_sig.real_signal_name].append(f_sig)
        return return_dic

    def judge_message_bit_is_not_conflict(self):
        """该条暂不适用，目前存在复用帧报文情况-会根据第一个字节的值来判断怎么解析后7个字节的内容"""
        for f_can in self.can_list:
            for f_msg in f_can.message_list:
                msg_bit_list = []
                try:
                    for f_sig in f_msg.signal_list:
                        f_sig_value_range = list(range(f_sig.start_bit, f_sig.start_bit + f_sig.length_bit))
                        for one_value in f_sig_value_range:
                            if one_value in msg_bit_list:
                                print(f"{f_sig.real_signal_name} - [{f_sig.can_name}][{f_sig.msg_name}] 位信息定义错误，请核对")
                                raise ValueError()
                        msg_bit_list += f_sig_value_range
                except ValueError:
                    pass


if __name__ == "__main__":
    DBC_file = r"D:\canoe_project\canoe_project\tbox_project\vehicle_data\A13\dbc"
    dbc_obj = IDBC(DBC_file)
    dbc_obj.get_dbc_src_obj()
    dbc_obj.judge_message_bit_is_not_conflict()

    print('')
