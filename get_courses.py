# get_courses.py

import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 从 user_info.json 读取用户信息
with open('user_info.json', 'r') as f:
    user_info = json.load(f)

username_value = user_info["username"]
password_value = user_info["password"]

# 检测 courseList.csv 文件是否存在
if not os.path.exists('courseList.csv'):
    # 设置ChromeDriver路径
    chrome_driver_path = 'chromedriver/chromedriver'  # 确保这个路径是正确的
    service = Service(chrome_driver_path)

    # 初始化Chrome浏览器
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # 打开指定的URL并登录
    url = 'https://mis.uic.edu.cn/mis/usr/login.sec'
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

    # 进入选课页面
    elective_url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
    driver.get(elective_url)

    # 初始化课程信息列表
    courses = []

    # 获取所有 "Select Course / Item" 链接的数量
    view_course_links = driver.find_elements(By.XPATH, "//a[contains(@title, 'Select Course')]")
    links_count = len(view_course_links)
    print(f"Found {links_count} 'Select Course / Item' links.")



    processed_links = set()

    while len(processed_links) < links_count:
        view_course_links = driver.find_elements(By.XPATH, "//a[contains(@title, 'Select Course')]")
        for index, link in enumerate(view_course_links):
            if index in processed_links:
                continue

            try:
                # 重新获取链接，因为页面刷新后旧的链接可能失效
                link = view_course_links[index]
                link.click()

                # 获取当前页面的HTML内容
                html_content = driver.page_source

                # 解析HTML内容并提取课程信息
                soup = BeautifulSoup(html_content, "html.parser")
                rows = soup.find_all("tr")

                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) >= 2:
                        course_id = columns[0].text.strip()
                        course_name = columns[1].text.strip()
                        elective_type_element = row.find("input", {"type": "hidden", "id": lambda x: x and x.endswith("_type")})
                        if elective_type_element:
                            elective_type_id = elective_type_element["id"]
                            course_id_from_elective = elective_type_id.replace("_type", "")
                            courses.append({
                                "courseId": course_id_from_elective,
                                "electiveTypeId": elective_type_id,
                                "courseName": course_name
                            })

                # 返回选课页面
                driver.get(elective_url)
                processed_links.add(index)

            except Exception as e:
                print(f"Error processing link: {e}")
                driver.get(elective_url)
                continue

    # 将课程信息转换为DataFrame并保存为CSV文件
    df_courses = pd.DataFrame(courses)
    df_courses.to_csv("courseList.csv", index=False)
    print("Course information has been extracted and saved to courseList.csv.")

    # 关闭浏览器
    driver.quit()

    # run main_menu.py
    os.system('python main_menu.py')
else:
    print("courseList.csv 已存在，不需要再次获取课程信息。")
    input()
    os.system('python main_menu.py')
