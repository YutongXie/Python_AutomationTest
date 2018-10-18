# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

import unittest, time, re

class TestSearch(unittest.TestCase):
    #初始化资源，例如Firefox的driver
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    # 执行用例的方法
    def test_kanban(self):
        #初始化 Firefox driver
        driver = self.driver
        #登录
        driver.get("http://test/login/do.jsp?method=login")
        driver.find_element_by_id("userName").click()
        driver.find_element_by_id("userName").clear()
        driver.find_element_by_id("userName").send_keys("test")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("test")
        driver.find_element_by_id("password").send_keys(Keys.DOWN)
        driver.find_element_by_id("login-button").click()
        #切换到主页面
        driver.switch_to.parent_frame()
        #停顿1s，等待页面加载
        time.sleep(1)
        #点击 进入后台
        driver.find_element_by_link_text(u"进入后台").click()
        #切换到 top frame
        driver.switch_to.frame("topFrame")
        #点击 后台
        driver.find_element_by_link_text(u"后台").click()
        #切回到 主页面
        driver.switch_to.parent_frame()
        #切换到 left frame
        driver.switch_to.frame("leftFrame")
        time.sleep(1)
        #点击 物料管理 tab页
        driver.find_element_by_id("leftMenuSpan612").click()
        time.sleep(1)
        #点击 物料管理项目
        driver.find_element_by_link_text(u"物料管理").click()
        # 切回到 主页面
        driver.switch_to.parent_frame()
        # 切回到 中央区域 frame
        driver.switch_to.frame("main")
        #选择查询条件，进行查询
        Select(driver.find_element_by_id("tid")).select_by_visible_text(u"三联挂旗")
        driver.find_element_by_id("materialname").send_keys("this is test")
        driver.find_element_by_name("Submit").click()

        time.sleep(1)
        #获取 数据表格的统计信息
        pageNum = driver.find_element_by_xpath('//div[@class="fr listpage"]/span').text
        #打印统计信息
        print("the page number char is :",pageNum)
        #断言 判断结果（case：可以查询到一条记录）
        try:
            assert "共1页 - 共1条数据" == pageNum
            print("测试结果符合期望，测试用例通过")
        except Exception as e:
            print("测试结果不符合期望，测试用例失败", format(e))
        # 断言 判断结果（case：查询不到记录）
        Select(driver.find_element_by_id("tid")).select_by_visible_text(u"三联挂旗")
        driver.find_element_by_id("materialname").send_keys("invalid test case")
        driver.find_element_by_name("Submit").click()

        time.sleep(1)

        pageNum2 = driver.find_element_by_xpath('//div[@class="fr listpage"]/span').text
        print("the page number char is :",pageNum2)
        try:
            assert "共0页 - 共0条数据" == pageNum2
            print("测试结果符合期望，测试用例通过")
        except Exception as e:
            print("测试结果不符合期望，测试用例失败", format(e))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
    # 退出程序，释放资源
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
