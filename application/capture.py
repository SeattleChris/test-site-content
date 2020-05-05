from flask import flash, current_app as app
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from .errors import InvalidUsage
import time
import re
from os import path
from random import randint
from pprint import pprint

# VALID_POST_TYPE = {'STORY': True}
IG_EMAIL = app.config.get('IG_EMAIL')
IG_PASSWORD = app.config.get('IG_PASSWORD')


def wait(val):
    """ Adds a time.sleep period. Input can either be a float or a string matching our semantic duration lables. """

    def _r(a, b):
        """ Inputs are measured in tenths of a second. Output is a float value measured in seconds. """
        return randint(a * 100, b * 100) / 1000  # in Python 3, always returns a float.

    semantic_duration = {'quick': _r(1, 8), 'short': _r(11, 17), 'med': _r(19, 31), 'long': _r(41, 55)}
    if isinstance(val, (int, float)):
        val = max(0.06, val)
        a = ((val * 0.95) + (val - 0.1)) / 2
        b = ((val * 1.05) + (val + 0.1)) / 2
        val = _r(a, b)
    elif isinstance(val, str) and val in semantic_duration:
        val = semantic_duration[val]
    else:
        raise ValueError(f"The wait function input of {val} was not a number or correct semantic string value. ")

    time.sleep(val)
    return True


def setup_chromedriver(headless=True):
    """ Returns a driver object to be used for navigating websites. """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument("--remote-debugging-port=9222")
        # options.binary_location = chromedriver.chromedriver_filename
        # chrome_executable_path = '/usr/bin/google-chrome'
    chromedriver_path = 'chromedriver' if app.config.get('LOCAL_ENV') else '/usr/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver_path, options=options)
    # app.logger.info("=========================== Setup chrome driver ===========================")
    return driver


def ig_login(driver, current_page=True, ig_email=IG_EMAIL, ig_password=IG_PASSWORD):
    """ Login to Instagram. This is required to view Story posts. """
    if not current_page:
        driver.get('https://www.instagram.com/accounts/login/')
    wait('quick')  # Let the page finish loading.
    # app.logger.info('============== InstaGram Login ===================')
    attempts, form_inputs = 5, []
    while attempts and not form_inputs:
        attempts -= 1
        try:
            form_inputs = driver.find_elements_by_css_selector('form input')
            if not form_inputs:
                raise NoSuchElementException('Not yet. ')
            app.logger.info(f"Form inputs found! On Attempt: {5 - attempts} ")
            app.logger.info(f"Have {len(form_inputs)} form inputs for ig_login. ")
        except NoSuchElementException as e:
            app.logger.info(f"Exception for target_button: {attempts} left. ")
            if not attempts:
                app.logger.error(e)
            else:
                wait('quick')
        except Exception as e:
            app.logger.error("Exception in ig_login. ")
            app.logger.error(e)
            driver.quit()
            raise e
    if form_inputs:
        email_input = form_inputs[0]
        password_input = form_inputs[1]
        email_input.send_keys(ig_email)
        password_input.send_keys(ig_password)
        password_input.send_keys(Keys.ENTER)
    success = len(form_inputs) > 0
    return driver, success


def story_click(driver):
    """ Do the necessary browser actions for a story post. """
    # app.logger.info('============== story_click ================')
    # all_buttons = driver.find_elements_by_tag_name('button')
    # desired_div_inside_button = driver.find_element_by_xpath("//button/descendant::div[text()='Tap to play']")
    # desired_div_inside_button = driver.find_element_by_xpath("//button/descendant::div[contains(., 'Tap to play')]")
    # target_button = desired_div_inside_button.find_element_by_xpath("ancestor::button")
    wait('long')  # Let the page finish loading.
    attempts, success = 5, False
    while attempts and not success:
        attempts -= 1
        try:
            # TODO: Maybe try a different approach for our target.
            target_button = driver.find_element_by_xpath("//button[@type='button']")
            app.logger.info('*@*@*@*@*@*@*@*@*@*@*@*@*@*@* TARGET BUTTON *@*@*@*@*@*@*@*@*@*@*@*@*@*@*')
            # pprint(dir(target_button))
            # app.logger.debug('-------------------------------------------------------------------------')
            # pprint(vars(target_button))
            success = True
        except NoSuchElementException as e:
            app.logger.info(f"Exception for target_button: {attempts} left. ")
            if not attempts:
                app.logger.error(e)
            else:
                wait('quick')
        except Exception as e:
            app.logger.error("Exception in story_click. ")
            app.logger.error(e)
            driver.quit()
            raise e
    if success:
        target_button.click()
    # ? TODO: Emulate clicking in text box to freeze image? //textarea[@placeholder='Send Message']
    return driver, success


