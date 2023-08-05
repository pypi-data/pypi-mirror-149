"""
    SPDX-FileCopyrightText: 2022 Senne Van Baelen
    SPDX-License-Identifier: Apache-2.0

    Turtlebot class for connecting to a ROS bridge

    Author(s):    Senne Van Baelen
    Contact:      senne.vanbaelen@kuleuven.be
    Date created: 2021-02-14

    TODO:
        - should probably implement <https://stackoverflow.com/a/52301233>
"""

# import sys
import os
import signal
import time
import json
# import traceback
import asyncio
# from enum import Enum
import threading
import logging
# import sqlite3
import pathlib
import numpy as np
import websockets
import rolab_tb.log as logger

#=====================================================================
# Configs
#=====================================================================

TB_LIMIT_LIN_VEL = 0.22         # m/s
# TB_LIMIT_ANG_VEL = 2.84         # rad/s (as advertised)
TB_LIMIT_ANG_VEL = 2.5          # rad/s (new bots have issues with adv. max)

# <https://github.com/ROBOTIS-GIT/OpenCR/blob/master/arduino/opencr_arduino/opencr/libraries/turtlebot3/examples/turtlebot3_burger/turtlebot3_core/turtlebot3_core_config.h#L64>
TB_TICK_TO_RAD = 0.001533981

CHANGE_ANG_VEL_DIR = False

D_CONFIG_DEFAULT = {
        "ws_host": "10.42.0.1",
        "ws_port": 9090,
        "log_level": "INFO",
        "logfile": None,
        "msg-sub-dir": "msgs/sub/",
        "msg-pub-dir": "msgs/pub/",
        # list of msg keys to ignore in stream validation validation
        "sub-msgs-ignore-check": [],
        # "sqlite-sensor-uri": "file:mem-sensor?mode=memory&cache=shared",
        # "sqlite-control-uri": "file:mem-control?mode=memory&cache=shared",
        }

D_TB_CONFIG = {
        "tick2rad": 0.001533981,
        "wheel_radius": 0.033,
        "wheel_base": 0.178,
        "max_lin_vel": TB_LIMIT_LIN_VEL,
        "max_ang_vel": TB_LIMIT_ANG_VEL,
        }

LOGGER = logger.get_logger("root", "INFO")

# data structure to be shared between threads
D_SHARED_DATA = {
        "sensor": {
            "msgs": {}
            },
        "input": {
            "linvel": 0,
            "angvel": 0
            }
        }

# class StatusMainProcess(Enum):

    # """ status codes """

    # RUNNING = 1
    # WARNING = 2
    # ERROR = 3

# class StatusSensorMsgs(Enum):

    # """ status codes """

    # INITIALISING = 0
    # REQUESTED = 1
    # SUBSCRIBED = 2
    # ERROR = 3

#=====================================================================
# General methods
#=====================================================================

def kill_all_threads():

    """ kill all treads """

    if os.name == 'nt':
        # pylint: disable=protected-access
        os._exit()
    else:
        os.kill(os.getpid(), signal.SIGINT)


def quaternion_to_euler_angle_vectorized(q_w, q_x, q_y, q_z):

    """ convert IMU quaternion to euler angles (roll pitch yaw) """

    ysqr = q_y * q_y

    intm_0 = +2.0 * (q_w * q_x + q_y * q_z)
    intm_1 = +1.0 - 2.0 * (q_x * q_x + ysqr)
    x_euler = np.degrees(np.arctan2(intm_0, intm_1))

    intm_2 = +2.0 * (q_w * q_y - q_z * q_x)
    intm_2 = np.where(intm_2>+1.0,+1.0,intm_2)
    #t2 = +1.0 if t2 > +1.0 else t2

    intm_2 = np.where(intm_2<-1.0, -1.0, intm_2)
    #t2 = -1.0 if t2 < -1.0 else t2
    y_euler = np.degrees(np.arcsin(intm_2))

    intm_3 = +2.0 * (q_w * q_z + q_x * q_y)
    intm_4 = +1.0 - 2.0 * (ysqr + q_z * q_z)
    if CHANGE_ANG_VEL_DIR:
        z_euler = -np.degrees(np.arctan2(intm_3, intm_4))
    else:
        z_euler = np.degrees(np.arctan2(intm_3, intm_4))

    return x_euler, y_euler, z_euler


