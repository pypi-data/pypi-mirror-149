# SPDX-FileCopyrightText: 2022 Senne Van Baelen
#
# SPDX-License-Identifier: Apache-2.0

"""
    Tests encoder functionality on step input
"""

import os
import time
import csv
import pathlib
import json
import numpy as np
import rolab_tb.log as logger
from rolab_tb.turtlebot import Turtlebot

LOGGER = logger.get_logger("test", "INFO")

TIME_INTERVAL = 3

D_RES = {
        "description": None,
        "input_lin_vel": 0.22,
        "input_ang_vel": 0,
        "tstart_user": None,
        "tstart_sensor": None,
        "l_time_user": [],
        "l_time_sensor": [],
        "l_ticks_left": [],
        "l_ticks_right": [],
        "l_linvel": [],
        "l_angvel": []
        }

CSV_PATH_BENCHMARK = "./benchmarks/encoders_linvel_step_022_t3.csv"
AVAILABLE_INPUT_BENCHMARKS = [[0.22, 0]]

def write_dict_to_csv(csv_path, d_res, csv_columns=None):

    """ write lists resulting dictionary to csv """

    cwd = os.getcwd()
    csv_path = pathlib.Path(cwd, csv_path)

    if not csv_columns:
        csv_columns = ['l_time_user','l_time_sensor','l_ticks_left',
                       'l_ticks_right', 'l_linvel', 'l_angvel']
    try:
        with open(csv_path, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(csv_columns)
            lists_to_columns = []
            for col_name in csv_columns:
                lists_to_columns.append(d_res[col_name])

            for row in zip(*lists_to_columns):
                writer.writerow(row)

    except IOError as err:
        LOGGER.error("Failed to write to csv file")
        LOGGER.error(err)


def get_dict_from_csv(csv_path):

    """ get dictionary from benchmark CSV file """

    thisfile_path = pathlib.Path(__file__).parent.absolute()
    csv_filepath = pathlib.Path(thisfile_path, csv_path)

    d_benchmark_data = {}
    try:
        with open(csv_filepath, 'rU', encoding='utf-8') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile)
            for row in reader:
                for header, value in row.items():
                    try:
                        d_benchmark_data[header].append(float(value))
                    except KeyError:
                        d_benchmark_data[header] = [float(value)]
    except IOError as err:
        LOGGER.error("Failed to read benchmark csv file")
        LOGGER.error(err)

    return d_benchmark_data


def benchmark_comparison(d_res, csv_path=CSV_PATH_BENCHMARK,
                         check_available_bm=True,
                         print_results=False):

    """ compare result with benchmark """

    # check if benchmark is available
    available = False
    for l_inputs in AVAILABLE_INPUT_BENCHMARKS:
        if d_res['input_lin_vel'] == l_inputs[0] and \
                d_res['input_ang_vel'] == l_inputs[1]:
            available = True
            break

    if not available and check_available_bm:
        LOGGER.warning("A bechmark for inputs {linvel: %s, angvel: %s} is \
not available. Can't perform benchmark tests",
                       d_res['input_lin_vel'],
                       d_res['input_ang_vel'])
        return None, None

    benchmark_cols = ['l_ticks_left', 'l_ticks_right', 'l_linvel',
                     'l_angvel']

    d_benchmark = get_dict_from_csv(csv_path)

    d_benchmark_res = {}
    for colname in benchmark_cols:
        d_benchmark_res[colname] = {}
        interp_res = np.interp(d_benchmark['l_time_sensor'],
                               d_res['l_time_sensor'], d_res[colname])

        # the sum of absolute differences (SAD),
        d_benchmark_res[colname]['SAD'] = np.sum(np.abs(
                                                interp_res -
                                                d_benchmark[colname])
                                                )
        # the sum of squared differences (SSD)
        d_benchmark_res[colname]['SSD'] = np.sum(np.square(
                                                interp_res -
                                                d_benchmark[colname])
                                                )
        # the correlation coefficient
        d_benchmark_res[colname]['corrcoef'] = np.corrcoef(
                                                    interp_res,
                                                    d_benchmark[colname]
                                                    )[0][1]
    if print_results:
        LOGGER.info("Encoder benchmark results for \
{linvel: %s, angvel: %s}:", d_res['input_lin_vel'], d_res['input_ang_vel'])
        LOGGER.info(json.dumps(d_benchmark_res,
                               sort_keys=True, indent=2))

    return d_benchmark, d_benchmark_res


