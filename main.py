#!/usr/bin/env python3

from re import L
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json
import time
from pyvirtualdisplay import Display

LOCAL_PATH = ''
REAL_LINK_WORK_UA = []

WORK_UA = []

display = Display(visible=0, size=(800, 600))
display.start()

options = Options()
options.add_argument("window-size=1200,600")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
ua = UserAgent(verify_ssl=False)
user_agent = ua.random
print(user_agent)
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options,
                          executable_path=LOCAL_PATH + '/chrome_driver/chromedriver')

def change_display():
    display = Display(visible=0, size=(800, 600))
    display.start()

    options = Options()
    options.add_argument("window-size=1200,600")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options,
                          executable_path=LOCAL_PATH + '/chrome_driver/chromedriver') 

def parse_work_ua():
    try:
        URL = 'https://www.work.ua/jobs/?ss=1'
        time.sleep(2)
        driver.get(url=URL)
        btn = driver.find_element_by_id('pjax-job-list').find_element_by_class_name('add-top').get_attribute(
            'innerHTML')
        pagg_num = ''
        for e in btn.strip():
            try:
                int(e)
                pagg_num = pagg_num + e
            except:
                break
        pagg_num = round(int(pagg_num) / 13)
        print(pagg_num)
        calc = 0
        for i in range(pagg_num):
            change_display()
            URL = f'https://www.work.ua/jobs/?page={i}'
            driver.get(url=URL)
            for el in driver.find_elements_by_tag_name('h2'):
                link = el.find_element_by_tag_name('a').get_attribute('href')
                temp_link = {"link": f"{link}"}
                calc += 1
                print(f"{temp_link} Cyrcle {calc}")
                REAL_LINK_WORK_UA.append(temp_link)
            driver.close()
            driver.quit()    

    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()
        with open(LOCAL_PATH + '/last_work_ua_links.json', 'w', encoding="utf-8") as file:
            file.write(json.dumps(REAL_LINK_WORK_UA))
        state = 1
    driver.close()
    driver.quit()         
    return state       