async def update_sensor_readings(ws_uri, subscribe_msgs, shared_data):

    """ async event loop for obtaining sensor data """

    data_lock = threading.Lock()

    try:
        async with websockets.connect(ws_uri) as websocket:
            for topic in subscribe_msgs:
                send_msg = json.dumps(subscribe_msgs[topic])
                await websocket.send(send_msg)

            while True:
                d_data = json.loads(await websocket.recv())
                with data_lock:
                    # return message a string (for educational purposes)
                    shared_data['sensor']['msgs'][d_data['topic']] = \
                            json.dumps(d_data['msg'])
    except (ConnectionRefusedError, OSError,
            asyncio.exceptions.TimeoutError) as err:
        LOGGER.error("failed to connect to websocket server at %s", ws_uri)
        LOGGER.error(err)
        LOGGER.info("Make sure the Turlebot (+ websocket bridge) is running")
        LOGGER.info("Exiting...")
        kill_all_threads()


async def send_control_inputs(ws_uri, msgs, shared_data):

    """ async event loop for sending control inputs """

    cmd_vel_template = msgs['cmd_vel']

    try:
        async with websockets.connect(ws_uri) as websocket:
            for topic in msgs:
                keys = ['op', 'type', 'topic']
                adv_msg = {x:msgs[topic][x] for x in keys}
                adv_msg['op'] = "advertise"
                send_msg = json.dumps(adv_msg)
                await websocket.send(send_msg)
            previous_input = shared_data['input']
            while True:
                # check and send at max (theoretical) freq of 20Hz
                last_input = shared_data['input']
                if last_input['linvel'] == previous_input['linvel'] and \
                   last_input['angvel'] == previous_input['angvel']:
                    # await asyncio.sleep(0.05)
                    time.sleep(0.05)
                    continue
                cmd_vel_template['msg']['linear']['x'] = \
                        last_input['linvel']
                cmd_vel_template['msg']['angular']['z'] = \
                        last_input['angvel']
                previous_input = last_input
                # <https://github.com/aaugustin/websockets/issues/865>
                cmd_vel_msg = json.dumps(cmd_vel_template)
                await websocket.send(cmd_vel_msg)
                # await asyncio.sleep(0)
                time.sleep(0.05)

    except (ConnectionRefusedError, OSError,
            asyncio.exceptions.TimeoutError) as err:
        LOGGER.error("failed to connect to websocket server at %s", ws_uri)
        LOGGER.error(err)
        LOGGER.info("Make sure the Turlebot (+ websocket bridge) is running")
        LOGGER.info("Exiting...")
        kill_all_threads()


def get_json_msgs(subdir, json_sub_msgs=None):

    """ collect subscribe messages from json files """

    # resolve subdir relative to this file directory
    fpath = pathlib.Path(__file__).parent.resolve()
    subdir_abs = pathlib.Path(fpath, subdir)

    if not json_sub_msgs:
        json_sub_msgs = {}

    pathlist = pathlib.Path(subdir_abs).glob('*.json')
    for path in pathlist:
        filename = path.stem
        with open(str(path), encoding='utf-8') as json_file:
            data = json.load(json_file)
            json_sub_msgs[filename] = data

    return json_sub_msgs


def loop_in_thread(ws_uri, msgs, d_data):

    """ asyncio loop in separate thread """

    first_key = next(iter(msgs))

    if 'op' in msgs[first_key]:
        if msgs[first_key]['op'] == "subscribe":
            event_loop_sub = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop_sub)
            event_loop_sub.run_until_complete(
                    update_sensor_readings(ws_uri, msgs, d_data))
        elif msgs[first_key]['op'] == "publish":
            event_loop_pub = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop_pub)
            event_loop_pub.run_until_complete(
                    send_control_inputs(ws_uri, msgs, d_data))
        else:
            LOGGER.error("operation '%s' not recognised",
                         str(msgs[first_key]['op']))

    else:
        LOGGER.error("failed to initiate thread since messages do not \
contain an operation type (op)")


#=====================================================================
# Main class
#=====================================================================

