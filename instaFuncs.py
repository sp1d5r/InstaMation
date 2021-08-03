

import time
from time import sleep
import random
from selenium import webdriver
import os
from instaConsts import *


'''
How to get chrome driver working (Mac)
1) check chrome version
2) download appropriate version from :https://chromedriver.chromium.org/downloads
3) open the zipped file 
4) move the chrome driver file to /usr/local/bin (to do this open finder, then click go (top left) then go to folder, 
            and then '/usr/local/bin')
5) make sure to run the chrome driver for the first time by right clicking it, then clickign open, then open again and 
            let it run for 2 mins 
            
Windows tutorial will be done soon + Raspberry tutorial too
'''

# save the strings of the buttons in separate file so i don't need to update the whole thing every damn time...

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def start_up(username, password):
    username = username
    password = password
    try:
        if (os.environ["LOCAL"]==False):
            mobile_emulation = {"deviceName": "Nexus 5"}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.binary_location = GOOGLE_CHROME_PATH
            driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options,
                                      desired_capabilities=chrome_options.to_capabilities())
        else:
            mobile_emulation = {"deviceName": "Nexus 5"}
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            chrome_options.add_experimental_option("detach", True)
            # chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())

    except:
        mobile_emulation = {"deviceName": "Nexus 5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities())

    driver.set_window_size(300, 780)
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    time.sleep(1)
    if (not login(username, password, driver)):
        raise Exception("User Failed to Log in")
    return driver


def follow(username, driver):
    try:
        if not is_following(username, driver):
            driver.find_element_by_xpath("//button[text() = \"Follow\"]").click()
            # update the table of usernames
            action_blocked_checker(driver)
            return True
        else:
            return False
    except:
        print("following :" + username + " failed")
        return False


def unfollow(username, driver):
    if is_following(username, driver):
        driver.find_element_by_xpath("//span[contains(@aria-label, \"Following\")]").click()
        sleep_random_decimals(small_lower, small_upper)
        driver.find_element_by_xpath("// button[text() = \"Unfollow\"]").click()
        action_blocked_checker(driver)
        return True
    elif is_requested(username, driver):
        driver.find_element_by_xpath("//button[text() = \"Requested\"]").click()
        sleep_random_decimals(small_lower, small_upper)
        driver.find_element_by_xpath("// button[text() = \"Unfollow\"]").click()
        return True
    else:
        return False


def follow_users_from_user(user, driver):
    # returns an array
    go_to_page(user, driver)
    # driver.get("https://www.instagram.com/"+ user +"/followers/")
    sleep_random_decimals(3, 7)
    go_to_page(user, driver)
    sleep_random_decimals(3,7)
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[2]/a/span").click()
    usernames = []
    sleep_random_decimals(4, 7)
    for i in range(2, random.randint(9, 50)):
        try:
            new_username = driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"]/div/div[1]/div[2]/div[1]/a")
            follow_button = driver.find_element_by_xpath(
                            "//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"] /div/div[2]/button")
            if follow_button.text == "Follow":
                new_username_text = new_username.text
                follow_button.click()
                print("following:\t" + new_username_text)
            else:
                print("Already Following: \t" + new_username.text)
            usernames.append(new_username_text)
            sleep_random_decimals(30, 50)
            follow_button.location_once_scrolled_into_view
        except:
            print("Unable to Follow Users --> If persists, message Elijah")
            sleep_random_decimals(6, 10)
        sleep_random_decimals(6, 10)
    sleep_random_decimals(1200, 1500)
    return usernames


def follow_users_from_first_post(user, driver):
    # returns array of 9 users who liked the post
    go_to_page(user, driver)
    sleep_random_decimals(2, 4)
    try:
        first_post = driver.find_element_by_xpath(
        "//*[@id=\"react-root\"]/section/main/div/div[4]/article/div[1]/div/div[1]/div[1]/a/div/div[2]")
    except:
        try:
            first_post = driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/")
        except:
            print("could not find the first post...")
            return []
    first_post.location_once_scrolled_into_view
    sleep_random_decimals(2, 4)
    first_post.click()
    sleep_random_decimals(2, 4)
    try:

        bars = driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[2]/section[1]")
        bars.location_once_scrolled_into_view
        likes = driver.find_element_by_xpath(
            "//*[@id=\"react-root\"]/section/main/div/div[1]/article/div[2]/section[2]/div/div[2]/a[2]")
        sleep_random_decimals(2, 4)
    except:
        print("probably a video")
        return []
    sleep_random_decimals(1, 2)
    likes.click()
    sleep_random_decimals(2, 4)
    usernames = []
    for i in range(1, random.randint(10,50)):
        try:
            new_username = driver.find_element_by_xpath(
                "//div/div/div["+str(i)+"]/div/div/div/a/div/div/div")
            follow_button = driver.find_element_by_xpath(
                            "//*[@id=\"react-root\"]/section/main/div[1]/div/div["+str(i)+"]/div[3]/button")

            if follow_button.text == "Follow":
                new_username_text = new_username.text
                follow_button.click()
                print("following:\t" + new_username_text)
            else:
                print("Already Following: \t" + new_username.text)
            usernames.append(new_username_text)
            sleep_random_decimals(30, 50)
            follow_button.location_once_scrolled_into_view
        except:
            print("Unable to Follow Users --> If persists, message Elijah")

    sleep_random_decimals(4, 9)
    return usernames


