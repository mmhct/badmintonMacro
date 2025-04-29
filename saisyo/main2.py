'''简化了时间选择操作'''
import pyautogui
import keyboard
import threading
import time

# 用于阻塞的事件标志
block_event = threading.Event()


# 监听键盘事件解除阻塞
def listen_for_key():
    while True:
        if keyboard.is_pressed('c'):  # 监听按键事件（这里是 'c' 键）
            block_event.set()  # 按键时解除阻塞
            print("按下 'c' 键，解除阻塞！")
            time.sleep(0.5)  # 防止按键事件被触发多次，这里延迟
            continue


# 模拟程序运行中的阻塞
def perform_task():
    print("任务开始，等待解除阻塞...")
    block_event.wait()  # 阻塞，等待解除
    print("阻塞解除，任务继续执行...")
    start = time.time()
    # 继续执行剩余的代码
    pyautogui.click(386, 939)  # 点击5号场地
    point1 = time.time()
    block_event.clear()  # 重置阻塞事件
    block_event.wait()  # 阻塞，等待解除
    point2 = time.time()
    pyautogui.click(29, 83)  # 点击系统浏览器回退键
    '''这里就需要手动操作一下，选择需要抢的场，然后等圈转完（也就是加载完，再按c键）'''
    pyautogui.click(343, 512)  # 点击2号场地,如果要抢其他场地，可以注释掉这行，自己选择c
    point3 = time.time()
    block_event.clear()  # 重置阻塞事件
    block_event.wait()  # 阻塞，等待解除
    point4 = time.time()
    pyautogui.click(2239, 518)  # 点击日期框
    pyautogui.click(1284, 1409)  # 这个是选择下一个月份，如果遇到月份更替就要做这个操作，如果没有更替做这个也没事
    # 这个月份功能还没测试，不知道是否能用，因为选择月份之后可能会有些系统延迟，需要等待一下，等月份更替的时候进行测试
    pyautogui.click(2141, 1409)  # 点击日期栏，其实执行的是选择之后的日期，一般手抢是下滑选择日期
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)
    pyautogui.click(2141, 1409)  # 连续点击以选到最后的日期，这里多点几次也没事，建议先打开一个然后拖到最底
    pyautogui.click(2515, 1095)  # 点击确认键

    '''下面这部分就是抢实际的场了，此处可以参考position.txt里的坐标进行修改'''
    # TODO: 根据position.txt里的坐标进行修改
    time.sleep(0.15)  # 等待一下
    pyautogui.click(133, 624)  # 8-8:30
    pyautogui.click(900, 622)  # 9:30-10
    # pyautogui.click(1155, 624)  # 10-10:30
    # pyautogui.click(1925, 624)  # 11:30-12
    #pyautogui.click(1424, 715)  # 15-15:30
    #pyautogui.click(2174, 720)  # 16:30-17

    # 下面的固定不改
    pyautogui.click(215, 1192)  # 点击使用人数框
    # pyautogui.click(240, 1252)  # 篮球场测试用
    time.sleep(0.15)  # 等待一下
    pyautogui.write("1")  # 输入文本
    pyautogui.click(714, 1245)  # 点击预约
    end = time.time()
    # pyautogui.click(629, 1301) # 篮球场测试用
    print("任务执行完毕，耗时：", end - start)
    print("加载5号场地耗时：", point2 - point1)
    print("点击要抢的场并等待加载完毕耗时：", point4 - point3)


if __name__ == "__main__":
    # 启动监听线程
    threading.Thread(target=listen_for_key, daemon=True).start()  # 监听键盘按键
    perform_task()  # 执行任务