def parse_single_work_ua():
    try:
        with open(LOCAL_PATH + '/new_add_work_ua_links.json', 'r') as file:
            all_links = json.load(file)
            calc = 0
            cycl = 0
            ######### test #############
            text = 'test'
            with open(LOCAL_PATH + '/test.txt', 'w') as f:
                f.write(text)
            ######## text #############

            for link in all_links:
                change_display()
                if calc == 1000:
                    with open(LOCAL_PATH + "/work_ua_draft.json", 'w', encoding="utf-8") as file:
                        file.write(json.dumps(WORK_UA))
                    calc = 0
                try:
                    calc += 1
                    cycl += 1
                    print(f"{cycl} page parsed ---- all pages {len(all_links)}")
                    URL = f'{link["link"]}'
                    driver.get(url=URL)
                    try:
                        btn_click = driver.find_element_by_class_name(
                            'link-phone').click()
                    except Exception as err:
                        number = "Non Info"
                    # time.sleep(2)
                    try:
                        try:
                            number = driver.find_element_by_id('contact-phone').find_element_by_tag_name(
                                'a').get_attribute(
                                'innerHTML')
                        except Exception as err:
                            number = driver.find_element_by_id(
                                'contact-phone').text
                    except Exception as err:
                        number = "Non Info"

                    title = driver.find_element_by_id(
                        'h1-name').get_attribute('innerHTML')

                    try:
                        salary = driver.find_element_by_xpath(
                            "//b[@class='text-black']").get_attribute('innerHTML')
                    except Exception as arr:
                        salary = "Non Info"
                    try:
                        address = driver.find_element_by_xpath(
                            "/html/body/section[@id='center']/div[@class='container']/div[@class='row row-print']/div"
                            "[@class='col-md-8 col-left']/div[3]/div[@class='card wordwrap']/p[@class='text-indent"
                            " add-top-sm'][1]")
                        name_add = ''
                        print(address.txt)
                        for el in address.text:
                            if el != ".":
                                name_add = name_add + el
                            else:
                                break

                    except Exception as err:
                        address = driver.find_element_by_xpath(
                            "/html/body/section[@id='center']/div[@class='container']/div[@class='row row-print']/div"
                            "[@class='col-md-8 col-left']/div[3]/div[@class='card wordwrap']/p[@class='text-indent"
                            " add-top-sm'][1]")
                        name_add = ''
                        address = address.text
                        for el in address:
                            if el != ".":
                                name_add = name_add + el
                            else:
                                break

                    except Exception as err:
                        address = 'Non Info'

                    try:
                        try:
                            fl = driver.find_element_by_xpath(
                                "/html/body/section[@id='center']/div[@class='container']/div[@class='row row-print']/"
                                "div[@class='col-md-8 col-left']/div[3]/div[@class='card wordwrap']/p[@class='text-indent"
                                " add-top-sm'][3]").text
                        except Exception as err:
                            fl = driver.find_element_by_xpath(
                                "/html/body/section[@id='center']/div[@class='container']/"
                                "div[@class='row row-print']/div[@class='col-md-8 col-left']/div[3]/div"
                                "[@class='card wordwrap']/p[@class='text-indent add-top-sm'][2]").text
                    except Exception as err:
                        fl = 'Non Info'

                    try:
                        descp = driver.find_element_by_id(
                            'job-description').get_attribute('innerHTML')
                    except Exception as err:
                        descp = "Non Info"
                    try:
                        category = driver.find_element_by_xpath(
                            "/html/body/section[@id='center']/div[@class='container']/div[@class='row row-print']/div[@class='col-md-8 col-left']/div[@class='design-verse']/div[@class='card wordwrap']/p[@class='text-indent text-muted add-top-sm'][2]/span[@class='add-top-xs']")
                        clean_category = ''
                        for item in category.text:
                            if item != ';':
                                clean_category = clean_category + item

                    except Exception as err:
                        category = driver.find_element_by_xpath(
                            "/html/body/section[@id='center']/div[@class='container']/div[@class='row row-print']/div[@class='col-md-8 col-left']/div[3]/div[@class='card wordwrap']/p[@class='text-indent text-muted add-top-sm']/span[@class='add-top-xs']")
                        clean_category = ''
                        for item in category.text:
                            if item != ';':
                                clean_category = clean_category + item
                    except Exception as err:
                        print(err)
                        clean_category = "Non Info"

                    temp_work_ua = {
                        'title': f'{title}',
                        'salary': f'{salary}',
                        'category': f'{clean_category}',
                        'number': f'{number}',
                        'address': f'{address}',
                        'props': f'{fl}',
                        'description': f'{descp}',
                        'link': link["link"]
                    }

                    WORK_UA.append(temp_work_ua)
                    print(temp_work_ua)
                    print(f"Parsed link: {link['link']}")
                except Exception as err:
                    print(err)
                    continue

                driver.close()
                driver.quit() 
    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()
        with open(LOCAL_PATH + "/send_work_ua_draft.json", 'w', encoding="utf-8") as file:
            file.write(json.dumps(WORK_UA))
        with open(LOCAL_PATH + "/work_ua_draft.json", 'a', encoding="utf-8") as file:
            file.write(json.dumps(WORK_UA))
        state = 3        
    return state     


