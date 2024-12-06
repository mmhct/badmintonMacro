import pyautogui

print("本台计算机分辨率为：", pyautogui.size(),
      type(pyautogui.size()))  # Size(width=1920, height=1080) <class 'pyautogui.Size'>

# 获取当前鼠标位置
x, y = pyautogui.position()
print("目前光标的位置：", pyautogui.position(),
      type(pyautogui.position()))  # Point(x=842, y=346) <class 'pyautogui.Point'>

# 检查XY是否在允许的分辨率内
print(pyautogui.onScreen(0, 0))  # True
print(pyautogui.onScreen(1920, 1080))
