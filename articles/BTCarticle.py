import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

"""
Main
"""
driver = webdriver.Chrome()

xpath = "/html/body/app-root/div/app-variable-sale/section/app-variable-assets-list/section/div/div[2]/div/ul/li[1]"
df = pd.DataFrame(columns=["Ação", "Taxa %"])
url = "https://www.btgpactualdigital.com/renda-variavel/venda-descoberta"

driver.get(url)

# Wait element
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
except TimeoutException:
    print("Timeout!")

driver.implicitly_wait(3)
elements = driver.find_elements_by_xpath(xpath[:-3])
print("Collecting BTC:")
for i, element in enumerate(elements):
    if len(element.text) < 11:
        continue
    newElement = {}
    newElement["Ação"] = element.text.split("\n")[0]
    newElement["Taxa %"] = element.text.split("\n")[1]
    print(i, newElement)
    df = df.append(newElement, ignore_index=True)

df["Taxa %"] = df["Taxa %"].str.replace(",", ".")
df["Taxa %"] = df["Taxa %"].str.replace("%", "")
df["Taxa %"] = df["Taxa %"].astype('float')

print("\n")
print("Info about BTC data From BTG Pactual:")
print(df.info())

print("\n")
print("Conteúdo do DataFrame")
print(df)