#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.manip_case_table import parse_cell_value
from common.check_result import *
from common.comm_paras import g_logger


g_case_input = None
g_case_expt = None


def chk_ota_result(*exp):
    # assert result
    #chk_return_number("m")
    chk_uos_launch(OTA_UOS_DIR)
    chk_ota_version(exp[0])

    # cv process
    g_ssh_slave.exec_cmd(CV_MAIN.replace("uisee*", "uos"))

    time.sleep(5)
    ps_ef_grep("s", exp[1])


def upgrade_os_ota_full():
    # copy version to master host
    vername = g_case_input['os_version']
    verpath = os.path.join(OS_VER_DIR, vername)
    cp_pth_to_ma(verpath, TEST_DIR)

    # slave copy uos_json
    uos_common_path = os.path.join(OS_VER_DIR.replace("os_version", "ota"), "uos_common.json")
    cp_pth_to_sl(uos_common_path, UOS_CFG_DIR)

    copy_map()

    # exec upgrade cmd
    apply_os_ver(vername)

    # remove testdata dir
    rm_ma_dir(TEST_DIR)

    # copy package
    # g_ssh_master.exec_cmd("cp ~/test_ota_package/1224_full/* ~/download_uos/")

    # ota upgrade
    del g_case_input["os_version"]
    do_ota_full(g_case_input)
    # assert result

    chk_ota_result(g_case_expt['version'], g_case_expt["result"])
    # chk_uos_launch(OTA_UOS_DIR)
    # chk_ota_version(g_case_expt['version'])
    #
    # cv process
    # g_ssh_slave.exec_cmd(CV_MAIN.replace("uisee*", "uos"))
    #
    # time.sleep(5)
    # ps_ef_grep("s", g_case_expt["result"])


def upgrade_os_ota():
    # copy version to master host
    vername = g_case_input['os_version']
    verpath = os.path.join(OS_VER_DIR, vername)
    cp_pth_to_ma(verpath, TEST_DIR)

    # exec upgrade cmd
    apply_os_ver(vername)

    # remove testdata dir
    rm_ma_dir(TEST_DIR)
    do_ota_delta()

    del g_case_input["os_version"]
    chk_ota_result(g_case_input["version"], g_case_expt["version"])


def ota_help():
    g_ssh_master.exec_cmd(OTA+"-h")

    chk_result_com("m")


def plantfrom_CQ_ota():
    # ota upgrade
    do_ota_full(g_case_input["plantfrom"])

    # assert result
    chk_ota_result(g_case_input['version'], g_case_expt["result"])


def plantfrom_GG_ota():
    # ota upgrade
    do_ota_full(g_case_input["plantfrom"])

    # assert result
    chk_ota_result(g_case_input['version'], g_case_expt["result"])


def plantfrom_CG_ota():
    # ota upgrade
    do_ota_full(g_case_input["plantfrom"])

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def branch_ota():
    # ota upgrade
    do_ota_full(g_case_input["branch"])

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def download_ota():
    # ota upgrade
    do_ota_full(g_case_input["download_dir"])

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vid_0_mode():
    # ota upgrade
    prepare_ota_full(g_case_input)
    do_ota_delta()

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vid_1_mode():
    # ota upgrade
    prepare_ota_full(g_case_input)
    do_ota_delta()

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def version_low():
    # ota upgrade
    do_ota_full(g_case_input["version"])

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def version_high():
    # ota upgrade
    do_ota_full(g_case_input["version"])

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def cluster_mode():
    # ota upgrade
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def location_name():
    # ota upgrade
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def ota_client_date():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def port_name():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def project_avp():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def server_local():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])

def slave_local():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def username():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vehicle_id_carnum():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vehicle_idmodle_no():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vehicle_idmodle_e200():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vehicle_node_m():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def vehicle_modile_s():
    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def size_disk_less():
    size = home_df_size("m")
    fallocate_file("m", g_case_input["size"], size)

    stdout = g_ssh_master.exec_cmd(OTA)

    # assert result
    chk_keyword_exists(g_case_expt["result"],stdout)


def size_disk_more():
    size = home_df_size("m")
    fallocate_file("m", g_case_expt["size"], size)

    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def size_disk_empty():
    size = home_df_size("m")
    fallocate_file("m", g_case_expt["size"], size)

    stdout = g_ssh_master.exec_cmd(OTA)

    # assert result
    chk_keyword_exists(g_case_expt["result"],stdout)


def size_disk_just():
    size = home_df_size("m")
    fallocate_file("m", g_case_expt["size"], size)

    do_ota_full(g_case_input)

    # assert result
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def mac_address():
    #
    stdout = do_ota_full(g_case_input)

    # assert result
    chk_keyword_exists(g_case_expt["result"], stdout)


def download_data_full():
    ota_comm = "_ota_cli.pyc"
    ota_dir = os.path.join(OTA_DATA_DIR, ota_comm)
    g_ssh_master.upload(ota_dir, HOME_DIR)
    prepare_ota_full(g_case_input)
    g_ssh_master.exec_cmd("python " + ota_comm)

    do_ota_full(g_case_input)
    chk_ota_result(g_case_expt['version'], g_case_expt["result"])


def download_data_delta():
    prepare_ota_full(g_case_input)
    g_ssh_master.exec_cmd(OTA + "-f")




dict_func = {
    "upgrade_os_ota": upgrade_os_ota,
    "upgrade_os_ota_full": upgrade_os_ota_full,
    "ota_help": ota_help,
    "plantfrom_cq_ota": plantfrom_CQ_ota,
    "plantfrom_gg_ota": plantfrom_GG_ota,
    "plantfrom_CG_ota": plantfrom_CG_ota,
    "branch_ota": branch_ota,
    "download_ota": download_ota,
    "vid_0_mode": vid_0_mode,
    "vid_1_mode": vid_1_mode,
    "version_low": version_low,
    "version_high": version_high,
    "cluster_mode": cluster_mode,
    "location_name": location_name,
    "ota-client_date": ota_client_date,
    "port_name": port_name,
    "project_avp": project_avp,
    "server_local": server_local,
    "slave_local": slave_local,
    "username": username,
    "vehicle_id_carnum": vehicle_id_carnum,
    "vehicle_idmodle_no": vehicle_idmodle_no,
    "vehicle_idmodle_e200": vehicle_idmodle_e200,
    "vehicle_node_m": vehicle_node_m,
    "vehicle_modile_s": vehicle_modile_s,
    "size_disk_less": size_disk_less,
    "size_disk_more": size_disk_more,
    "size_disk_empty": size_disk_empty,
    "size_disk_just": size_disk_just,
    "mac_address": mac_address,
    "download_uos_full": download_data_full,
    "download_data_delta": download_data_delta,

}


def run_case(case_name, case_input, case_expt):
    global g_case_input
    global g_case_expt

    g_logger.info(case_name)

    g_case_input = parse_cell_value(case_input)
    g_case_expt = parse_cell_value(case_expt)

    try:
        dict_func[case_name]()
    except TypeError:
        pass

    return True


if __name__ == '__main__':
    pass