class Turtlebot():

    """ Turtlebot base class """

    def __init__(self, d_user_config=None, d_tb_config=None, clogger=LOGGER):

        """ turtlebot constructor, and the defaut config will be merged with
            the config dict argument, to avoid unset values
        """

        self._config = D_CONFIG_DEFAULT
        self._tb_config = D_TB_CONFIG
        self._pose = {
                "init_from_tb_odom": {
                    "x": None,
                    "y": None,
                    "th": None
                    },
                "current_from_tb_odom": {
                    "x": None,
                    "y": None,
                    "th": None
                    }
                }
        if d_user_config:
            self._config = {**self._config, **d_user_config}
        if d_tb_config:
            self._tb_config = {**self._tb_config, **d_tb_config}

        self._config['sub-msgs'] = \
                get_json_msgs(self._config['msg-sub-dir'])
        self._config['pub-msgs'] = \
                get_json_msgs(self._config['msg-pub-dir'])

        self._config['ws_uri'] = "ws://" + self._config['ws_host'] + ":" + \
                str(self._config['ws_port'])

        # in-memory DB
        # <https://docs.python.org/3/library/sqlite3.html>
        # <https://stackoverflow.com/a/3172950>
        # <https://charlesleifer.com/blog/going-fast-with-sqlite-and-python/>

        self.__configure(clogger)
        self.__create_sensor_listener_tread()
        self.__create_control_thread()
        self.__await_sensor_stream()
        self.set_control_inputs(0,0)

    def __configure(self, clogger):

        """ general configurations """

        if not clogger:
            self._clogger = logging.getLogger("root")
        else:
            self._clogger = clogger

        clogger.setLevel(self._config['log_level'])
        if self._config['logfile']:
            self._clogger = logger.get_logger("root",
                                                 self._config['log_level'],
                                                 self._config['logfile'])

    def __create_sensor_listener_tread(self):

        thread = threading.Thread(target=loop_in_thread,
                                  args=(self._config['ws_uri'],
                                        self._config['sub-msgs'],
                                        D_SHARED_DATA))

        thread.daemon = True
        thread.start()

    def __create_control_thread(self):

        thread = threading.Thread(target=loop_in_thread,
                                 args=(self._config['ws_uri'],
                                 self._config['pub-msgs'],
                                 D_SHARED_DATA))

        thread.daemon = True
        thread.start()

    def __await_sensor_stream(self, sleep=0.05, timeout=5):

        """ Wait until turtlebot is accepting sensor data and ready to
            send message to the ROS bridge """

        self._clogger.info("initialising sensor stream...")

        if len(self._config['sub-msgs-ignore-check']) == \
                len(self._config['sub-msgs']):
            # sleep to check connection without any msg validation
            conn_timeout = 1
            time.sleep(conn_timeout)

        for topic in self._config['sub-msgs']:
            if self._config['sub-msgs-ignore-check']:
                if topic in self._config['sub-msgs-ignore-check']:
                    continue
            t_start = time.time()
            while True:
                if time.time() - t_start > timeout:
                    self._clogger.warning("Timeout reached when trying to get \
data from topic '%s'. Got 'None', which will likely propagate to \
API 'getters' related to this topic", topic)
                    break
                # query = f"SELECT msg FROM sensor_readings WHERE topic \
