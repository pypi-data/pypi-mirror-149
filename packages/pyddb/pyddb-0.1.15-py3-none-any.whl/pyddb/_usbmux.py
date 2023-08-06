# -*- coding: utf-8 -*-
# @Time : 2022/4/13 0013 13:05
# @Author : ruomubingfeng
# @File : _usbmux.py
import json
import os
import subprocess
import time


class Device:
    @staticmethod
    def __android_device_list(remote_adb_host=None) -> list:
        android_devices_list = []
        android_dict = {}
        if remote_adb_host:
            shell_str = 'adb -H {} devices'.format(remote_adb_host)
        else:
            shell_str = 'adb devices'
        for device in Shell.invoke(shell_str).splitlines():
            if 'device' in device and 'devices' not in device:
                device = device.split('\t')[0]
                android_dict["ident"] = device
                android_dict["deviceName"] = ADB(device).adb_android_model()
                android_dict["platform"] = ADB(device).adb_platform_name()
                android_devices_list.append(str(android_dict))
        return android_devices_list

    @staticmethod
    def __ios_device_list() -> list:
        ios_list = []
        ios_datas_list = []
        ios_dict = {}
        device_list = []
        result_str = os.popen("tidevice list")
        results = result_str.read().split("\n")
        [ios_datas_list.append(results[result].split(" " * 8)) for result in range(0, len(results))]
        [ios_list.append(ios_data[0].strip().split(" " * 2)) for ios_data in ios_datas_list]
        ios_list.pop()
        ios_list.pop(0)
        for ios_device in range(0, len(ios_list)):
            ios_dict["ident"] = ios_list[ios_device][0]
            ios_dict["deviceName"] = ios_list[ios_device][2]
            ios_dict["platform"] = "iOS"
            device_list.append(str(ios_dict))
        return device_list

    @staticmethod
    def device_info():
        device_info = []
        for device in Device.__android_device_list() + Device.__ios_device_list():
            device_info.append(eval(device))
        return json.dumps(device_info)

    @staticmethod
    def is_platform(ident):
        devices = json.loads(Device.device_info())
        return ''.join([device["platform"] for device in devices if ident == device["ident"]])

    @staticmethod
    def device_ident():
        devices = json.loads(Device.device_info())
        return [device["ident"] for device in devices]

    @staticmethod
    def device_list():
        devices = json.loads(Device.device_info())
        return [device["deviceName"] for device in devices]

    @staticmethod
    def device_sysinfo():
        pass

    @staticmethod
    def device_install():
        pass

    @staticmethod
    def device_uninstall():
        pass

    @staticmethod
    def device_reboot():
        pass

    @staticmethod
    def device_shutdown():
        pass

    @staticmethod
    def device_xctest():
        pass

    @staticmethod
    def device_wdaproxy():
        pass

    @staticmethod
    def device_syslog():
        pass

    @staticmethod
    def device_crashreport():
        pass

    @staticmethod
    def device_perf():
        pass

    @staticmethod
    def device_anr():
        pass

    @staticmethod
    def device_file():
        pass


class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        result = output.decode("utf-8")
        return result


