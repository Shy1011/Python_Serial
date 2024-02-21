try:
    # 尝试执行可能会引发异常的代码块
    result = 10 / 0  # 这里会引发一个除零异常
except:
    # 捕获所有异常
    print("发生异常，执行备用代码")
    result = None  # 或者执行其他操作

# 继续执行其他代码
print("结果：", result)
