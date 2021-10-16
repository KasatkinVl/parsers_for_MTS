from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


options = Options()
options.headless = False
webdriver_path = ''
driver = webdriver.Chrome(options=options, executable_path=webdriver_path)
result = pd.DataFrame()


driver.get("https://live.mts.ru/moskva/cinema")


# Пролистываем до низа страницы
elem = driver.find_elements_by_xpath('//*[contains(text(),"Показать ещё")]')
while len(elem) > 0:
    try:
        elem = driver.find_element_by_xpath('//*[contains(text(),"Показать ещё")]')
        try:
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            # elem.location_once_scrolled_into_view
            driver.execute_script("window.scrollTo(0, -500)")
            elem.click()
            elem = driver.find_elements_by_xpath('//*[contains(text(),"Показать ещё")]')

        except StaleElementReferenceException:
            elem = []
    except NoSuchElementException:
        elem = []

movie_card = []
movie_card = driver.find_elements_by_class_name("CardV2-module__content--3EYkM")

movie_titles = []
cinema_count = []

for i in movie_card:
    if (len(i.find_elements_by_class_name('CardV2-module__more--2MHZJ')) > 0)\
            and (i.find_element_by_class_name('CardV2-module__more--2MHZJ').text != 'Читать далее'):
        movie_titles.append(i.find_element_by_class_name('CardV2-module__title--rXlHe').text)
        cinema_count.append(int(i.find_element_by_class_name('CardV2-module__more--2MHZJ').text[5:-11]))

print(movie_titles)
print(cinema_count)



df1 = pd.DataFrame(movie_titles,
                  columns=['movie_titles']
                  )
df2 = pd.DataFrame(cinema_count,
                  columns=['cinema_count']
                  )


result = df1.join(df2)
result = result.sort_values('cinema_count', ascending=False)\
               .reset_index()\
               .drop(columns=['index']).drop_duplicates().head(30)


print(result)
driver.quit()