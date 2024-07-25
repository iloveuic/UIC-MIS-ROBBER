# main_menu.py

import os
import json

from get_courses import get_courses
from start_robber import start_robber, open_chrome
from generate_javascript_code import save_js_code

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def get_user_info():
    username = input("请输入学号，如s122212321：")
    password = input("请输入密码：")
    start_rob_time = input("请输入开始选课的24小时制时间，例如15:00：")

    print(
        "输入要加入的课程名称列表，用逗号分开，如 Approaches to Second Language Teaching (1002), Listen and Speak Up (1007)")
    course_names_input = input("你想选的课程是：")
    course_names = [course.strip() for course in course_names_input.split(',')]

    user_info = {
        "username": username,
        "password": password,
        "start_rob_time": start_rob_time,
        "course_names": course_names
    }

    with open('user_info.json', 'w') as f:
        json.dump(user_info, f)

    print("用户信息已保存到 user_info.json")


def display_menu():
    print("菜单选项:")
    print("1: 获取所有课程信息")
    print("2: 开始抢课")
    print("3: 修改用户信息")
    print("4: 输出JavaScript代码")
    print("5: 打开自动控制浏览器")
    print("q: 退出程序")
    choice = input("请选择一个选项: ")
    return choice


def main():
    if not os.path.exists('user_info.json'):
        get_user_info()

    choice = display_menu()

    if choice == '1':
        get_courses()
    elif choice == '2':
        start_robber()
    elif choice == '3':
        get_user_info()
        display_menu()
    elif choice == '4':
        save_js_code()
    elif choice == '5':
        open_chrome()

    elif choice == 'q':
        pass
    else:
        print("无效选项，请重新运行程序。")


if __name__ == "__main__":
    main()