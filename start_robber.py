# start_robber.py

import os
import json
import time
from datetime import datetime, timedelta

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from generate_javascript_code import generate_javascript_code

# 从 user_info.json 读取用户信息
with open('user_info.json', 'r') as f:
    user_info = json.load(f)

username_value = user_info["username"]
password_value = user_info["password"]
course_names = user_info["course_names"]
start_rob_time = user_info["start_rob_time"]

# 读取 courseList.csv 文件
df_courses = pd.read_csv('courseList.csv')

# 根据课程名称生成JavaScript代码
javascript_code = generate_javascript_code(course_names, df_courses)

# 设置ChromeDriver路径
chrome_driver_path = 'chromedriver/chromedriver'  # 确保这个路径是正确的
service = Service(chrome_driver_path)

# 初始化Chrome浏览器
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
driver.get(url)

# 登录操作
username = driver.find_element(By.ID, 'j_username')
password = driver.find_element(By.NAME, 'j_password')
student_radio = driver.find_element(By.ID, 'student')
login_button = driver.find_element(By.XPATH, "//input[@type='image']")

username.send_keys(username_value)
password.send_keys(password_value)
student_radio.click()
login_button.click()

url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
driver.get(url)

# 定义任务
def task(username_value, password_value, course_names, df_courses):
    # start timing
    start_time = time.time()
    # 执行JavaScript代码
    driver.execute_script(javascript_code)

    # stop timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    # 等待页面加载完成
    time.sleep(0.1)

    driver.get(url)

    # 保持浏览器打开一段时间，以便查看结果
    input("Press Enter to close the browser...")

    # 关闭浏览器

# 等待到指定时间执行任务，并打印剩余时间
def wait_until_specified_time(execution_time, username_value, password_value, course_names, df_courses):
    now = datetime.now()
    next_execution_time = now.replace(hour=execution_time.hour, minute=execution_time.minute, second=0, microsecond=0)
    if now >= next_execution_time:
        next_execution_time += timedelta(days=1)

    wait_time = (next_execution_time - now).total_seconds()
    print(
        f"Remaining time until execution: {int(wait_time // 3600)} hours, {int(wait_time % 3600 // 60)} minutes, {int(wait_time % 60)} seconds")

    for _ in range(int(wait_time)):
        time.sleep(1)
        now = datetime.now()
        wait_time = (next_execution_time - now).total_seconds()
        if wait_time <= 0:
            break
        print(
            f"Remaining time until execution: {int(wait_time // 3600)} hours, {int(wait_time % 3600 // 60)} minutes, {int(wait_time % 60)} seconds",
            end='\r')

    task(username_value, password_value, course_names, df_courses)

if __name__ == "__main__":
    # 定义执行任务的时间，例如10:00
    execution_time = datetime.strptime(start_rob_time, "%H:%M").time()

    # 开始等待
    wait_until_specified_time(execution_time, username_value, password_value, course_names, df_courses)