def ticks_to_platform_velocity(d_res, d_tb_conf,
                               user_time=False, init_v=0, init_w=0):

    """ convert encoder ticks to wheel speeds """

    l_time = d_res["l_time_sensor"]

    if user_time:
        l_time = d_res["l_time_user"]

    v_all = [init_v]
    w_all = [init_w]

    for idx, _ in enumerate(l_time[:-1]):
        t_step = l_time[idx+1] - l_time[idx]
        d_enc_l = d_res['l_ticks_left'][idx+1] - \
                    d_res['l_ticks_left'][idx]
        d_enc_r = d_res['l_ticks_right'][idx+1] - \
                    d_res['l_ticks_right'][idx]
        w_l = d_enc_l * d_tb_conf['tick2rad'] / t_step
        w_r = d_enc_r * d_tb_conf['tick2rad'] / t_step

        v_all.append((w_r + w_l) * d_tb_conf['wheel_radius'] / 2)
        w_all.append((w_r - w_l) * d_tb_conf['wheel_radius'] /
                d_tb_conf['wheel_base'])

    d_res['l_linvel'] = v_all
    d_res['l_angvel'] = w_all

    return d_res

def append_vals(d_res, enc_result, keep_duplicates=False):

    """ append sensor reading to lists """

    if not keep_duplicates and len(d_res['l_ticks_left']) > 0:
        if d_res['l_ticks_left'][-1] == enc_result['left'] and \
                d_res['l_ticks_right'][-1] == enc_result['right']:
            return

    d_res['l_time_user'].append(time.time() -
            d_res['tstart_user'])
    d_res['l_time_sensor'].append(enc_result['timestamp'] -
            d_res['tstart_sensor'])
    d_res['l_ticks_left'].append(enc_result['left'])
    d_res['l_ticks_right'].append(enc_result['right'])


def step_input_response(interval=TIME_INTERVAL,
                        tb_config=None, inputs=None,
                        csv_file=None):

    """ test encoders """

    tb_inst = Turtlebot(tb_config)

    tb_config = tb_inst.get_tb_config()

    d_res = D_RES
    d_res['description'] = "step input response based on encoders"

    if inputs:
        d_res['input_lin_vel'] = inputs[0]
        d_res['input_ang_vel'] = inputs[1]

    tb_inst.set_control_inputs(d_res['input_lin_vel'],
                               d_res['input_ang_vel'])

    LOGGER.info("Performing encoder tests through step input:\n\
  - linear velocity: %s [m/s]\n\
  - angular velocity %s [rad/s]\n\
  - over a time interval of %s seconds",
                d_res['input_lin_vel'],
                d_res['input_ang_vel'],
                interval)


    t_start = time.time()
    d_res['tstart_user'] = t_start

    # wait for first enc thick value
    enc_ticks = None
    while True:
        enc_ticks = tb_inst.get_encoder_ticks()
        if enc_ticks:
            break
        time.sleep(0.05)
    d_res['tstart_sensor'] = enc_ticks['timestamp']
    append_vals(d_res, enc_ticks)

    while (time.time() - t_start) < interval:
        tb_inst.get_encoder_ticks()
        append_vals(d_res, tb_inst.get_encoder_ticks())
        time.sleep(0.01)
    tb_inst.stop()

    if not tb_config:
        tb_config = tb_inst.get_tb_config()

    d_res = ticks_to_platform_velocity(d_res, tb_config)

    if csv_file:
        write_dict_to_csv(csv_file, d_res)

    return d_res

def test_encoders(interval=TIME_INTERVAL, tb_config=None, inputs=None,
                  reponse_csv_path=None, check_available_bm=True):

    """ perform benchmark on encoders """

    d_res_step = step_input_response(interval=interval,
                                     tb_config=tb_config,
                                     inputs=inputs,
                                     csv_file=reponse_csv_path)


    d_benchmark, d_benchmark_res = benchmark_comparison(d_res_step,
                                   print_results=True,
                                   check_available_bm=check_available_bm)

    return d_res_step, d_benchmark, d_benchmark_res