def get_my_followers(your_username, driver):
    driver.get("https://www.instagram.com/" + your_username)
    sleep_random_decimals(4, 8)
    number_of_followers = int(
        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[2]/a/span").text.replace(',', ''))
    count = 0
    followers = []
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[2]/a").click()
    sleep_random_decimals(4, 5)

    for i in range(1, number_of_followers + 1):
        try:
            new_username = driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"]/div/div[1]/div[2]/div[1]/a")
            new_username.location_once_scrolled_into_view
            print(new_username.text)
            followers.append(new_username.text)
            sleep_random_decimals(0.5, 1)
        except:
            if (count < 11):
                print("Error, trying again")
                count += 1
            else:
                print("unable to load all followers:")
                print(followers)
                return followers

    print(followers)
    return followers


def get_my_following(your_username, driver):
    driver.get("https://www.instagram.com/" + your_username)
    sleep_random_decimals(2, 4)
    number_of_followers = int(
        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a/span").text.replace(',',''))
    count = 0
    following = []
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a").click()
    sleep_random_decimals(4, 5)

    for i in range(1,number_of_followers + 1):
        try:
            new_username = driver.find_element_by_xpath( "//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"]/div/div[1]/div[2]/div[1]/a")
            new_username.location_once_scrolled_into_view
            print(new_username.text)
            following.append(new_username.text)
            sleep_random_decimals(0.5,1)
        except:
            if (count < 11):
                print("Instagram doesn't always load all following")
                count += 1
            else:
                print(following)
                return following

    print(following)
    return following


def unfollowing_my_following(your_username, driver):
    driver.get("https://www.instagram.com/" + your_username)

    followers = get_my_followers(your_username, driver)
    following = get_my_following(your_username, driver)

    for i in following:
        if i not in followers:
            print("unfollowing user: " + i)
            unfollow(i, driver)
            sleep_random_decimals(30, 50)

    print("finished unfollowing dickhead users")


def quicker_unfollow_my_following(your_username, driver):
    driver.get("https://www.instagram.com/" + your_username)

    followers = get_my_followers(your_username, driver)
    sleep(2)
    driver.get("https://www.instagram.com/" + your_username)
    sleep_random_decimals(2, 4)
    number_of_followers = int(
        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a/span").text.replace(',',''))
    count = 0
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a").click()
    sleep_random_decimals(4, 5)

    for i in range(1, number_of_followers + 1):
        try:
            new_username = driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/section/main/div/ul/div/li[" + str(i) + "]/div/div[1]/div[2]/div[1]/a")
            if not (new_username in followers):
                try:
                    follow_button = driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"]/div/div[2]/button")
                    if (follow_button.text == "Unfollow"):
                        follow_button.click()
                        sleep_random_decimals(1,2)
                        confirm_unfollow = driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]")
                        confirm_unfollow.click()
                        print("unfollowed: \t" + new_username)
                except:
                    print("failed to unfollow the user")
                # unfollow these users
            new_username.location_once_scrolled_into_view
            print(new_username.text)
            sleep_random_decimals(0.5, 1)
        except:
            print("Error, user :" + str(i) + " not found")



def follow_new_users(user_arry, driver):
    popular_accounts = user_arry
    count = 0
    while count < 2:
        # get each function to follow the users themselves
        if (count % 2 == 0):
            for i in popular_accounts:
                # collect the usernames that you need to follow
                follow_users_from_first_post(i, driver)
                # sleep randomly inbetween getting users to reduce the suspicion of instagram
                sleep_random_decimals(60, 120)
        else :
            for j in popular_accounts:
                # collect the usernames that you need to follow
                follow_users_from_user(j, driver)
                # sleep randomly inbetween getting users to reduce the suspicion of instagram
                sleep_random_decimals(60, 120)

        count += 1

def follow_new_users_from_post(user_arry, driver):
    popular_accounts = user_arry
    count = 0
    while count < len(user_arry):
        for i in popular_accounts:
            # collect the usernames that you need to follow
            follow_users_from_first_post(i, driver)
            # sleep randomly inbetween getting users to reduce the suspicion of instagram
            sleep_random_decimals(60, 120)
        count += 1


def action_blocked_checker(driver):
    try:
        driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/button[2]")
        print("Instagram Bot Detected... ")
        sleep(1000000)
    except:
         i = 1


def send_message(username, message, driver):
    # Message must only contain 4 bit Unicode.
    go_to_page(username, driver)
    sleep_random_decimals(2,5)
    message_button = driver.find_element_by_xpath("//button[text()=\"Message\"]")
    message_button.click()
    sleep_random_decimals(2,5)
    send_message_field = driver.find_element_by_xpath("//textarea[@placeholder=\"Message...\"]")
    send_message_field.send_keys(message)
    sleep_random_decimals(2,5)
    send_button = driver.find_element_by_xpath("//button[text()=\"Send\"]")
    send_button.click()

