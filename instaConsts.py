heart_emoji1 = "\u2764"
heart_emoji2 = "\u2763"
smile_emoji = "\uE414"

small_lower = 0.2
small_upper = 1.5

medium_lower = 5
medium_upper = 10

large_lower = 500
large_upper = 10000

'''
XPATHS TO DIFFERENT LOCATIONS ON INSTAGRAM 
'''
first_post_xpath1 = '//*[@id="react-root"]/section/main/div/div[4]/article/div[1]/div/div[1]/div[1]/a/div/div[2]'
first_post_xpath2 = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a'

bar_xpath = '//*[@id="react-root"]/section/main/div/div/article/div/div[3]/section'
liked_by_xpath = '//a[text()=" others"]'

followers_button_xpath = '//a[text()=" followers"]'
following_button_xpath = '//a[text()=" following"]'

following_number_xpath = '//*[@id="react-root"]/section/main/div/ul/li[3]/a/span'

confirm_unfollow_button = '/html/body/div[4]/div/div/div/div[3]/button[1]'

def follow_button_from_followers_list(number):
    return "//div/section/main/div/ul/div/li[" + str(number) + "]/div/div[2]/button"

def username_from_followers_list(number):
    return "//div/section/main/div/ul/div/li[" +str(number)+"]/div/div[1]/div[2]/div[1]/a"

def username_from_unfollowing_list(number):
    return '//*[@id="react-root"]/section/main/div/ul/div/li['+str(number)+']/div/div[1]/div[2]/div[1]'

def unfollow_button_from_unfollowing_list(number):
    return '//*[@id="react-root"]/section/main/div/ul/div/li['+str(number)+']/div/div[2]/button'

def username_from_list(number):
    return "//div/div/div["+str(number)+"]/div/div/div/a/div/div/div"

def follow_button_from_list(number):
    return "//*[@id=\"react-root\"]/section/main/div[1]/div/div["+str(number)+"]/div[3]/button"




account_login_eli = "eli.bear__"

account_login_pass_eli = "rirqot-tacgaq-1tySqi"

TESTUSERNAME1 = "imjustbait"
TESTUSERNAME2 = "instagram"
TESTUSERNAME3 = "nadia.daniel_"
TESTUSERNAME4 = "filipedocarmo__"