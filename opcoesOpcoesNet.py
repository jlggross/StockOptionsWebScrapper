from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

# From my files
from Checkbox import Checkbox
from RadioButton import RadioButton
from variables import serie_call
from variables import serie_put

"""
Function: 
    opcoesNet_collectStockTickers
Description: 
    Enters the website and collect all the available tickers that have
    options. 
Parameters:
    * driver : driver to access urls. 
Return:
    * tickers : Tickers from stocks that have options. 
"""
def opcoesNet_collectStockTickers(driver):
    # Enter website
    driver.get("https://opcoes.net.br/opcoes/bovespa")

    select_name = "IdAcao" # Name of the selector "Ativos"
    elements = driver.find_element_by_name(select_name)

    tickers = [element.strip() for element in elements.text.split('\n')]
    print(sorted(tickers[1:-1]))

    return sorted(tickers[1:-1])

"""
Function: 
    opcoesNet_getStockOptionsTickers
Description: 
    Enters the website and collect all the available stock options tickers.
Parameters:  
    * driver : Chromedriver to access a website.  
    * tickers : Tickers that the website has options for.
Return:
    * df_stockOptions : DataFrame with stock options from Opcoes.net. 
"""
def opcoesNet_getStockOptionsTickers(driver, tickers):
    # Create DataFrame for the derivatives
    df_stockOptions = pd.DataFrame(columns=["Ação", "Opção", "Série", "Mês",
                                            "Vencimento", "FM", "Tipo", "Mod.",
                                            "Strike"])

    for ticker in tickers:
        driver.get("https://opcoes.net.br/opcoes/bovespa/" + ticker)

        # Click checkboxes for deadlines and for ITM, ATM and OTM
        deadlines = ["v2020-08-17", "v2020-09-21", "v2020-10-19"]
        moneyzones = ["ITM_acima_de_15", "ITM_entre_5_e_15", "ATM_entre_5_e_5",
                      "OTM_entre_5_e_15", "OTM_acima_de_15"]
        for checkbox in (deadlines + moneyzones):
            try:
                checkboxObj = Checkbox(driver, checkbox)
                checkboxObj.click_checkbox()
            except:
                print(ticker, "- Error with checkbox", checkbox)
                pass

        # Click Radio button for all stock derivatives
        radioTodas = RadioButton(driver, "todas")
        radioTodas.click_radiobutton()

        # Explict waits the table to load - When checkbox is checked rows class='even' are created by JavaScript
        driver.implicitly_wait(3)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "even")))
        except TimeoutException:
            print("Timeout for ticker", ticker)
            continue

        # Loads table rows and headers (first two rows)
        # table = driver.find_element_by_id('tblListaOpc').get_attribute('innerHTML')
        tableOp = driver.find_element_by_id("tblListaOpc")
        rows = tableOp.find_elements(By.TAG_NAME, "tr")
        rows = rows[2:]  # Skip header

        print(ticker, ":", len(rows))

        # Populate DataFrame
        for row in rows:
            new_derivative = {}
            for i, cell in enumerate(row.find_elements(By.TAG_NAME, "td"), start=1):
                if i == 1:
                    new_derivative["Ação"] = ticker
                    new_derivative["Opção"] = cell.text
                    new_derivative["Série"] = cell.text[4]
                elif i == 2:
                    if cell.text == "✔":
                        new_derivative["FM"] = "Sim"
                    else:
                        new_derivative["FM"] = "Não"
                elif i == 3:
                    new_derivative["Tipo"] = cell.text.capitalize()
                    if new_derivative["Tipo"] == "Call":
                        new_derivative["Mês"] = serie_call[new_derivative["Série"]][0]
                        new_derivative["Vencimento"] = serie_call[new_derivative["Série"]][1]
                    elif new_derivative["Tipo"] == "Put":
                        new_derivative["Mês"] = serie_put[new_derivative["Série"]][0]
                        new_derivative["Vencimento"] = serie_put[new_derivative["Série"]][1]
                elif i == 4:
                    new_derivative["Mod."] = cell.text
                elif i == 5:
                    continue
                elif i == 6:
                    new_derivative["Strike"] = float(cell.text.replace(",", "."))
                else:
                    break
            df_stockOptions = df_stockOptions.append(new_derivative, ignore_index=True)

    return df_stockOptions