# start_robber.py

import os
import json
import random
import time
from datetime import datetime, timedelta


import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from generate_javascript_code import generate_javascript_code

def open_chrome():
    with open('user_info.json', 'r') as f:
        user_info = json.load(f)

    username_value = user_info["username"]
    password_value = user_info["password"]
    course_names = user_info["course_names"]
    start_rob_time = user_info["start_rob_time"]

    chrome_driver_path = 'chromedriver/chromedriver'
    service = Service(chrome_driver_path)

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
    driver.get(url)

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

    input()

def start_robber():
    with open('user_info.json', 'r') as f:
        user_info = json.load(f)

    username_value = user_info["username"]
    password_value = user_info["password"]
    course_names = user_info["course_names"]
    start_rob_time = user_info["start_rob_time"]

    df_courses = pd.read_csv('courseList.csv')
    javascript_code = generate_javascript_code(course_names, df_courses)



    chrome_driver_path = 'chromedriver/chromedriver'
    service = Service(chrome_driver_path)

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
    driver.get(url)

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

    def task():
        start_time = time.time()
        # 随机sleep 0-0.05秒，防止被拦截

        for _ in range(50):
            driver.execute_script(javascript_code)
            time.sleep(random.uniform(0.02, 0.1))
            print("Execute JS Once in Group 1")

        for _ in range(50):
            driver.execute_script(javascript_code)
            time.sleep(0.1)
            print("Execute JS Once in Group 2")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

        time.sleep(0.1)
        # driver.get(url)

        # save js to javascript_code.js
        # with open('javascript_code.js', 'w') as f:
        #     f.write(javascript_code)
        #     print("JavaScript code has been saved to javascript_code.js.")

        input("Press Enter to close the browser...")

    def wait_until_specified_time(execution_time):
        now = datetime.now()
        next_execution_time = now.replace(hour=execution_time.hour, minute=execution_time.minute, second=0,
                                          microsecond=0)
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

        task()

    if start_rob_time == 'now':
        task()
    else:
        execution_time = datetime.strptime(start_rob_time, "%H:%M").time()
        wait_until_specified_time(execution_time)