class ADB(object):
    """
      参数:  device_id
    """

    def __init__(self, device_id="", remote_adb_host=None):

        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-s %s" % device_id
        if remote_adb_host:
            self.device_id = '-H {} {}'.format(remote_adb_host, self.device_id)

    def adb(self, args):
        cmd = "%s %s %s" % ('adb', self.device_id, str(args))
        return Shell.invoke(cmd)

    def shell(self, args):
        cmd = "%s %s shell %s" % ('adb', self.device_id, str(args),)
        return Shell.invoke(cmd)

    def adb_android_version(self):
        """
        获取设备中的Android版本号，如4.2.2
        """
        return self.shell(
            "getprop ro.build.version.release").strip()

    def adb_android_model(self):
        """
        获取设备型号
        """
        return self.shell('getprop ro.product.model').strip()

    def adb_platform_name(self):
        """
        获取平台名
        """
        return self.shell("getprop net.bt.name").strip()

    def install_apk(self, file_path):
        self.adb('install {}'.format(file_path))

    def uninstall_apk(self, package):
        self.adb('uninstall {}'.format(package))

    def adb_reboot(self):
        self.adb('reboot')

    def adb_shutdown(self):
        self.adb('reboot -p')

    def adb_anr(self, file_path):
        """adb bugreport > xxx.log Android 8.0"""
        """adb pull /data/anr/ . Android 7.0"""
        android_version = str(self.adb_android_version)
        if android_version < "8.0":
            self.adb_pull('/data/anr/', file_path)
        if android_version >= "8.0":
            self.adb('adb bugreport > {}'.format(file_path))

    def adb_pull(self, phone_path, local_path):
        self.adb('pull {} {}'.format(phone_path, local_path))

    def adb_push(self, local_path, phone_path):
        self.adb('push {} {}'.format(local_path, phone_path))

    def adb_app_list(self):
        """adb shell pm list packages"""
        self.shell('pm list packages')

    def adb_app3_list(self):
        """adb shell pm list packages -3"""
        self.shell('pm list packages -3')

    def adb_app_sys_list(self):
        """	adb shell pm list packages –s"""
        self.shell('pm list packages –s')

    def adb_syslog(self, file_path):
        """adb logcat -v time > xx.txt"""
        self.adb('logcat -v time > {}'.format(file_path))

    def adb_crashreport(self, file_path):
        self.shell('-v time -b crash > {}'.format(file_path))

    def adb_check_package(self):
        """adb shell dumpsys activity |find 'mFocusedActivity' Android 7.0"""
        """adb shell dumpsys activity |find "mResumedActivity" Android 8.0"""
        android_version = str(self.adb_android_version)
        if android_version < "8.0":
            self.shell("dumpsys activity |find 'mFocusedActivity'")
        if android_version >= "8.0":
            self.shell('dumpsys activity |find "mResumedActivity"')

    def adb_screen_shot(self):
        """
        :return: 截图,返回二进制码
        """
        path = os.path.abspath(os.path.dirname(os.getcwd()))
        fail_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        fail_pic = str(fail_time) + "截图.jpg"
        pic_name = os.path.join(path, fail_pic)
        cmd = self.shell('/system/bin/screencap -p /sdcard/screenshot.jpg')
        subprocess.call(cmd, shell=True)
        cmd = self.adb('pull /sdcard/screenshot.jpg {}'.format(pic_name))

        subprocess.call(cmd, shell=True)
        with open(pic_name, 'rb') as r:
            file_info = r.read()
        return file_info


class IOS(object):
    def __init__(self, device_id=""):

        if device_id == "":
            self.device_id = ""
        else:
            self.device_id = "-u %s" % device_id

    def idb(self, args):
        cmd = "%s %s %s" % ('tidevice', self.device_id, str(args))
        return Shell.invoke(cmd)

    def idb_reboot(self):
        self.idb('reboot')

    def idb_shutdown(self):
        self.idb('shutdown')

    def idb_xctest(self):
        self.idb('xctest')

    def idb_wda_proxy(self, package, port):
        self.idb('wdaproxy -B {} --port {}'.format(package, port))

    def idb_syslog(self):
        self.idb('syslog')

    def idb_crashreport(self, path):
        self.idb('crashreport {}'.format(path))

    def idb_perf(self, package):
        self.idb('perf -B {}'.format(package))

    def idb_app_list(self):
        self.idb('applist')

    def idb_sysinfo(self):
        self.idb('sysinfo')

    def idb_info(self):
        self.idb('info')

    def install_ipa(self, package):
        self.idb('install {}'.format(package))

    def uninstall_ipa(self, package):
        self.idb('uninstall {}'.format(package))

    def idb_screen_shot(self, file_name):
        self.idb("screenshot ./{}.png".format(file_name))


if __name__ == '__main__':
    print(Device.device_info())
    print(Device.is_platform("E6E4C20522046784"))
    print(Device.device_list())
    print(Device.device_ident())
    # print(type(ADB("E6E4C20522046784").adb_android_version()))
