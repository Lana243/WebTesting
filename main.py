import time

import pytest
import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import select
import datetime

URL = "https://acmp.ru"


class TestACMP:
    def setup_class(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 4)

    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self.driver.get(URL)
        yield

    def teardown_class(self):
        self.driver.close()

    # tests

    def test_title(self):
        assert 'Школа программиста' in self.driver.title

    def test_pages(self):
        links = self.driver.find_elements(By.XPATH, "/html/body/table/tbody/tr[1]/td/table/tbody/tr[3]/td[1]/a")
        pages = ["[задачи]", "[курсы]", "[олимпиады]", "[регистрация]"]
        assert len(links) == len(pages)
        for i in range(len(pages)):
            assert links[i].text == pages[i]

    def test_pages_clickable(self):
        for i in range(1, 5):
            link = self.driver.find_element(By.XPATH, f'/html/body/table/tbody/tr[1]/td/table/tbody/tr[3]/td[1]/a[{i}]')
            link.click()

    def test_login(self):
        login_field = self.driver.find_element(By.NAME, "lgn")
        login_field.send_keys("qwe")
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("qwe")
        login_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()

    def test_time(self):
        timer_field = self.driver.find_element(By.ID, "timer")
        time = datetime.date.today().strftime("%-m/%-d/%Y")
        assert time in timer_field.text

    def test_tasks(self):
        tasks_button = self.driver.find_element(By.XPATH,
                                                "/html/body/table/tbody/tr[1]/td/table/tbody/tr[3]/td[1]/a[1]")
        tasks_button.click()
        topic_select = select.Select(self.driver.find_element(By.NAME, "id_type"))
        expected_options = ["Все", "Бинарный поиск", "Геометрия", "Два указателя", "Двумерные массивы",
                            "Динамическое программирование", "Длинная арифметика", "Жадный алгоритм",
                            "Задачи для начинающих", "Комбинаторика", "Математическое моделирование",
                            "Простая математика", "Разбор строк", "Разное", "Рекурсия, перебор",
                            "Системы счисления", "Сортировка и последовательности", "Структуры данных",
                            "Теория графов", "Целочисленная арифметика"]
        assert len(expected_options) == len(topic_select.options)
        for i in range(len(expected_options)):
            assert expected_options[i] == topic_select.options[i].text

    def test_task_selection(self):
        tasks_button = self.driver.find_element(By.XPATH,
                                                "/html/body/table/tbody/tr[1]/td/table/tbody/tr[3]/td[1]/a[1]")
        tasks_button.click()
        topic_select = select.Select(self.driver.find_element(By.NAME, "id_type"))
        topic_select.select_by_visible_text("Задачи для начинающих")
        task_name = self.driver.find_element(By.NAME, "str")
        task_name.send_keys("A+B", selenium.webdriver.Keys.RETURN)
        time.sleep(2)
        rows = self.driver.find_elements(By.XPATH,
            "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table[3]/tbody/tr")
        assert len(rows) == 2
        task = self.driver.find_element(By.XPATH,
            "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table[3]/tbody/tr[2]/td[2]/a")
        assert task.text == "A+B"