# helper methods


def login(username, password, driver):
    time.sleep(2)
    driver.find_element_by_xpath("//button[text()=\"Accept All\"]").click()
    time.sleep(3)
    driver.find_element_by_xpath("//Input[@name=\"username\"]") \
        .send_keys(username)
    driver.find_element_by_xpath("//Input[@name=\"password\"]").send_keys(password)
    time.sleep(0.5)
    driver.find_element_by_xpath("//button[@type =\"submit\"]").click()
    sleep(10)

    try:
        driver.find_element_by_xpath("//a[text()=\"Not Now\"]").click()
        sleep(5)
    except:
        print("Could not find \"Not Now\" button, carrying on with login authentication flow")
        sleep(5)

    try:
        driver.find_element_by_xpath("//button[text()=\"Cancel\"]").click()
        sleep_random_decimals(2, 3)
    except:
        print("Could not fine \"Cancel\" button, carrying on with login authentication flow")
        sleep_random_decimals(2, 3)

    try:
        driver.find_element_by_xpath("//button[text()=\"Try Again\"]").click()
        print("Login Failed.")
        return False
    except:
        sleep_random_decimals(2,3)
        return True



def get_username_from_url(driver):
    # assumes you've gone to the correct URL
    return driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/header/section/div[1]/h1").text


def is_following(username, driver):
    go_to_page(username, driver)
    sleep_random_decimals(0, 0.5)
    try:
        driver.find_element_by_xpath(
            "//*[@id=\"react-root\"]/section/main/div/header/section/div[2]/div[2]/span/span[1]/button/div/span["
            "contains(@aria-label, \"Following\")]")
        print("you are following" + username)
        return True
    except:
        print("you are not following" + username)
        return False


def is_requested(username, driver):
    go_to_page(username, driver)
    sleep_random_decimals(0, 0.5)
    try:
        driver.find_element_by_xpath("//button[text()=\"Requested\"]")
        print("you have requested" + username)
        return True
    except:
        print("you have not requested" + username)
        return False


def go_to_page(username, driver):
    driver.get("https://www.instagram.com/" + username + "/")


def sleep_random_decimals(lower_bound, upper_bound):
    time.sleep(float(random.randrange(lower_bound * 1000, upper_bound * 1000) / 1000))


def unfollow_users_not_following(following, followers, driver):
    # params - following = list of perople following,
    # followers = list of who im following
    # collect my followers in an array,
    # collect my following in an array,
    # find users in following but not followers
    # unfollow these users.

    for i in following:
        if i not in followers:
            unfollow(i, driver)
            print("unfollowed: " + i)
            sleep_random_decimals(60, 120)


    print("Done")


def unfollow_my_not_followers(username, followers, driver):
    driver.get("https://www.instagram.com/" + username)
    sleep_random_decimals(2, 4)
    number_of_followers = int(
        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a/span").text.replace(',',''))
    count = 0
    following = []
    driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/div/ul/li[3]/a").click()
    sleep_random_decimals(4, 5)

    for i in range(1, number_of_followers + 1):
        try:
            new_username = driver.find_element_by_xpath(
                "//*[@id=\"react-root\"]/section/main/div/ul/div/li[" + str(i) + "]/div/div[1]/div[2]/div[1]/a")
            new_username.location_once_scrolled_into_view
            if not (new_username.text in followers):
                follow_button = driver.find_element_by_xpath( "//*[@id=\"react-root\"]/section/main/div/ul/div/li["+str(i)+"]/div/div[2]/button")
                follow_button.click()
                sleep(2)
                unfollow_button = driver.find_element_by_xpath("//button[text()=\"Unfollow\"]")
                unfollow_button.click()
                sleep(2)

                print("unfollowing user: \t" + new_username.text)
                sleep_random_decimals(30, 50)
            else:
                print("not unfollowing user: \t" + new_username.text)
            following.append(new_username.text)
        except:
            if (count < 11):
                print("Error, trying again")
                count += 1
            else:
                return following

    print(following)
    return following

def array_to_string(array):
    string = ''
    for i in array:
        string = string + i + '\n'

    return string


'''
Old test...
driv = start_up(account_login_car_manic, account_login_pass_car_manic)
user_arr_house_manic = ["REALESTATELEGEND", "REALESTATE_ACADEMY", "REALESTATEAUS", "BEGINNINGINTHEMIDDLE", "JAMESGALLO_COM", "THE_REAL_HOUSES_OF_IG"]
user_arr_travel_manic = ["travelandleisure", "bestvacations", "travel_a_little_luxe", "tourist2townie", "andyto",
                        "kristarossow"]
user_arr_car_manic= ["audi_city", "luxury", "_some_car_guy_", "ferrariusa", "vw"]


while True:
    sleep(20)
    follow_new_users(user_arr_car_manic, driv)
    sleep_random_decimals(3000, 4500)
    unfollowing_my_following(account_login_travel_manic, driv)
    sleep_random_decimals(3000, 4500)
'''