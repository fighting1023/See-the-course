# coding:utf-8
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def sleep_sed_num():
    sed = random.uniform(2, 3)
    time.sleep(sed)


def login():
    username = '账号'
    password = '密码'
    print('用户登录...')
    opt = webdriver.ChromeOptions()  # 创建浏览器
    print(' ' * 5 + "浏览器已打开")
    driver = webdriver.Chrome(options=opt)
    driver.get('https://www.bjjnts.cn/login')  # 打开目标网址
    print(' ' * 5 + "登录网页已打开")
    driver.maximize_window()  # 窗口最大化
    sleep_sed_num()  # 停留几秒

    inputs = driver.find_elements_by_tag_name("input")
    for input_ in inputs:
        if input_.get_attribute("type") == "text":
            input_.send_keys(username)
            print(' ' * 5 + '用户名已输入')
        sleep_sed_num()
        if input_.get_attribute("type") == "password":
            input_.send_keys(password)
            print(' ' * 5 + '密码已输入')
        sleep_sed_num()

    ele_btn_login = driver.find_element_by_class_name("login_btn")
    ele_btn_login.click()
    sleep_sed_num()
    print(' ' * 5 + '您已登录\n\n')
    return driver


def is_time(hour, minute, second):
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    time_start = int(time.time())
    time_end = time_start + 3600 * hour + 60 * minute + second + 30
    return time_end


def play_video(driver, website, video_id):
    driver.get(website)
    ele_video_btm = driver.find_element_by_xpath('//a[@data-lessonnum="' + str(video_id) + '"]')  # 找到目标视频标签
    video_name = driver.find_element_by_xpath('//a[@data-lessonnum="' + str(video_id) + '"]/div/h4')  # 获取目标视频名称
    video_name = video_name.text
    print(' ' * 6 + str(video_id) + '.' + str(video_name) + ':')
    total_time_text = driver.find_element_by_xpath(
        '//a[@data-lessonnum="' + str(video_id) + '"]/div/p[@class="course_study_menudate"]')  # 获取目标视频时长
    total_time_text = total_time_text.text  # 获取目标视频时长
    total_time = int(total_time_text[1:3]) * 3600 + int(total_time_text[4:6]) * 60 + int(total_time_text[7:9])

    schedule = driver.find_element_by_xpath('//a[@data-lessonnum="' + str(video_id) + '"]/span')
    schedule = schedule.text
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    num_in_schedule = []
    for i in schedule:
        if i in numbers:
            num_in_schedule.append(i)
    if len(num_in_schedule) >= 3 and num_in_schedule[0] + num_in_schedule[1] + num_in_schedule[2] == '100':
        print(' ' * 14 + '视频播放已完成\n')
        return driver
    if len(num_in_schedule) > 1:
        num = (int(num_in_schedule[0]) * 10 + int(num_in_schedule[1]) - 7) / 100
        if num < 0:
            num = 0
    else:
        num = 0

    if num > 0.2:
        print(' ' * 8 + '二刷：')
        time_end = int(time.time()) + int(total_time * (1 - num)) + 30
        time.sleep(2)
        ele_video_btm.click()
        print(' ' * 10 + '视频播放时间：',
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
              ' --> ',
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end))
              )
        video_window = driver.find_element_by_xpath('//video[@id="studymovie"]')
        ActionChains(driver).move_to_element_with_offset(video_window, 888 * num, 499).perform()
        print(' ' * 10 + '二刷悬停3s...')
        time.sleep(3)
        print(' ' * 10 + '二刷点击进度条')
        ActionChains(driver).move_to_element_with_offset(video_window, 726, 499).click().perform()
        print(' ' * 10 + '二刷点击进度条已拖至', num * 100, '%')


    else:
        time_end = (int(time.time()) + total_time + 30)
        ele_video_btm.click()
        print(' ' * 10 + '视频播放时间：',
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),
              ' --> ',
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end))
              )
        sleep_sed_num()
        print(' ' * 10 + "开始时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))
        time.sleep(3)
        print(' ' * 10, '3秒后播放视频')
        ele_video_btm.click()
        print(' ' * 10 + '视频播放中...')

    i = 0
    j = 0
    while True:
        if time_end < int(time.time()):
            print(' ' * 14 + '视频播放已完成\n')
            return driver
        try:  # 处理浏览器的弹窗
            # confirm = driver.switch_to_alert()
            confirm = driver.switch_to_default_content()
            time.sleep(2)
            confirm.accept()
            i += 1
            print(' ' * 10 + '已关闭浏览器弹窗次数：' + str(i))
            time.sleep(2)
        except:
            pass

        try:  # 处理网页"继续"弹窗
            WebDriverWait(driver, 2, 0.5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "layui-layer-btn0")))
            time.sleep(2)
            driver.find_element_by_class_name("layui-layer-btn0").click()
            j += 1
            print(' ' * 10 + '已关闭网页弹窗次数：' + str(j) + ' ' * 5 + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                             time.localtime(int(time.time()))))
            time.sleep(2)
        except:
            pass

        try:  # 处理网页"人脸识别"弹窗
            WebDriverWait(driver, 2, 0.5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "face_startbtn")))
            time.sleep(2)
            driver.find_element_by_class_name("face_startbtn").click()
            j += 1
            print(' ' * 10 + '已关闭人脸识别弹窗次数：' + str(j) + ' ' * 5 + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                               time.localtime(int(time.time()))))
            f.write(' ' * 10 + '已关闭人脸识别弹窗次数：' + str(j) + ' ' * 5 + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                 time.localtime(
                                                                                     int(time.time()))) + '\n')
            time.sleep(2)
        except:
            time.sleep(3)


websites = ['https://www.bjjnts.cn/lessonStudy/48/1586',
            'https://www.bjjnts.cn/lessonStudy/60/2161',  # 内部控制与风险管理 15-87集
            'https://www.bjjnts.cn/lessonStudy/76/2857',  # 咨询管理 4-36集
            'https://www.bjjnts.cn/lessonStudy/79/2993',  # 组织行为学如何有效管理员工 9-71集
            'https://www.bjjnts.cn/lessonStudy/196/3986',  # 行政职业能力提升 7-62集
            'https://www.bjjnts.cn/lessonStudy/209/4547', ]  # 现代礼仪 26-49集

course_names = [
    '《组织行为学》--如何有效管理员工1',
    '《内部控制与风险管理》',
    '《咨询管理》',
    '《组织行为学如何有效管理员工》',
    '《行政职业能力提升》',
    '《现代礼仪》',
]

video_ids = [72, 88, 37, 1, 72, 63, 50]

if __name__ == '__main__':
        driver = login()
        for i in range(len(websites)):
            print(course_names[i] + '课程观看进度：')
            for video_id in range(1, video_ids[i]):
                while True:
                    driver = play_video(driver, websites[i], video_id)
                    driver.refresh()
                    schedule_ = driver.find_element_by_xpath('//a[@data-lessonnum="' + str(video_id) + '"]/span')
                    schedule_ = schedule_.text
                    if '100' in schedule_:
                        break

