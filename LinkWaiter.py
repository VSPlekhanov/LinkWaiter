if __name__ == '__main__':
    import re
    import time
    import win10toast

    from selenium import webdriver

    lecture_number = int(input('lecture number:'))
    current_day = int(input('Current day:'))

    if lecture_number < 1 or lecture_number > 8:
        raise Exception('invalid lecture number: ' + str(lecture_number))

    if current_day < 1 or current_day > 31:
        raise Exception('invalid day: ' + str(current_day))

    current_day = str(current_day)
    lecture_number = str(lecture_number)

    driver = webdriver.Chrome(r'drivers\chromedriver.exe')
    driver.get('https://lk.sut.ru/')

    # login
    login = driver.find_element_by_name("users")
    login.send_keys(input('enter your email: '))
    password = driver.find_element_by_name("parole")
    password.send_keys(input('enter your password: '))
    logButton = driver.find_element_by_name('logButton')
    logButton.click()

    # go to schedule
    time.sleep(1)
    collapse = driver.find_element_by_tag_name('div.title_item.collapsed')
    collapse.click()

    schedule = driver.find_element_by_id('menu_li_807')
    time.sleep(1)
    schedule.click()

    time.sleep(2)
    table_elemetns = driver.find_elements_by_xpath('/html/body/div/div/table[2]/tbody/tr')

    curr_day_id = None
    for id, el in enumerate(table_elemetns):
        if el.text and re.match('\w+\n\d+.\d+.\d+', el.text) and el.text.split('\n')[1][:2] == current_day:
            curr_day_id = id

    if curr_day_id is None:
        raise Exception('Cannot find current day in schedule!')

    curr_lecture_id = None
    for i in range(curr_day_id, min(curr_day_id + 6, len(table_elemetns))):
        if table_elemetns[i].text[0] == lecture_number:
            curr_lecture_id = i

    if curr_lecture_id is None:
        raise Exception('Cannot find current lecture in schedule!')

    toaster = win10toast.ToastNotifier()
    link_is_here = False
    while not link_is_here:
        try:
            driver.refresh()
            time.sleep(1)
            collapse = driver.find_element_by_tag_name('div.title_item.collapsed')
            collapse.click()

            schedule = driver.find_element_by_id('menu_li_807')
            time.sleep(1)
            schedule.click()

            time.sleep(2)
            table_elemetns = driver.find_elements_by_xpath('/html/body/div/div/table[2]/tbody/tr')
            lecture_row_text = table_elemetns[curr_lecture_id].text
            if lecture_row_text[-6:] == 'Ссылка':
                print('Link is ready')
                link_is_here = True
                toaster.show_toast('Python', 'Link is ready!')
                # todo: send notification
                pass
            elif lecture_row_text[-14:] == 'Начать занятие':
                toaster.show_toast('Python', 'You can begin the lecture!!')
                print('You can begin the lecture')
                # todo: send notification
            else:
                print(time.asctime().split()[3] + ' : ' + 'link is still not here...')
        except Exception:
            print(time.asctime().split()[3] + ' : ' + 'Exception... (maybe site is too slow)')
            pass
        time.sleep(10)
    driver.close()
