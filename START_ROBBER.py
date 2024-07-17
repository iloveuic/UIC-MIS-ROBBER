# import os
# import threading
# import time
# from datetime import datetime, timedelta
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
#
# ###################填写以下内容######################
#
#
# # 用户名和密码，例如
# username_value = 'k130022222'
# password_value = 'Ysjh2231412'
#
# # 要加入的课程名称列表， 用逗号分开
# course_names = ['Approaches to Second Language Teaching (1002)', 'Listen and Speak Up (1007)', 'Professional Communication (1002)']
#
# start_rob_time = "10:00"
#
#
# #################################################
#
#
# # 检测 courseList.csv 文件是否存在
# if not os.path.exists('courseList.csv'):
#     # 设置ChromeDriver路径
#     chrome_driver_path = 'chromedriver/chromedriver'  # 确保这个路径是正确的
#     service = Service(chrome_driver_path)
#
#     # 初始化Chrome浏览器
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(chrome_driver_path)
#
#     # 打开指定的URL并登录
#     url = 'https://mis.uic.edu.cn/mis/usr/login.sec'
#     driver.get(url)
#
#     # 登录操作
#     username = driver.find_element(By.ID, 'j_username')
#     password = driver.find_element(By.NAME, 'j_password')
#     student_radio = driver.find_element(By.ID, 'student')
#     login_button = driver.find_element(By.XPATH, "//input[@type='image']")
#
#     username.send_keys(username_value)
#     password.send_keys(password_value)
#     student_radio.click()
#     login_button.click()
#
#     # 进入选课页面
#     elective_url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
#     driver.get(elective_url)
#
#     # 初始化课程信息列表
#     courses = []
#
#     # 获取所有 "Select Course / Item" 链接的数量
#     view_course_links = driver.find_elements(By.XPATH, "//a[contains(@title, 'Select Course')]")
#     links_count = len(view_course_links)
#     print(f"Found {links_count} 'Select Course / Item' links.")
#
#     processed_links = set()
#
#     while len(processed_links) < links_count:
#         view_course_links = driver.find_elements(By.XPATH, "//a[contains(@title, 'Select Course')]")
#         for index, link in enumerate(view_course_links):
#             if index in processed_links:
#                 continue
#
#             try:
#                 # 重新获取链接，因为页面刷新后旧的链接可能失效
#                 link = view_course_links[index]
#                 link.click()
#
#                 # 获取当前页面的HTML内容
#                 html_content = driver.page_source
#
#                 # 解析HTML内容并提取课程信息
#                 soup = BeautifulSoup(html_content, "html.parser")
#                 rows = soup.find_all("tr")
#
#                 for row in rows:
#                     columns = row.find_all("td")
#                     if len(columns) >= 2:
#                         course_id = columns[0].text.strip()
#                         course_name = columns[1].text.strip()
#                         elective_type_element = row.find("input", {"type": "hidden", "id": lambda x: x and x.endswith("_type")})
#                         if elective_type_element:
#                             elective_type_id = elective_type_element["id"]
#                             course_id_from_elective = elective_type_id.replace("_type", "")
#                             courses.append({
#                                 "courseId": course_id_from_elective,
#                                 "electiveTypeId": elective_type_id,
#                                 "courseName": course_name
#                             })
#
#                 # 返回选课页面
#                 driver.get(elective_url)
#                 processed_links.add(index)
#
#             except Exception as e:
#                 print(f"Error processing link: {e}")
#                 driver.get(elective_url)
#                 continue
#
#     # 将课程信息转换为DataFrame并保存为CSV文件
#     df_courses = pd.DataFrame(courses)
#     df_courses.to_csv("courseList.csv", index=False)
#     print("Course information has been extracted and saved to courseList.csv.")
#
# # 读取 courseList.csv 文件
# df_courses = pd.read_csv('courseList.csv')
#
# # 根据课程名称生成JavaScript代码
# def generate_javascript_code(course_names, courses):
#     course_data = []
#     for name in course_names:
#         course_info = courses[courses['courseName'] == name]
#         if not course_info.empty:
#             course_data.append({
#                 'electiveTypeId': course_info.iloc[0]['electiveTypeId'],
#                 'courseId': course_info.iloc[0]['courseId']
#             })
#         else:
#             print(f"Course not found: {name}")
#
#     javascript_code = """
#     (function() {
#         function joinCourses() {
#             const courses = [
#     """
#     for course in course_data:
#         javascript_code += f"{{ electiveTypeId: '{course['electiveTypeId']}', courseId: '{course['courseId']}' }},"
#
#     javascript_code += """
#             ];
#             courses.forEach(course => {
#                 fetch('https://mis.uic.edu.cn/mis/student/es/select.do', {
#                     method: 'POST',
#                     headers: {
#                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#                         'Content-Type': 'application/x-www-form-urlencoded'
#                     },
#                     body: new URLSearchParams({
#                         electiveTypeId: course.electiveTypeId,
#                         id: course.courseId
#                     })
#                 }).then(response => {
#                     if (response.ok) {
#                         console.log(`Successfully joined the course with ID: ${course.courseId}`);
#                     } else {
#                         console.log(`Failed to join the course with ID: ${course.courseId}. Please try again.`);
#                     }
#                 }).catch(error => {
#                     console.error('Error:', error);
#                     console.log(`An error occurred while trying to join the course with ID: ${course.courseId}`);
#                 });
#             });
#         }
#         joinCourses();
#     })();
#     """
#     return javascript_code
#
# # 生成JavaScript代码
# javascript_code = generate_javascript_code(course_names, df_courses)
#
# # 设置ChromeDriver路径
# chrome_driver_path = 'chromedriver/chromedriver'  # 确保这个路径是正确的
# service = Service(chrome_driver_path)
#
# # 初始化Chrome浏览器
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(chrome_driver_path)
#
# url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
# driver.get(url)
#
# # 登录操作
# username = driver.find_element(By.ID, 'j_username')
# password = driver.find_element(By.NAME, 'j_password')
# student_radio = driver.find_element(By.ID, 'student')
# login_button = driver.find_element(By.XPATH, "//input[@type='image']")
#
# username.send_keys(username_value)
# password.send_keys(password_value)
# student_radio.click()
# login_button.click()
#
# url = 'https://mis.uic.edu.cn/mis/student/es/elective.do'
# driver.get(url)
#
# # 定义任务
# def task(username_value, password_value, course_names, df_courses):
#     # start timing
#     start_time = time.time()
#     # 执行JavaScript代码
#     driver.execute_script(javascript_code)
#
#     # stop timing
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Elapsed time: {elapsed_time:.2f} seconds")
#
#     # 等待页面加载完成
#     time.sleep(0.1)
#
#     driver.get(url)
#
#     # 保持浏览器打开一段时间，以便查看结果
#     input("Press Enter to close the browser...")
#
#     # 关闭浏览器
#
# # 等待到指定时间执行任务，并打印剩余时间
# def wait_until_specified_time(execution_time, username_value, password_value, course_names, df_courses):
#     now = datetime.now()
#     next_execution_time = now.replace(hour=execution_time.hour, minute=execution_time.minute, second=0, microsecond=0)
#     if now >= next_execution_time:
#         next_execution_time += timedelta(days=1)
#
#     wait_time = (next_execution_time - now).total_seconds()
#     print(
#         f"Remaining time until execution: {int(wait_time // 3600)} hours, {int(wait_time % 3600 // 60)} minutes, {int(wait_time % 60)} seconds")
#
#     for _ in range(int(wait_time)):
#         time.sleep(1)
#         now = datetime.now()
#         wait_time = (next_execution_time - now).total_seconds()
#         if wait_time <= 0:
#             break
#         print(
#             f"Remaining time until execution: {int(wait_time // 3600)} hours, {int(wait_time % 3600 // 60)} minutes, {int(wait_time % 60)} seconds",
#             end='\r')
#
#     task(username_value, password_value, course_names, df_courses)
#
# if __name__ == "__main__":
#     # 定义执行任务的时间，例如10:00
#     execution_time = datetime.strptime(start_rob_time, "%H:%M").time()
#
#     # 开始等待
#     wait_until_specified_time(execution_time, username_value, password_value, course_names, df_courses)