def capture_img(filename, driver, media_type=''):
    """ For a given page, capture the images in the img tags. """
    # app.logger.info('================= capture_img =====================')
    files, error_files, message, count, error_count = [], [], '', 0, 0
    dur = 'short' if media_type == 'STORY' else 'quick'
    temp = f"{filename}_full.png"
    wait(dur)
    success = driver.save_screenshot(temp)
    if success:
        files.append(temp)
    else:
        error_files.append(temp)
        error_count += 1
        count -= 1
    # app.logger.info(f"Start of count at {count + 1}. Successful screenshot: {success}. ")
    soup = bs(driver.page_source, 'html.parser')
    # TODO: Determine if we can do this without BeautifulSoup processes.
    target = [img.get('src') for img in soup.findAll('img') if not re.search("^\/", img.get('src'))]
    for ea in target:
        count += 1
        temp = f"{filename}_{count}.png"
        try:
            driver.get(ea)
            wait(dur)
            success = driver.save_screenshot(temp)
            # capture_screenshot_to_string()
            # driver.get_screenshot_as_base64()
            if not success:
                raise Exception("Screenshot not saved. ")
            files.append(temp)
        except Exception as e:
            message += f"Error on file # {count} . "
            error_count += 1
            error_files.append(temp)
            app.logger.error(e)
    success = error_count == 0
    message += 'Files Saved! ' if success else "Error in Screen Grab. "
    app.logger.info(message)
    answer = {'success': success, 'message': message, 'file_list': files, 'error_files': error_files}
    return answer


def chrome_grab(ig_url, filename, media_type, headless=True):
    """ Using selenium webdriver with Chrome and grabing the file from the page content. """
    # headless = False  # TODO: Usually set as True. Only set to False to visually watch when running locally.
    app.logger.info(f"================= chrome_grab with headless as {headless} ================")
    success, answer = True, {}
    driver = setup_chromedriver(headless=headless)
    app.logger.info('-------------------- chrome_grab -----------------')
    pprint(driver)
    driver.get(ig_url)
    if media_type == 'STORY':
        driver, success = ig_login(driver, current_page=True)
        if success:
            app.logger.info('We have an InstaGram login. ')
        else:
            app.logger.error("The IG login FAILED! ")
    if media_type == 'STORY' and success:
        success = False
        driver, success = story_click(driver)
        app.logger.info(f"========== story_click response: {success} ==========")
    if success:
        answer = capture_img(filename, driver)
        # app.logger.info("------ capture_img gave a response ------")
    else:
        message = f"The story_click function had an issue. "
        answer = {'success': success, 'message': message, 'file_list': [], 'error_files': []}
    app.logger.info("Finishing chrome grab. ")
    pprint(answer)
    driver.quit()  # driver.close() to close tab? driver.exit() to end browser?
    return answer


def soup_no_chrome(ig_url, filename, media_type):
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


def capture(url, filename, media_type='STORY'):
    """ Visits the permalink for give Post, creates a screenshot named the given filename. """
    if not isinstance(media_type, str):
        raise InvalidUsage("The media_type must be a string. ")
    media_type = media_type.upper()
    if not url or not filename:
        raise InvalidUsage("You must have a url and a filename. ")
    answer = chrome_grab(url, filename, media_type)
    # answer = soup_no_chrome(ig_url, filename, media_type)
    return answer
