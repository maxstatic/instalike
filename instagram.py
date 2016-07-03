import random
from time import sleep
import logging


from selenium.webdriver.common.keys import Keys
from selenium import webdriver

log = logging.getLogger('instalike')



class Instagram(object):
    def __init__(self):
        self.__url = 'https://instagram.com'
        self.driver = None
        self.__start_browser()

    @staticmethod
    def fuzzy_delay(min_delay=0.1, max_delay=5):
        return random.randint(min_delay * 100., max_delay * 100.) / 100.

    def __start_browser(self):
        try:
            driver = webdriver.Firefox()
        except Exception as e:
            log.exception(e)
            raise Exception('Failed to load webdriver: {}'.format(str(e)))
        driver.get(self.__url)

    def iterate_articles(self):
        articles = self.driver.find_elements_by_class_name('_8ab8k')
        for one_article in articles:
            delay = self.fuzzy_delay()
            sleep(delay)
            author = one_article.find_element_by_class_name('_4zhc5').text
            like_button = one_article.find_element_by_class_name('_soakw')
            if like_button.text == 'Like':
                liked = False
            elif like_button.text == 'Unlike':
                liked = True
            else:
                liked = False
            print author, liked
            if not liked:
                delay = self.fuzzy_delay()
                print 'Liking in {}'.format(delay)
                sleep(delay)
                like_button.click()
                print 'Liked!'

    @staticmethod
    def get_article_data(article):
        """

        :param article: selenium webdriver element
        """
        pass
        result = {}
        result['avatar'] = article.find_element_by_class_name('_a012k').get_attribute('src')
        result['author'] = article.find_element_by_class_name('_4zhc5').text
        result['img'] = article.find_element_by_class_name('_icyx7').get_attribute('src')
        result['alt'] = article.find_element_by_class_name('_icyx7').get_attribute('alt')
        if article.find_element_by_class_name('_soakw').text == 'Like':
            result['liked'] = False
        elif article.find_element_by_class_name('_soakw').text == 'Unlike':
            result['liked'] = True
        else:
            raise Exception('Error parsing like status')
        return result
