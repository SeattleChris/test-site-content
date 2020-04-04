""" Original Attempts from a different project running this inside a Flask app. """
from flask import flash, current_app as app
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import re
from os import path
# from pprint import pprint
# import json


# def phantom_grab(ig_url, filename):
#     """ Using selenium webdriver with phantom js and grabing the file from the page content. """
#     # from phantomjs import Phantom
#     from phantomjs_bin import executable_path

#     driver = webdriver.PhantomJS(executable_path=executable_path)
#     app.logger.info("==============================================")
#     files, message = [], ''
#     driver.get(ig_url)
#     temp = f"{filename}_full.png"
#     success = driver.save_screenshot(temp)
#     count = 0 if success else -1
#     files.append(temp)
#     app.logger.debug(f"Start of count at {count + 1}. ")
#     soup = bs(driver.page_source, 'html.parser')
#     # TODO: Determine if we can do this without BeautifulSoup processes.
#     target = [img.get('src') for img in soup.findAll('img') if not re.search("^\/", img.get('src'))]
#     pprint(target)
#     for ea in target:
#         count += 1
#         time.sleep(1)
#         try:
#             driver.get(ea)
#             temp = f"{filename}_{count}.png"
#             files.append(temp)
#             driver.save_screenshot(temp)
#         except Exception as e:
#             temp = f"Error on file # {count} . "
#             message += temp
#             app.logger.exception(e)
#     success = count == len(target)
#     message += 'Files Saved! ' if success else "Error in Screen Grab. "
#     app.logger.debug(message)
#     answer = {'success': success, 'message': message, 'file_list': files}
#     driver.close()
#     # driver.exit()  # Needed?
#     return answer


def chrome_grab(ig_url, filename):
    """ Using selenium webdriver with Chrome and grabing the file from the page content. """
    # import chromedriver_binary  # Adds chromedriver binary to path
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument("--remote-debugging-port=9222")
    # options.binary_location = chromedriver_binary.chromedriver_filename
    # chrome_executable_path = '/usr/bin/google-chrome'
    chromedriver_path = 'chromedriver' if app.config.get('LOCAL_ENV') else '/usr/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
    app.logger.info("=========================== Set driver in chrome_grab ===========================")
    files, message = [], ''
    driver.get(ig_url)
    temp = f"{filename}_full.png"
    success = driver.save_screenshot(temp)
    error_count = 0 if success else 1
    count = 0 if success else -1
    files.append(temp)
    app.logger.debug(f"Start of count at {count + 1}. ")
    soup = bs(driver.page_source, 'html.parser')
    # TODO: Determine if we can do this without BeautifulSoup processes.
    target = [img.get('src') for img in soup.findAll('img') if not re.search("^\/", img.get('src'))]
    for ea in target:
        count += 1
        time.sleep(1)
        try:
            driver.get(ea)
            temp = f"{filename}_{count}.png"
            files.append(temp)
            driver.save_screenshot(temp)
        except Exception as e:
            message += f"Error on file # {count} . "
            error_count += 1
            app.logger.exception(e)
    success = error_count == 0
    message += 'Files Saved! ' if success else "Error in Screen Grab. "
    app.logger.debug(message)
    answer = {'success': success, 'message': message, 'file_list': files}
    driver.close()
    # driver.quit()  # Needed?
    # driver.exit()  # Needed?
    return answer


def soup_no_chrome(ig_url, filename):
    """ If possible, approach that does not require a browser emulation.
        If the page is a react app, or depends on javascript, this probably won't work.
    """
    import requests
    import urllib.request

    def _get_images(ig_url, filename):
        """ Helper function to traverse and capture image files.
            Recursive call if image source points to another web page.
        """
        # extensions = ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp',)
        # vid_extensions = ('.mp4', '.mpeg', '.mpg', '.m4p', '.m4v', '.mp2', '.avi',)
        response = requests.get(ig_url)
        app.logger.debug(response)
        soup = bs(response.text, "html.parser")
        app.logger.debug(soup)
        images = [img.get('src') for img in soup.findAll('img') if not re.search("^\/", img.get('src'))]
        app.logger.debug(images)
        goal, bonus = len(images), 0
        file_count = 1
        for image in images:
            # TODO: The following steps are not fully implemented.
            # Check if the src pointed to actual images, or a web page
            # 1) regex to grab the file extension
            name, ext = path.splitext(image)
            # 2) if file extension exists, confirm it matches known image extensions.
            if ext:
                # extension = 'png'  # example, but actually set according to a.
                #   a) set the output filename to have the same file extension as original file.
                urllib.request.urlretrieve(image, f"{filename}_{file_count}.{ext}")
            else:
                # 3) if no file extension or doesn't match known extensions, assume a web page view.
                recur_goal, recur_found = _get_images(image, f"filename_{file_count}")
                goal += recur_goal
                bonus += recur_found
            file_count += 1
        return (goal, file_count + bonus)

    goal, found = _get_images(ig_url, filename)
    success = goal == found
    message = 'Files Saved! ' if success else "Error in Capture(s). "
    app.logger.debug(message)
    flash(message)
    answer = f"{filename}" if success else f"Failed. {success} "
    return answer


def capture(url=None, post=None, filename='screenshot'):
    """ Visits the permalink for give Post, creates a screenshot named the given filename. """
    ig_url = post.permalink if post else 'https://www.instagram.com/p/B4dQzq8gukI/'
    ig_url = url or ig_url
    answer = chrome_grab(ig_url, filename)
    # answer = phantom_grab(ig_url, filename)
    # answer = soup_no_chrome(ig_url, filename)
    return answer
