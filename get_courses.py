# get_courses.py

import os
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_courses():
    with open('user_info.json', 'r') as f:
        user_info = json.load(f)

    username_value = user_info["username"]
    password_value = user_info["password"]

    if not os.path.exists('courseList.csv'):
        chrome_driver_path = 'chromedriver/chromedriver'
        service = Service(chrome_driver_path)

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)

        url = 'https://mis.uic.edu.cn/mis/usr/login.sec'
        driver.get(url)

        username = driver.find_element(By.ID, 'j_username')
        password = driver.find_element(By.NAME, 'j_password')
        student_radio = driver.find_element(By.ID, 'student')
        login_button = driver.find_element(By.XPATH, "//input[@type='image']")

        username.send_keys(username_value)
        password.send_keys(password_value)
        student_radio.click()
        login_button.click()

        elective_url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
        driver.get(elective_url)

        courses = []
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
                    link = view_course_links[index]
                    link.click()
                    html_content = driver.page_source
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

                    driver.get(elective_url)
                    processed_links.add(index)

                except Exception as e:
                    print(f"Error processing link: {e}")
                    driver.get(elective_url)
                    continue

        df_courses = pd.DataFrame(courses)
        df_courses.to_csv("courseList.csv", index=False)
        print("Course information has been extracted and saved to courseList.csv.")
    else:
        print("courseList.csv 已存在，不需要再次获取课程信息。")
