import json

import pandas as pd


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


def save_js_code():
    with open('user_info.json', 'r') as f:
        user_info = json.load(f)

    course_names = user_info["course_names"]
    df_courses = pd.read_csv('courseList.csv')

    js_code = generate_javascript_code(course_names, df_courses)

    # formatted_js_code = "javascript:" + js_code
    formatted_js_code = "javascript:" + js_code.replace("\n", "").replace("    ", "").replace("            ", "")

    with open('js_output.txt', 'w') as f:
        f.write(formatted_js_code)


    print("JavaScript code has been saved to generate_javascript_code.js.")
