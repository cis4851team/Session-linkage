from selenium import webdriver
import requests
import calendar
import random
import os
from time import sleep

def execute_test_plan(driver):
    # Shorter name for convenience
    get_elem = driver.find_element_by_css_selector

    # Construct fake identity for testing
    print("constructing fake identity")
    driver.get("https://www.fakenamegenerator.com/gen-random-us-us.php")
    identity = {}
    name = get_elem("div.address > h3").text
    identity["firstname"] = name.split(' ')[0]
    identity["lastname"] = name.split(' ')[2]
    fullAddress = get_elem("div.adr").text.splitlines()
    identity["address"] = fullAddress[0]
    identity["city"] = fullAddress[1].split(',')[0]
    identity["state"] = fullAddress[1].split(',')[1][1:3]
    identity["zip"] = fullAddress[1].split(',')[1][4:]
    identity["country"] = "United States of America"
    values = driver.find_elements_by_tag_name("dd")
    identity["phone"] = values[3].text
    birthday = values[5].text
    identity["birthday-month"] = list(calendar.month_name).index(birthday.split(' ')[0])
    identity["birthday-day"] = int(birthday.split(' ')[1][:-1])
    identity["birthday-year"] = int(birthday.split(' ')[2])
    identity["age"] = int(values[6].text.split(' ')[0])
    identity["email"] = values[8].text.splitlines()[0]
    identity["username"] = values[9].text
    identity["password"] = values[10].text

    # # Now start browsing plan. get request:
    # print("going to google")
    # driver.get("https://www.google.com")
    # random_word = random.choice(open("dictionary.txt").readlines())
    # get_elem('input[name="q"]').send_keys(random_word)
    # sleep(1)

    print("resetting advertising site tuples")
    driver.get("https://evil-third-party.herokuapp.com/reset")
    sleep(1)

    # get request
    print("going to PII GET page")
    driver.get("https://pii-contact-form.herokuapp.com/")
    get_elem('#form-name').send_keys(identity["firstname"] + " " + identity["lastname"])
    get_elem('#form-email').send_keys(identity["email"])
    get_elem('#form-phone').send_keys(identity["phone"])
    get_elem('#form-subject').send_keys('Test Subject')
    get_elem('#form-message').send_keys('Test message')
    get_elem('button').click()
    sleep(1)

    # # post request
    # print("going to PII POST page")
    # driver.get("https://pii-private-browsing-test-site.herokuapp.com/")
    # get_elem('input[name="first_name"]').send_keys(identity["firstname"])
    # get_elem('input[name="last_name"]').send_keys(identity["lastname"])
    # get_elem('input[name="address"]').send_keys(identity["address"])
    # get_elem('input[name="email"]').send_keys(identity["email"])
    # get_elem('input[name="dob"]').send_keys("{}/{}/{}".format(identity["birthday-month"], identity["birthday-day"], identity["birthday-year"]))
    # get_elem('input[type="submit"]').click()
    # sleep(1)
    
    # get request
    print("going to whistleblower site")
    driver.get("https://pii-whistleblower-site.herokuapp.com/")
    if enter_hackers_group:
        get_elem('#form-message').send_keys('hackers_group')
        get_elem('button').click()
        sleep(5)
    else:
        get_elem('#form-name').send_keys('asdf')
        get_elem('button').click()
        sleep(1)

    print('navigating to heroku data explorer')
    driver.get("https://heroku-data-explorer.herokuapp.com/")
    get_elem('.btn-lg').click()
    sleep(1)
    sleep(5)
    driver.find_elements_by_class_name("connection")[1].click()
    sleep(5)
    get_elem('li[data-item-id="public_fingerprint_tuples"').click()
    sleep(1)
    get_elem('.dx-icon-export-excel-button').click()
    sleep(1)
    os.rename(os.path.expanduser('~/Downloads/export.xlsx'), os.path.expanduser('~/Downloads/fingerprints.xlsx'))
    get_elem('li[data-item-id="public_url_tuples"').click()
    sleep(1)
    get_elem('.dx-icon-export-excel-button').click()
    sleep(1)
    os.rename(os.path.expanduser('~/Downloads/export.xlsx'), os.path.expanduser('~/Downloads/urls.xlsx'))

    # # send email
    # print("sending email")
    # driver.get("https://accounts.google.com/signin/v2/sl/pwd?service=mail")
    # sleep(1)
    # driver.switch_to.active_element.send_keys(email_address + '\n')
    # sleep(1)
    # driver.switch_to.active_element.send_keys(password + '\n')
    # sleep(5)
    # driver.switch_to.active_element.send_keys('c')
    # driver.switch_to.active_element.send_keys(identity["email"] + '\t')
    # sleep(0.3)
    # driver.switch_to.active_element.send_keys('\t')
    # driver.switch_to.active_element.send_keys('Secret Message')
    # driver.switch_to.active_element.send_keys('\t')
    # driver.switch_to.active_element.send_keys('The password is {}'.format(identity["password"]))
    # driver.switch_to.active_element.send_keys('\t\n')
    # sleep(3)

def main():
    if test_regular:
        print("Doing testing plan with regular browser")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = test_headless
        with webdriver.Chrome(chrome_options=chrome_options) as driver:
            execute_test_plan(driver)
        
    if test_incognito:
        print("Doing testing plan with incognito browser")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--incognito')
        chrome_options.headless = test_headless
        with webdriver.Chrome(chrome_options=chrome_options) as driver:
            execute_test_plan(driver)
    
    if test_guest:    
        print("Doing testing plan with guest mode browser")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--bwsi')
        chrome_options.headless = test_headless
        with webdriver.Chrome(chrome_options=chrome_options) as driver:
            execute_test_plan(driver)


if __name__ == "__main__":
    test_headless = False
    test_regular = True
    test_incognito = False
    test_guest = False
    enter_hackers_group = True
    main()