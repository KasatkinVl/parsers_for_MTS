from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
webdriver_path = ''
driver = webdriver.Chrome(options=options, executable_path=webdriver_path)

# Сюда передаём список id артистов из алиаса на Я.Музыке
artist_id = {
    3976197, 4356483, 5098446, 4480055, 1554548, 6207325, 6229247, 4464750, 158454,
    1556385, 3879764, 5850853, 404281, 3892062, 4017435, 4944386, 4611844, 3502567,
    249991, 4443004, 5940317, 3821347, 3836355, 6456325, 426302, 424985, 167026, 31203,
    5652191, 41174, 158058, 167085, 430993, 167353, 156426, 5780809, 189548, 41221, 165131,
    9078726, 159015, 755171, 41052, 168851, 4370377, 155917, 975699, 3292790, 4101345, 1636897,
    6625670, 4773324, 6676267, 445029, 218333, 6103852, 2630560, 2403276, 234192, 168852, 6996012,
    391868, 167053, 6424360
}
result = pd.DataFrame()

# Перебираем артистов из списка
for id in artist_id:
    driver.get("https://music.yandex.ru/artist/{id}/info".format(id=id))

    # проверяем наличие и закрываем заглушку о подписке на Яндекс Плюс
    if len(driver.find_elements_by_xpath(
            './/div/div[@class="payment-plus__header-close js-close payment-plus__header-close-rainbow"]')) > 0:
        driver.find_element_by_xpath(
            './/div/div[@class="payment-plus__header-close js-close payment-plus__header-close-rainbow"]').click()

    # Находим блок с прослушиваниями, прокручиваем экран до него, кликаем и раскрываем список
    elem = driver.find_element_by_xpath('//*[contains(text(),"Слушателей")]')
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    driver.find_element_by_xpath('//*[contains(text(),"Слушателей")]').click()



    # Определение месяца прослушиваний
    month = []
    month = driver.find_elements_by_class_name("graph__bar-caption")

    month_list = []
    for i in month:
        month_list.append(i.text)


    # Определение количества прослушиваний
    total_count = []
    total_count = driver.find_elements_by_class_name("graph__bar-count")

    total_count_list = []
    for i in total_count:
        total_count_list.append(i.text)

    listenings_month = ['Пр_' + str(i) for i in month_list]


    # Закрываем список с прослушиваниями, переходим к списку лайков
    driver.find_element_by_xpath('//*[contains(text(),"Слушателей")]').click()
    elem_likes = driver.find_element_by_xpath('//*[contains(text(),"Лайков")]')
    driver.execute_script("arguments[0].scrollIntoView();", elem_likes)
    driver.find_element_by_xpath('//*[contains(text(),"Лайков")]').click()


    # Определение месяца лайков
    month_likes = []
    month_likes = driver.find_elements_by_class_name("graph__bar-caption")

    month_list_likes = []
    for i in month_likes:
        month_list_likes.append(i.text)


    # Определение количества лайков
    total_count_likes = []
    total_count_likes = driver.find_elements_by_class_name("graph__bar-count")

    total_count_likes_list = []
    for i in total_count_likes:
        total_count_likes_list.append(i.text)

    likes_month = ['Лайки ' + str(i) for i in month_list_likes]

    # Сохраняем имя артиста с анализируемой страницы
    artist_name = []
    artist_name.append(driver.find_element_by_class_name("page-artist__title").text)

    # Создаём DF-мы для прослушиваний/лайков и объединяем их
    df1 = pd.DataFrame(np.array(total_count_list),
                      columns=artist_name,
                      index=listenings_month)
    df2 = pd.DataFrame(np.array(total_count_likes_list),
                      columns=artist_name,
                      index=likes_month)
    concat_df = pd.concat([df1, df2])

    # Присоединяем DF по артисту к результирующему DF
    result = result.join(concat_df, how='right')

print(result)
result.to_csv('result2.csv')

driver.quit()
