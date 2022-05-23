import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions as e
import os
import sys
import inspect
from dotenv import dotenv_values

ADMINS = dotenv_values("admins.env")["ADMINS"]

def login_session_simulation(user_username, user_password):

    service = Service("chromedriver.exe")
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service = service, options = options)

    driver.get("https://pythonflaskvirtualpiano.herokuapp.com/")

    LOGIN_ELEMENT_XPATH = "/html/body/div[1]/div[6]/a"
    LOGIN_USERNAME_XPATH = "/html/body/div[2]/div/div[2]/form/div[1]/input"
    LOGIN_PASSWORD_XPATH = "/html/body/div[2]/div/div[2]/form/div[2]/input"
    LOGIN_BUTTON_XPATH = "/html/body/div[2]/div/div[4]/input"
    SORT_GENRES_XPATH = "/html/body/div[1]/div[5]/a"
    UPDATE_GENRE_XPATH = "/html/body/div[2]/div[2]/a[2]/button"
    SELECT_GENRE_XPATH = "/html/body/div[2]/div/form/div/select"
    UPDATE_BUTTON_XPATH = "/html/body/div[2]/form/button"

    def get_element_XPATH(XPATH):
        try:
            element = driver.find_element(By.XPATH, XPATH)
            return element
        except e.NoSuchElementException:
            raise ValueError("Expected XPATH input")

    # need to wrap this in a function to be reused in order to avoid stale reference
    def login_admin():

        #visiting the register/login page
        LOGIN_PAGE_ELEMENT = get_element_XPATH(LOGIN_ELEMENT_XPATH)
        LOGIN_PAGE_ELEMENT.click()

        #sending the keys
        LOGIN_USERNAME_ELEMENT = get_element_XPATH(LOGIN_USERNAME_XPATH)
        LOGIN_USERNAME_ELEMENT.click()
        LOGIN_USERNAME_ELEMENT.send_keys(user_username)

        LOGIN_PASSWORD_ELEMENT = get_element_XPATH(LOGIN_PASSWORD_XPATH)
        LOGIN_PASSWORD_ELEMENT.click()
        LOGIN_PASSWORD_ELEMENT.send_keys(user_password)

        LOGIN_BUTTON_ELEMENT = get_element_XPATH(LOGIN_BUTTON_XPATH)
        LOGIN_BUTTON_ELEMENT.click()

        SORT_GENRES_ELEMENT = get_element_XPATH(SORT_GENRES_XPATH)
        SORT_GENRES_ELEMENT.click()

        #admins have the option to update genre for a sheet
        UPDATE_GENRE_ELEMENT = get_element_XPATH(UPDATE_GENRE_XPATH)
        UPDATE_GENRE_ELEMENT.click()

        SELECT_ELEMENT = Select(driver.find_element(By.NAME, "update_genres_select"))
        SELECT_ELEMENT.select_by_visible_text("CLASSICAL")

        UPDATE_BUTTON_ELEMENT = get_element_XPATH(UPDATE_BUTTON_XPATH)
        UPDATE_BUTTON_ELEMENT.click()

    def login_user():
        # visiting the register/login page
        LOGIN_PAGE_ELEMENT = get_element_XPATH(LOGIN_ELEMENT_XPATH)
        LOGIN_PAGE_ELEMENT.click()

        # sending the keys
        LOGIN_USERNAME_ELEMENT = get_element_XPATH(LOGIN_USERNAME_XPATH)
        LOGIN_USERNAME_ELEMENT.click()
        LOGIN_USERNAME_ELEMENT.send_keys(user_username)

        LOGIN_PASSWORD_ELEMENT = get_element_XPATH(LOGIN_PASSWORD_XPATH)
        LOGIN_PASSWORD_ELEMENT.click()
        LOGIN_PASSWORD_ELEMENT.send_keys(user_password)

        LOGIN_BUTTON_ELEMENT = get_element_XPATH(LOGIN_BUTTON_XPATH)
        LOGIN_BUTTON_ELEMENT.click()

    if user_username in ADMINS:
        login_admin()
    else:
        login_user()

login_session_simulation("hardlane2000", "hardlane17")