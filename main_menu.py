# main_menu.py

import os
import json


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
    print("4: 退出程序")
    choice = input("请选择一个选项: ")
    return choice


def main():
    if not os.path.exists('user_info.json'):
        get_user_info()

    choice = display_menu()

    if choice == '1':
        os.system('python get_courses.py')
    elif choice == '2':
        os.system('python start_robber.py')
    elif choice == '3':
        get_user_info()
        display_menu()
    elif choice == '4':
        pass
    else:
        print("无效选项，请重新运行程序。")


if __name__ == "__main__":
    main()