import hid # 库的名字叫做 HIDAPI 不是HID 也不是USB

for device_dict in hid.enumerate(): # list [dics]
    keys = list(device_dict.keys()) # 取出 dics中的键值
    keys.sort() # 按照键值排序
    for key in keys: #打印出所有字典
        print("%s : %s" % (key, device_dict[key]))
    print()