# == '{topic}' ORDER BY rowid DESC LIMIT 1;"
                # res = db_query_select(self.db_con_sensor, query,
                                      # as_json=True,
                                      # print_warnings=False)
                res = None
                try:
                    res = json.loads(D_SHARED_DATA['sensor']['msgs'][topic])
                except KeyError:
                    pass
                if res:
                    if topic == "odom":
                        orientation = res['pose']['pose']['orientation']
                        _, _, z_eul = \
                                quaternion_to_euler_angle_vectorized(
                                        float(orientation['w']),
                                        float(orientation['x']),
                                        float(orientation['y']),
                                        float(orientation['z']))
                        self._pose['init_from_tb_odom']['x'] = \
                            res['pose']['pose']['position']['x']
                        self._pose['init_from_tb_odom']['y'] = \
                            res['pose']['pose']['position']['y']
                        self._pose['init_from_tb_odom']['th'] = z_eul

                    break
                time.sleep(sleep)

        self._clogger.info("Go!")

    def __check_control_limits(self, lin_vel, ang_vel,
                               lin_vel_max=TB_LIMIT_LIN_VEL,
                               ang_vel_max=TB_LIMIT_ANG_VEL):

        """ check control limits """

        # some bots seem to have issues with their exact limits, and setting
        # them to numpy values seems to work, thats why ">" becomes ">=",
        # and 0.9999 is added
        if np.abs(lin_vel) >= lin_vel_max:
            if np.abs(lin_vel) > lin_vel_max:
                self._clogger.warning("linear velocity control limit exceeded \
(%s m/s). Setting to maximum...", lin_vel_max)
            lin_vel = 0.9999*np.sign(lin_vel)*lin_vel_max
        if np.abs(ang_vel) >= ang_vel_max:
            if np.abs(ang_vel) > ang_vel_max:
                self._clogger.warning("angular velocity control limit exceeded \
(%s rad/s). Setting to maximum...", ang_vel_max)
            ang_vel = 0.9999*np.sign(ang_vel)*ang_vel_max

        return lin_vel, ang_vel

    def get_tb_config(self):

        """ returns turtlebot configuration dictionary
        """

        return self._tb_config

    def get_tick_to_rad(self):

        """ returns tick to radians conversion factor
        """

        return self._tb_config['tick2rad']

    def get_imu(self, topic="imu"):

        """ get IMU sensor reading
           <http://docs.ros.org/en/lunar/api/sensor_msgs/html/msg/Imu.html>
        """

        if topic in D_SHARED_DATA['sensor']['msgs']:
            return D_SHARED_DATA['sensor']['msgs'][topic]

        self._clogger.warning("get_imu returned None")

        return None

    def get_imu_angle(self):

        """ get IMU euler angle in degrees """

        d_res = None
        if 'imu' in D_SHARED_DATA['sensor']['msgs']:
            d_res = json.loads(D_SHARED_DATA['sensor']['msgs']['imu'])

        if d_res:
            _, _, z_eul = quaternion_to_euler_angle_vectorized(
                    float(d_res['orientation']['w']),
                    float(d_res['orientation']['x']),
                    float(d_res['orientation']['y']),
                    float(d_res['orientation']['z']))
            return z_eul

        self._clogger.warning("failed to derive IMU angle from quaternion")
        self._clogger.warning("get_imu_angle returned None")

        return None

    def get_sensor_state(self, topic="sensor_state"):

        """ get current sensor state reading """

        if topic in D_SHARED_DATA['sensor']['msgs']:
            return D_SHARED_DATA['sensor']['msgs'][topic]

        self._clogger.warning("get_sensor_state returned None")

        return None

    def get_odom(self, topic="odom"):

        """ get current sensor state reading """

        if topic in D_SHARED_DATA['sensor']['msgs']:
            return D_SHARED_DATA['sensor']['msgs'][topic]

        self._clogger.warning("get_odom returned None")

        return None

    def get_pose_from_odom(self, topic="odom"):

        """ get current built-in odometry computation, corrected based on
            starting point """

        odom_res = None
        if topic in D_SHARED_DATA['sensor']['msgs']:
            odom_res = json.loads(self.get_odom(topic=topic))
        if not odom_res:
            self._clogger.warning("No odometry data avaialble")
            self._clogger.warning("get_pose_from_odom returned None")
            return None

        th_cur = self.get_imu_angle()
        th_init = self._pose['init_from_tb_odom']['th']
        pos = odom_res['pose']['pose']['position']

        self._pose['current_from_tb_odom']['x'] = pos['x'] - \
                self._pose['init_from_tb_odom']['x']
        self._pose['current_from_tb_odom']['y'] = pos['y'] - \
                self._pose['init_from_tb_odom']['y']
        theta = th_cur - th_init
        theta = (theta + 180) % 360 - 180
        # theta = theta/180*np.pi
        self._pose['current_from_tb_odom']['th'] = theta
        # alternative:
               # np.arctan2(np.sin(th_cur - th_init ),
                          # np.cos(th_cur - th_init))

        return self._pose['current_from_tb_odom']

    def get_scan(self, topic="scan"):

        """ get current lidar scan reading """

        if topic in D_SHARED_DATA['sensor']['msgs']:
            return D_SHARED_DATA['sensor']['msgs'][topic]

        self._clogger.warning("get_scan returned None")

        return None

    def get_encoder_ticks(self):

        """ derive encoder thicks from sensor state """

        res_ss = self.get_sensor_state()

        if res_ss:
            d_sensor_state = json.loads(res_ss)

            res = {"left": d_sensor_state['left_encoder'],
                   "right": d_sensor_state['right_encoder'],
                   "timestamp":  d_sensor_state['header']['stamp']['sec'] + \
                                 d_sensor_state['header']['stamp']['nanosec']/10**9
                   }
            return res

        self._clogger.warning("No sensor_state data availabe for \
getting encoder thicks")
        self._clogger.warning("get_encoder_ticks returned None")

        return None

    def set_control_inputs(self, lin_vel, ang_vel):

        """ set control inputs (in database) """

        lin_vel, ang_vel = self.__check_control_limits(lin_vel, ang_vel)

        if CHANGE_ANG_VEL_DIR:
            ang_vel = -ang_vel

        data_lock = threading.Lock()
        with data_lock:
            D_SHARED_DATA['input'] = {"linvel": float(lin_vel),
                                      "angvel": float(ang_vel)}

    def stop(self):

        """ Set robot input back to zero """

        self.set_control_inputs(0,0)
        # sleep to avoid user-program ending _before_ commands are sent
        time.sleep(0.2)

    # def stop(self):

        # """ @deprecated
            # close connections and threads (brute force) """

        # self.set_control_inputs(0,0)
        # self._clogger.info("closing all connections, exiting gracefully.")
        # self._clogger.info("Wait for it...")
        # time.sleep(1)
        # self._clogger.info("Bye!")
        # sys.exit()