def fiter_links_work_ua():
    with open(LOCAL_PATH + "/last_work_ua_links.json", 'r') as file:
        last_links = json.load(file)
    with open(LOCAL_PATH + "/work_ua_links.json", 'r') as f:
        all_links = json.load(f)

    NEW_LINKS = []
    DELETE_LINKS = []

    for link in last_links:
        if link not in all_links:
            NEW_LINKS.append(link)
    for link in all_links:
        if link not in last_links:
            DELETE_LINKS.append(link)
    copy_all_links = all_links

    for link in DELETE_LINKS:
        if link in all_links:
            copy_all_links.remove(link)
            continue

    for link in NEW_LINKS:
        if link not in copy_all_links:
            copy_all_links.append(link)
    print(f"___ ADD NEW LINK ____ {len(NEW_LINKS)}")
    print(f"___ DELETE LINKS ____ {len(DELETE_LINKS)}")
    print(f"___ ACTUAL LINKS ____ {len(copy_all_links)}")
    with open(LOCAL_PATH + '/new_add_work_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(NEW_LINKS))
    with open(LOCAL_PATH + '/delete_work_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(DELETE_LINKS))
    with open(LOCAL_PATH + '/work_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(copy_all_links))
    state = 2
    return state    


def formating_data_work_ua():
    global data_frame_vac
    with open(LOCAL_PATH + "/parse_to_erobota_cat.json") as file:
        all_category = json.load(file)
    with open(LOCAL_PATH + "/send_work_ua_draft.json") as file:
        all_vacancy = json.load(file)
    with open(LOCAL_PATH + "/koatuu.json") as file:
        all_regions = json.load(file)
    with open(LOCAL_PATH + "/job_type.json") as file:
        all_types = json.load(file)

    FILTERED_VAC = []
    cat_work = []
    n = 0
    print(len(all_vacancy))
    for vacancy in all_vacancy:
        for cat in all_category:
            vacancy_filt = vacancy['category'].lower()
            # print(vacancy_filt)
            clean_vac = ''
            for item in vacancy_filt:
                try:
                    str(item)
                    if item != ",":
                        clean_vac = clean_vac + item
                    else:
                        break
                except Exception as err:
                    break

            if clean_vac in cat['work_ua'].lower():
                # print(clean_vac)
                frame_vac = {
                    "is_active": 'true',
                    "name": "",  # tile
                    "contact_name": "Null",
                    "location": {
                        "string": "",
                        "ids": {}
                    },
                    "created_by": "import",
                    "formattedPhone": "",
                    "job_type": [100, 200],  # занятість
                    "salary": {
                        "min": "",
                        "max": "",
                        "string": ""
                    },
                    "description": "",
                    "cat_id": 2,
                    "location_string": "",
                    "contact_phone": "",
                    "location_ids": []
                }
                frame_vac['cat_id'] = cat['id']

                vacancy['filt_cat'] = "complete"

                for region in all_regions:
                    parse_address = vacancy['address'].lower()
                    clear_add = ""
                    for item in parse_address:
                        if item != ",":
                            clear_add = clear_add + item

                        else:
                            break
                    if region['n'].strip().lower() == clear_add:
                        temp_loc = ''
                        for i in vacancy['address']:
                            if i != '·':
                                temp_loc = temp_loc + i
                            else:
                                break
                        frame_vac['location']['string'] = temp_loc
                        frame_vac['location']['ids']['l_2'] = region['l_2']
                        frame_vac['location']['ids']['l_1'] = region['l_1']
                        frame_vac['location']['ids']['l_3'] = region['l_3']
                        frame_vac['location_string'] = temp_loc
                        frame_vac['location_ids'].append(region['l_1'])
                        frame_vac['location_ids'].append(region['l_2'])
                        frame_vac['location_ids'].append(region['l_3'])

                        clean_num = vacancy['number'].strip()
                        clean_num = clean_num.replace("+", "")
                        clean_num = clean_num.replace("(", "")
                        clean_num = clean_num.replace(")", "")
                        clean_num = clean_num.replace("-", "")
                        clean_num = clean_num.strip()
                        if clean_num[0] == "0":
                            clean_num = '38' + clean_num
                        elif clean_num == "Показати телефон" or clean_num == "Non Info" or clean_num == "<span>Показати телефон</span>":
                            clean_num = "Null"
                        frame_vac['formattedPhone'] = clean_num
                        frame_vac['contact_phone'] = clean_num
                        frame_vac['link'] = vacancy['link']

                        salary = vacancy['salary']
                        if salary == "Non Info":
                            salary = "Null"
                            frame_vac['salary'] = salary
                            frame_vac['min_salary'] = salary
                            frame_vac['max_salary'] = salary
                        else:
                            try:
                                salary = vacancy['salary'].split()
                                min_salary = salary[0] + salary[1]
                                max_salary = salary[3] + salary[4]
                                frame_vac['salary'] = max_salary
                                frame_vac['min_salary'] = min_salary
                                frame_vac['max_salary'] = max_salary
                            except Exception as err:
                                salary = vacancy['salary'].split()
                                salary = salary[0] + salary[1]
                                frame_vac['salary'] = salary
                                frame_vac['min_salary'] = "Null"
                                frame_vac['max_salary'] = "Null"

                        frame_vac['name'] = vacancy['title']
                        frame_vac['description'] = vacancy['description']
                        if frame_vac not in FILTERED_VAC:
                            FILTERED_VAC.append(frame_vac)
                            n += 1
                            print(f"doing {n} file circle")
    # print(cat_work)
    with open(LOCAL_PATH + "/filtered_vac_work.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(FILTERED_VAC))
    len(FILTERED_VAC)
    state = 4
    return state


def parse_robota_ua():
    LINK_ROBOTA_UA = []
    for i in range(1, 34):
        change_display()
        try:
            try:
                URL = f'https://rabota.ua/ua/zapros/all/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0?parentId={i}'
                driver.get(url=URL)
                pagg = driver.find_element_by_class_name('santa-typo-h2').text
                pagg = pagg.split()
                all_pagg = pagg[0] + pagg[1]
                num_pagg = round(int(all_pagg) / 40)
            except Exception as err:
                URL = f'https://rabota.ua/ua/zapros/all/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0?parentId={i}'
                driver.get(url=URL)
                pagg = driver.find_element_by_class_name('santa-typo-h2').text
                pagg = pagg.split()
                all_pagg = pagg[0]
                num_pagg = round(int(all_pagg) / 40)

            calc = 0
            for pagg_page in range(num_pagg):
                URL = f'https://rabota.ua/ua/zapros/all/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0?parentId={i}&page={pagg_page}'
                driver.get(url=URL)
                links = driver.find_elements_by_class_name('card')
                for item in links:
                    link = item.get_attribute('href')
                    temp_el = {"link": f"{link}",
                               "patern": f"{i}"}
                    LINK_ROBOTA_UA.append(temp_el)
                    calc += 1
                    print(
                        f'Parse link -- {calc}/{num_pagg*40} --- {link} -- patern -- {i}')
                        
            with open(LOCAL_PATH + "/last_robota_ua_links.json", 'w', encoding="utf-8") as f:
                f.write(json.dumps(LINK_ROBOTA_UA))            

        except Exception as err:
            print(err)

        driver.close()
        driver.quit()    

    with open(LOCAL_PATH + "/last_robota_ua_links.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(LINK_ROBOTA_UA))
    state = 5
    driver.close()
    driver.quit()
    return state    


def parse_single_robota_ua():
    display = Display(visible=0, size=(800, 600))
    display.start()

    options = Options()
    options.add_argument("window-size=1200,600")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    ua = UserAgent(verify_ssl=False)
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=options,
                          executable_path=LOCAL_PATH + '/chrome_driver/chromedriver')
    print('________ START _______')
    with open(LOCAL_PATH + '/new_add_robota_ua_links.json', 'r') as file:
        all_links = json.load(file)
    BASE_VAC_DATA = []
    cal = 0
    c = 0
    for link in all_links:
        change_display()
        try:
            url = link["link"].replace(
                'https://rabota.ua/', 'https://rabota.ua/ua/')
            URL = f'{url}'
            driver.get(url=URL)
            try:
                driver.find_element_by_xpath(
                    "//*[@data-id='show-contact-button']").click()
                number = driver.find_element_by_xpath(
                    "//*[@data-id='vacancy-contact-phone']").get_attribute("innerHTML")
            except Exception as err:
                number = "Null"

            try:
                title = driver.find_element_by_xpath(
                    "//*[@data-id='vacancy-title']").text
                # print(title)
            except Exception as err:
                print(err)

            salary = ''
            try:
                salary = driver.find_element_by_xpath(
                    "//*[@data-id='vacancy-salary-from-to']").text

            except Exception as err:
                if len(salary) == 0:
                    try:

                        salary = driver.find_element_by_xpath(
                            "//*[@data-id='vacancy-salary']").text
                    except Exception as err:
                        salary = "Null"

            try:
                city = driver.find_element_by_xpath(
                    "//*[@data-id='vacancy-city']").text
                # print(city)
            except Exception as err:
                city = "Null"

            try:
                descp = driver.find_element_by_id(
                    'description-wrap').get_attribute('innerHTML')
                # print(descp)
            except Exception as err:
                descp = "Null"

            try:
                temp_frame = {
                    'title': f'{title}',
                    'link': f"{url}",
                    'paternId': f"{link['patern']}",
                    'phone': f"{number}",
                    'salary': f"{salary}",
                    'city': f"{city}",
                    'descp': f"{descp}"
                }
                BASE_VAC_DATA.append(temp_frame)
                cal += 1
                c += 1
                status = f'--- {c}/{len(all_links)} el. --- parsed link --- {url} '
                with open(LOCAL_PATH + '/check.txt', 'a') as f:
                    f.write(f'{status}')
                if cal == 300:
                    with open(LOCAL_PATH + '/send_robota_ua_draft.json', 'w', encoding="utf-8") as file:
                        file.write(json.dumps(BASE_VAC_DATA))
                        cal = 0
            except Exception as err:
                print(err)
                continue

            driver.close()
            driver.quit()

        except Exception as err:
            print(err)

    with open(LOCAL_PATH + '/send_robota_ua_draft.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(BASE_VAC_DATA))
    with open(LOCAL_PATH + '/robota_ua_draft.json', 'a', encoding="utf-8") as file:
        file.write(json.dumps(BASE_VAC_DATA)) 
    state = 7
    driver.close()
    driver.quit()
    return state       


def fiter_links_robota_ua():
    with open(LOCAL_PATH + "/last_robota_ua_links.json", 'r') as file:
        last_links = json.load(file)
    with open(LOCAL_PATH + "/robota_ua_links.json", 'r') as f:
        all_links = json.load(f)

    NEW_LINKS = []
    DELETE_LINKS = []

    for link in last_links:
        if link not in all_links:
            NEW_LINKS.append(link)
    for link in all_links:
        if link not in last_links:
            DELETE_LINKS.append(link)
    copy_all_links = all_links

    for link in DELETE_LINKS:
        if link in all_links:
            copy_all_links.remove(link)
            continue

    for link in NEW_LINKS:
        if link not in copy_all_links:
            copy_all_links.append(link)

    with open(LOCAL_PATH + '/new_add_robota_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(NEW_LINKS))
    with open(LOCAL_PATH + '/delete_robota_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(DELETE_LINKS))
    with open(LOCAL_PATH + '/robota_ua_links.json', 'w', encoding="utf-8") as file:
        file.write(json.dumps(copy_all_links))
    state = 6
    return state    


def formating_data_robota_ua():
    FILTERED_VAC_ROBOTA_UA = []
    n = 0
    with open(LOCAL_PATH + '/send_robota_ua_draft.json', 'r') as file:
        all_vacancy = json.load(file)
    with open(LOCAL_PATH + "/parse_to_erobota_cat.json") as file:
        all_category = json.load(file)
    with open(LOCAL_PATH + "/koatuu.json") as file:
        all_regions = json.load(file)
    with open(LOCAL_PATH + "/job_type.json") as file:
        all_types = json.load(file)

    for vacancy in all_vacancy:
        robota_temp = {
            "is_active": 'true',
            "name": "",  # tile
            "contact_name": "Null",
            "location": {
                "string": "",
                "ids": {}
            },
            "created_by": "import",
            "formattedPhone": "",
            "job_type": [100, 200],  # занятість
            "salary": {
                "min": "",
                "max": "",
                "string": ""
            },
            "description": "",
            "cat_id": 2,
            "location_string": "",
            "contact_phone": "",
            "location_ids": []
        }
        for cat in all_category:
            if vacancy['paternId'] == cat['robota_ua']:
                robota_temp['cat_id'] = cat['id']
                break

        for region in all_regions:
            if vacancy['city'].lower() == region['n'].lower():
                robota_temp['location']['string'] = vacancy['city']
                robota_temp['location']['ids']['l_2'] = region['l_2']
                robota_temp['location']['ids']['l_1'] = region['l_1']
                robota_temp['location']['ids']['l_3'] = region['l_3']
                robota_temp['location_string'] = vacancy['city']
                robota_temp['location_ids'].append(region['l_1'])
                robota_temp['location_ids'].append(region['l_2'])
                robota_temp['location_ids'].append(region['l_3'])
                break

        if vacancy['phone'] == 'Null':
            clean_num = 'Null'
        else:
            clean_num = vacancy['phone'].replace('&nbsp;', '')

        robota_temp['formattedPhone'] = clean_num
        robota_temp['contact_phone'] = clean_num
        robota_temp['link'] = vacancy['link']

        salary = vacancy['salary']
        if salary == "Non Info":
            salary = "Null"
            robota_temp['salary'] = salary
            robota_temp['min_salary'] = salary
            robota_temp['max_salary'] = salary
        else:
            try:
                salary = vacancy['salary'].split()
                min_salary = salary[0] + salary[1]
                max_salary = salary[3] + salary[4]
                robota_temp['salary'] = max_salary
                robota_temp['min_salary'] = min_salary
                robota_temp['max_salary'] = max_salary
            except Exception as err:
                salary = vacancy['salary'].split()
                try:
                    salary = salary[0] + salary[1]
                    robota_temp['salary'] = salary
                    robota_temp['min_salary'] = "Null"
                    robota_temp['max_salary'] = "Null"
                except Exception as err:
                    salary = "Null"
                    robota_temp['salary'] = salary
                    robota_temp['min_salary'] = salary
                    robota_temp['max_salary'] = salary

        robota_temp['name'] = vacancy['title']
        robota_temp['description'] = vacancy['descp']
        if robota_temp not in FILTERED_VAC_ROBOTA_UA:
            FILTERED_VAC_ROBOTA_UA.append(robota_temp)
            n += 1
            print(f" -- Doing {n}/{len(all_vacancy)} -- {robota_temp} \n")

    with open(LOCAL_PATH + "/filtered_vac_robota_ua.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(FILTERED_VAC_ROBOTA_UA))
    print(f'\n'
          f'Filt. --- {len(FILTERED_VAC_ROBOTA_UA)} elements \n\n'
          f'Status: sucsess!')
    state = 8
    return state      


def parse_trud_com():
    try:
        URL = 'https://ua.trud.com/ua/ownpage/job/886862.html'
        driver.get(url=URL)
        time.sleep(2)
        btn_click = driver.find_element_by_class_name('phone-button').click()
        time.sleep(1)
        number = driver.find_element_by_class_name('phone-button').find_element_by_class_name(
            'phone-code').get_attribute('innerHTML')
        print(number)

    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()


def parse_nowa_robota_ua():
    try:
        URL = 'https://novarobota.ua/vacancy/vodiy-mizhnarodnik-71208'
        driver.get(url=URL)
        time.sleep(2)
        number = driver.find_element_by_class_name('phone_number_hide').find_element_by_tag_name('span').get_attribute(
            'data-value')
        print(number)

    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()


# def remove_vacancy():
#     with open (LOCAL_PATH + "/delete_robota_ua_links.json") as file:
#         base_links = json.load(file)
#         delete_temp = []
#         l = 0
#         for item in base_links:
#             l += 1
#             clean_link = item['link'].replace(
#                 'https://rabota.ua/', 'https://rabota.ua/ua/')
#             temp_el = {"link":f"{clean_link}"}
#             delete_temp.append(temp_el)
#             if l >= 100:
#                 URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/remove/"
#                 req = requests.post(URL_send, json=delete_temp)
#                 print(req.text)
#                 delete_temp.clear()
#                 l = 0
#             else:
#                 continue    
#     URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/remove/"
#     req = requests.post(URL_send, json=delete_temp)
#     print(req.text)
               
#     with open (LOCAL_PATH + "/delete_work_ua_links.json") as file:
#         base_links = json.load(file)
#         delete_temp = []
#         l = 0
#         for item in base_links:
#             l += 1
#             delete_temp.append(item)
#             if l >= 100:
#                 URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/remove/"
#                 req = requests.post(URL_send, json=delete_temp)
#                 print(req.text)
#                 delete_temp.clear()
#                 l = 0
#             else:
#                 continue
#     URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/remove/"
#     req = requests.post(URL_send, json=delete_temp)
#     print(req.text)
#     state = 9
#     return state  


# def send_vacation():
#     with open(LOCAL_PATH + "/filtered_vac_work.json", 'r') as file:
#         all_filt_vac = json.load(file)
#         send_base = []
#         temp = 0
#         k = 0
#         for item in all_filt_vac:
#             temp += 1
#             if temp <= 100:
#                 send_base.append(item)
#             else:
#                 k += 1
#                 print(f"Sending {k}/{round(len(all_filt_vac) / 100)} block")
#                 URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/import/"
#                 req = requests.post(URL_send, json=send_base)
#                 print(req)
#                 send_base.clear()
#                 temp = 0

#     print(f"Sending {k}/{round(len(all_filt_vac) / 100)} block")
#     URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/import/"
#     req = requests.post(URL_send, json=send_base)
#     print(req)

#     with open(LOCAL_PATH + "/filtered_vac_robota_ua.json", 'r') as file:
#         all_filt_vac = json.load(file)
#         send_base = []
#         temp = 0
#         k = 0
#         for item in all_filt_vac:
#             temp += 1
#             if temp <= 100:
#                 send_base.append(item)
#             else:
#                 k += 1
#                 print(f"Sending {k}/{round(len(all_filt_vac) / 100)} block")
#                 URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/import/"
#                 req = requests.post(URL_send, json=send_base)
#                 print(req)
#                 send_base.clear()
#                 temp = 0 

#     print(f"Sending {k}/{round(len(all_filt_vac) / 100)} block")
#     URL_send = "https://us-central1-erobota-ua.cloudfunctions.net/api/vacancies/import/"
#     req = requests.post(URL_send, json=send_base)
#     print(req)
#     state = 10
#     return state                       



def finish():
    #while True:
    print('Finish script')
    time.sleep(5000)
    state = 0
    driver.close()
    driver.quit()
    return state


if __name__ == "__main__":
    state = 0
    try:
        while True:
            if state == 0:
                state = parse_work_ua()
            elif state == 1:    
                state = fiter_links_work_ua()
            elif state == 2:    
                state = parse_single_work_ua()
            elif state == 3:    
                state = formating_data_work_ua()
            elif state == 4:
                state = parse_robota_ua()
            elif state == 5:    
                state = fiter_links_robota_ua()
            elif state == 6:    
                state = parse_single_robota_ua()
            elif state == 7:     
                state = formating_data_robota_ua()
            # elif state == 8:
            #     state = remove_vacancy()
            # elif state == 9:    
            #     state = send_vacation()
            elif state == 10:
                state = finish()
    except Exception as err:
        with open(LOCAL_PATH + '/script_errros.txt', 'a') as file:
            file.write(f'\n\n --------- STATE [ {state} ] ------------- \n{err} ')    
    
