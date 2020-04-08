from flask import flash, current_app as app
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from .errors import InvalidUsage
import time
import re
from os import path


def chrome_grab(ig_url, filename):
    """ Using selenium webdriver with Chrome and grabing the file from the page content. """
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument("--remote-debugging-port=9222")
    # options.binary_location = chromedriver.chromedriver_filename
    # chrome_executable_path = '/usr/bin/google-chrome'
    chromedriver_path = 'chromedriver' if app.config.get('LOCAL_ENV') else '/usr/bin/chromedriver'
    driver = webdriver.Chrome(chromedriver_path, chrome_options=options)
    app.logger.info("=========================== Set driver in chrome_grab ===========================")
    files, error_files, message, count, error_count = [], [], '', 0, 0
    driver.get(ig_url)
    temp = f"{filename}_full.png"
    success = driver.save_screenshot(temp)
    if success:
        files.append(temp)
    else:
        error_files.append(temp)
        error_count += 1
        count -= 1
    app.logger.debug(f"Start of count at {count + 1}. ")
    soup = bs(driver.page_source, 'html.parser')
    # TODO: Determine if we can do this without BeautifulSoup processes.
    target = [img.get('src') for img in soup.findAll('img') if not re.search("^\/", img.get('src'))]
    for ea in target:
        count += 1
        time.sleep(1)
        temp = f"{filename}_{count}.png"
        try:
            driver.get(ea)
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
            app.logger.exception(e)
    success = error_count == 0
    message += 'Files Saved! ' if success else "Error in Screen Grab. "
    app.logger.debug(message)
    answer = {'success': success, 'message': message, 'file_list': files, 'error_files': error_files}
    # driver.close()  # Needed?
    driver.quit()  # Needed? or driver.exit()
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


def capture(url, filename):
    """ Visits the permalink for give Post, creates a screenshot named the given filename. """
    ig_url = url or 'https://www.instagram.com/p/B4dQzq8gukI/'
    if not url or not filename:
        raise InvalidUsage("You must have a url and a filename. ")
    answer = chrome_grab(ig_url, filename)
    # answer = soup_no_chrome(ig_url, filename)
    return answer
