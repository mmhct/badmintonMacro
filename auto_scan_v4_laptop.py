

import datetime

import pyautogui
import time
from auto_scan_laptop import run_lap
from scan_wait import run2
from scan_back_fault import run_back_fault
from scan_loading import run_loading
from scan_fail import run_scan_fail
from scan_if_still_verifying import run_if_still_verifying


def perform_task(have, iter):
    pre_have = have.copy()
    start = time.time()
    # 继续执行剩余的代码
    pyautogui.click(x=354, y=298)  # 点击5号场地
    time.sleep(0.2)  # 等待一下,要不然有可能连‘加载中’都还没显示出来
    while run_loading():  # 加载中，检测‘暂无数据’
        continue
    # 使用cv2识别是否处于等待响应状态(这个到底可不可以优化？2024/12/19回答：不能优化，因为不解决等待框，下面点击球场的动作无法实现且会被屏蔽，
    # 点击会变成无效点击，导致乱序，第一个抢场操作就会失败，但不会影响第二次迭代的抢场)
    while run2():
        continue
    # time.sleep(1.5)  # 等待一下，这里必须考虑来自服务器的延迟(这个到底可不可以优化？)
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    time.sleep(0.1)  # 等待一下，要不然有可能连‘加载中’都还没显示出来
    while run_loading():  # 加载中，检测‘暂无数据’
        continue
    if run_back_fault():  # 回退过多
        pyautogui.click(659, 708)  # 点击润扬羽毛球场

    if iter == 0:
        pyautogui.click(x=367, y=503)  # 点击2号场地
        # pyautogui.click(361, 708)  # 点击1号场地
    elif iter == 1:
        pyautogui.click(383, 924)  # 点击7号场地
    elif iter == 2:
        pyautogui.click(x=367, y=503)  # 点击2号场地
    elif iter == 3:
        pyautogui.click(x=368, y=1140)  # 点击9号场地

    # 使用cv2识别是否处于等待响应状态
    while run_loading():  # 加载中
        continue
    while run2():
        continue
    time.sleep(0.2)  # 可考虑减小的优化空间
    pyautogui.click(2239, 545)  # 点击日期框
    time.sleep(0.15)  # 等待一下
    # pyautogui.click(1284, 1409)  # 这个是选择下一个月份，如果遇到月份更替就要做这个操作，如果没有更替做这个也没事
    # pyautogui.click(429, 1409)  # 这个是选择下一个年份，如果遇到年份更替就要做这个操作，如果没有更替做这个也没事
    time.sleep(0.15)  # 等待一下,如果没有月份或年份更替就不用等待
    # 这个月份功能还没测试，不知道是否能用，因为选择月份之后可能会有些系统延迟，需要等待一下，等月份更替的时候进行测试
    pyautogui.click(2141, 1409)  # 点击日期栏，其实执行的是选择之后的日期，一般手抢是下滑选择日期
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)  # 连续点击以选到最后的日期，这里多点几次也没事，建议先打开一个然后拖到最底
    time.sleep(0.15)  # 等待一下
    pyautogui.click(2515, 1095)  # 点击确认键

    '''下面这部分就是抢实际的场了，程序会自动识别可抢的场地，并按照自定义优先规则进行选择，越靠后优先级越低'''
    '''v3.5 允许连续抢场，自动去重'''
    # TODO: 根据position.txt里的坐标进行修改
    time.sleep(0.25)  # 等待一下,如果这里还要强行优化，那就识别蒙上一层黑雾的图片
    detection_results = run_lap()
    detection_results = {key: not value for key, value in detection_results.items()}
    # TODO:晚场可以优化，iter=0时可抢
    if (detection_results[14] and detection_results[17]) and (
            14 not in have and 15 not in have and 16 not in have and 17 not in have):
        pyautogui.click(1163, 735)  # 15-15:30
        pyautogui.click(1922, 740)  # 16:30-17
        have.append(14)
        have.append(15)
        have.append(16)
        have.append(17)
    elif (detection_results[15] and detection_results[18]) and (
            15 not in have and 16 not in have and 17 not in have and 18 not in have):
        pyautogui.click(1399, 744)  # 15:30-16
        pyautogui.click(2156, 740)  # 17-17:30
        have.append(15)
        have.append(16)
        have.append(17)
        have.append(18)
    elif (detection_results[16] and detection_results[19]) and (
            16 not in have and 17 not in have and 18 not in have and 19 not in have):
        pyautogui.click(1662, 742)  # 16-16:30
        pyautogui.click(2418, 742)  # 17:30-18
        have.append(16)
        have.append(17)
        have.append(18)
        have.append(19)
    elif (detection_results[12] and detection_results[15]) and (
            12 not in have and 13 not in have and 14 not in have and 15 not in have):
        pyautogui.click(642, 742)  # 14-14:30
        pyautogui.click(1399, 744)  # 15:30-16
        have.append(12)
        have.append(13)
        have.append(14)
        have.append(15)
    elif (detection_results[13] and detection_results[16]) and (
            13 not in have and 14 not in have and 15 not in have and 16 not in have):
        pyautogui.click(905, 741)  # 14:30-15
        pyautogui.click(1662, 742)  # 16-16:30
        have.append(13)
        have.append(14)
        have.append(15)
        have.append(16)
    # elif (detection_results[12] and detection_results[13]) and (
    #         12 not in have and 13 not in have):  # 14-15一小时，仅周四用
    #     pyautogui.click(642, 722)  # 14-14:30
    #     pyautogui.click(905, 721)  # 14:30-15
    #     have.append(12)
    #     have.append(13)
    elif (detection_results[3] and detection_results[6]) and (
            3 not in have and 4 not in have and 5 not in have and 6 not in have):
        pyautogui.click(900, 642)  # 9:30-10
        pyautogui.click(1657, 647)  # 11-11:30
        have.append(3)
        have.append(4)
        have.append(5)
        have.append(6)
    # 更多自定义规则可以在这里添加
    elif (detection_results[2] and detection_results[5]) and (
            2 not in have and 3 not in have and 4 not in have and 5 not in have):
        pyautogui.click(668, 644)  # 9-9:30
        pyautogui.click(1421, 638)  # 10:30-11
        have.append(2)
        have.append(3)
        have.append(4)
        have.append(5)
    # pyautogui.click(133, 624)  # 8-8:30
    # pyautogui.click(900, 622)  # 9:30-10
    elif (detection_results[4] and detection_results[7]) and (
            4 not in have and 5 not in have and 6 not in have and 7 not in have):
        pyautogui.click(1155, 644)  # 10-10:30
        pyautogui.click(1925, 644)  # 11:30-12
        have.append(4)
        have.append(5)
        have.append(6)
        have.append(7)
    elif (detection_results[1] and detection_results[4]) and (
            1 not in have and 2 not in have and 3 not in have and 4 not in have):
        pyautogui.click(1421, 638)  # 10:30-11
        pyautogui.click(1925, 644)  # 11:30-12
        have.append(5)
        have.append(6)
        have.append(7)
    elif (detection_results[0] and detection_results[3]) and (
            0 not in have and 1 not in have and 2 not in have and 3 not in have):  # 啥也没剩，我打早八
        pyautogui.click(146, 644)  # 8-8:30
        pyautogui.click(900, 642)  # 9:30-10
        have.append(0)
        have.append(1)
        have.append(2)
        have.append(3)

    # elif (detection_results[0] and detection_results[1]) and (
    #         0 not in have and 1 not in have) :  # 啥也没剩，我打早八,但是这个8-9太过短暂，不适合
    #     pyautogui.click(146, 624)  # 8-8:30
    #     pyautogui.click(407, 624)  # 8:30-9
    #     have.append(0)
    #     have.append(1)

    else:  # 完全没场地了，或者没落进任何规则当中，执行一步后退操作
        # 可以再设计一个从22点往前找是否存在一个连续一小时的没在have里的场，如果有就订
        pyautogui.click(29, 83)  # 点击系统浏览器回退键
        # pyautogui.click(29, 83)  # 测试fault，正常运行要删掉
        while run_loading():  # 加载中
            continue
        if run_back_fault():  # 回退过多
            pyautogui.click(659, 708)  # 点击润扬羽毛球场
        return have  # 这里结束本次迭代

    # 下面的固定不改
    pyautogui.click(215, 1127)  # 点击使用人数框
    # pyautogui.click(240, 1252)  # 篮球场测试用
    time.sleep(0.15)  # 等待一下
    pyautogui.write("1")  # 输入文本
    pyautogui.click(714, 1189)  # 点击预约
    end = time.time()
    print("任务执行完毕，耗时：", end - start)
    # pyautogui.click(629, 1301) # 篮球场测试用
    time.sleep(3) # 等待一下，这里的等待时间必须大于点击预约按钮之后出现验证码的时间
    while run_if_still_verifying():  # 检测是否还处于验证状态
        continue
    time.sleep(0.3)  # 等待一下,这里是考虑到验证码消失的时间
    while run2():
        continue
    time.sleep(0.1)
    if run_scan_fail():  # 预约失败
        have = pre_have
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    pyautogui.click(29, 83)  # 点击系统浏览器回退键,要点两次，因为点一次是回退到场地界面，再点一次是回退到主界面
    while run_loading():  # 加载中
        continue
    if run_back_fault():  # 回退过多
        pyautogui.click(659, 708)  # 点击润扬羽毛球场
    return have


if __name__ == "__main__":
    set_time = datetime.datetime.strptime("2025-2-17 21:44:30", "%Y-%m-%d %H:%M:%S")
    time_difference = (set_time - datetime.datetime.now()).total_seconds()
    while time_difference > 0:
        if time_difference > 10:
            time.sleep(5)
        else:
            time.sleep(0.1)
        time_difference = (set_time - datetime.datetime.now()).total_seconds()
    have = []
    time.sleep(0.1)  # 等待一下
    for i in range(1): # 还没做回首页的下滑操作，所以只能抢一个场
        have = perform_task(have, i)  # 执行任务
