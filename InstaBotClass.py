import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


class Instagrambot:
    """
    A class used to represent an bot itself

    ...

    Attributes
    ----------
    username : str
        is the Username of the Person, where you want to scrape the followers
    userlink : str
        is the link of the Person you want to follow / unfollow

    Methods
    -------
    sign_in(self)
        Is Signing the User with their Credentials

    get_user_followers(self, username)
        Is Visiting the User and start scrapping their Followers

    follow_user(self, userlink)
        Is visiting the user and is following them

    unfollow_user(self, userlink)
        Is visiting the User and unfollow them

    get_follower_by_userposts(self, username)
        Is Visiting the User and opens some of their Posts to Scrape Followers

    watch_stories(self)
        Is visiting and Watching your Stories

    close_browser_session(self)
        Is closing the Browser Session


    """

    def __init__(self, username, password):
        self.browser = webdriver.Chrome("<LinktoChromedriver>")
        self.username = username
        self.password = password

    def sign_in(self):
        """ Is Signing the User with their Credentials

        """
        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(3)
        username = self.browser.find_element_by_name("username")
        username.send_keys(self.username)
        password = self.browser.find_element_by_name("password")
        password.send_keys(self.password)

        submit = self.browser.find_element_by_tag_name("form")
        submit.submit()
        time.sleep(8)

        not_now_button = WebDriverWait(self.browser, 15).until(
            lambda d: d.find_element_by_xpath('//button[text()="Jetzt nicht"]')
        )
        not_now_button.click()

    def get_user_followers(self, username):
        """  Is Visiting the User and start scrapping their Followers

                Parameters
                ----------
                username : str
                    Is the Username of the Person, where you want to scrape the followers

        """

        self.browser.get('https://www.instagram.com/' + username)
        followers_link = self.browser.find_element_by_css_selector('ul li a')
        followers_link.click()
        time.sleep(2)
        followers_list = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
        followers_list.click()
        time.sleep(5)

        # Choose the Max amount of User you want to Scrape
        maximum = 5000

        # Find all li elements in list
        front_body = self.browser.find_element_by_xpath("//div[@class='isgrP']")
        while number_of_followers_in_list < maximum:  # scroll 5 times
            time.sleep(2)
            self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                        front_body)
            time.sleep(2)
            number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))

        followers = []
        follower_links = open("{0}.txt".format(username), "w")
        # Extracting all Links and the
        for user in followers_list.find_elements_by_css_selector('li'):
            user_link = user.find_element_by_css_selector('a').get_attribute('href')
            follower_links.write(user_link)
            follower_links.write("\n")

            if len(followers) == maximum:
                follower_links.close()
                break

    def follow_user(self, userlink):
        """ Is visiting the Userpage of the Person via userlink and is following them

                Parameters
                ----------
                userlink : str
                    Is the Userlink of the User
        """
        self.browser.get(userlink)
        time.sleep(10)
        try:
            follow_button = self.browser.find_element_by_css_selector('button')
            if follow_button.text != 'dfd':
                follow_button.click()
                time.sleep(2)
            else:
                print("You are already following this User")
        except:
            pass

    def unfollow_user(self, userlink):
        """ Is visiting the Userpage of the Person via userlink and is unfollow them

                Parameters
                ----------
                userlink : str
                    Is the Userlink of the User
        """
        self.browser.get(userlink)
        try:
            time.sleep(5)
            follow_button = self.browser.find_element_by_css_selector(
                "#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_._4EzTm > "
                "span > span.vBF20._1OSdk > button")
            follow_button.click()
            time.sleep(6)
            unfollow_button = self.browser.find_element_by_css_selector(
                "body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.-Cab_")
            unfollow_button.click()
        except:
            pass

    def get_follower_by_userposts(self, username):
        """ Is opening the Page of the User and is looking some posts and checks who liked them and write that down
        in a filw

                Parameters
                ----------
                username : str
                    Is the username of the User
        """
        outputfile = open("{0}.txt".format(username), "w")
        outputfile.close()
        filenumber = 1
        for row in [1, 2, 3]:
            for pictures in [1, 2, 3]:
                self.browser.get('https://www.instagram.com/' + username)
                pic = self.browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[{0}]/div[{1}]/a/div/div[2]'
                    .format(row, pictures))
                pic.click()
                time.sleep(10)
                try:
                    like_button = self.browser.find_element_by_xpath(
                        "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/button")
                    like_button.click()
                    time.sleep(10)
                    maximum = 50
                    counter = 1
                    count_usernames = 1
                    front_body = self.browser.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")
                    usernames_list = []

                    while counter < maximum:  # scroll 5 times
                        try:
                            time.sleep(2)
                            username = self.browser.find_element_by_css_selector(
                                "body > div.RnEpo.Yx5HN > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div "
                                "> div:nth-child({0})".format(count_usernames)).text
                            username = str(username)[:str(username).find('\n')]
                            usernames_list.append(username)
                            counter += 1
                            count_usernames += 1
                        except:
                            self.browser.execute_script(
                                'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                front_body)
                            count_usernames = 1

                    outputfile = open("{0}.txt".format(username + str(filenumber)), "w")
                    for user in usernames_list:
                        user = "https://www.instagram.com/" + user
                        outputfile.writelines(user + "\n")
                    filenumber += 1
                except:
                    pass

        outputfile = open("{0}.txt".format(username), "a")
        filenumber = filenumber - 1
        while filenumber > 0:
            for line in open("{0}.txt".format(username + str(filenumber)), "r"):
                outputfile.write(line)
            filenumber -= 1
        outputfile.close()

    def watch_stories(self):
        """ Is opening the Page of the your own account and is looking at the stories
        """
        try:
            self.browser.get("https://www.instagram.com/")
            all_stories = self.browser.find_element_by_css_selector(
                '#react-root > section > main > section > div.COOzN > '
                'div._6Rvw2.DPiy6.Igw0E.IwRSH.eGOV_._4EzTm.iHqQ7.b2rUF.ZUqME > '
                'div.Igw0E.rBNOH.eGOV_.ybXk5._4EzTm._49XvD.XfCBB.XTCZH.ZUqME > a > div')
            all_stories.click()
        except:
            pass

    def close_browser_session(self):
        self.browser.quit()