import os
import threading
import time
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 从环境变量获取用户名、密码、课程名称和开始时间
username_value = os.getenv('USERNAME')
password_value = os.getenv('PASSWORD')
course_names = os.getenv('COURSES').split(',')
start_rob_time = os.getenv('START_TIME')

# 检测 courseList.csv 文件是否存在
if not os.path.exists('UIC_MIS_ROBBER/courseList.csv'):
    # 设置ChromeDriver路径
    chrome_driver_path = '/usr/local/bin/chromedriver'  # 确保这个路径是正确的
    service = Service(chrome_driver_path)

    # 初始化Chrome浏览器
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_driver_path)

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
    df_courses.to_csv("UIC_MIS_ROBBER/courseList.csv", index=False)
    print("Course information has been extracted and saved to courseList.csv.")

# 读取 courseList.csv 文件
df_courses = pd.read_csv('UIC_MIS_ROBBER/courseList.csv')

# 根据课程名称生成JavaScript代码
def generate_javascript_code(course_names, courses):
    course_data = []
    for name in course_names:
        course_info = courses[courses['courseName'] == name]
        if not course_info.empty:
            course_data.append({
                'electiveTypeId': course_info.iloc[0]['electiveTypeId'],
                'courseId': course_info.iloc[0]['courseId']
            })
        else:
            print(f"Course not found: {name}")

    javascript_code = """
    (function() { 
        function joinCourses() { 
            const courses = [ 
    """
    for course in course_data:
        javascript_code += f"{{ electiveTypeId: '{course['electiveTypeId']}', courseId: '{course['courseId']}' }},"

    javascript_code += """
            ]; 
            courses.forEach(course => { 
                fetch('https://mis.uic.edu.cn/mis/student/es/select.do', { 
                    method: 'POST', 
                    headers: { 
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
                        'Content-Type': 'application/x-www-form-urlencoded' 
                    }, 
                    body: new URLSearchParams({ 
                        electiveTypeId: course.electiveTypeId, 
                        id: course.courseId 
                    }) 
                }).then(response => { 
                    if (response.ok) { 
                        console.log(`Successfully joined the course with ID: ${course.courseId}`); 
                    } else { 
                        console.log(`Failed to join the course with ID: ${course.courseId}. Please try again.`); 
                    } 
                }).catch(error => { 
                    console.error('Error:', error); 
                    console.log(`An error occurred while trying to join the course with ID: ${course.courseId}`); 
                }); 
            }); 
        } 
        joinCourses(); 
    })();
    """
    return javascript_code

# 生成JavaScript代码
javascript_code = generate_javascript_code(course_names, df_courses)

# 初始化Chrome浏览器
driver = webdriver.Chrome(chrome_driver_path)

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
def task():
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
    driver.quit()

# 等待到指定时间执行任务，并打印剩余时间
def wait_until_specified_time(execution_time):
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

    task()

if __name__ == "__main__":
    # 定义执行任务的时间
    execution_time = datetime.strptime(start_rob_time, "%H:%M").time()

    # 开始等待
    wait_until_specified_time(execution_time)
