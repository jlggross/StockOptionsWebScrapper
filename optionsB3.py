from selenium import webdriver
import pandas as pd

"""
Function: 
    b3_FM_createWebdriver
Description: 
    Creates a Chromedriver to surf the web and provides a driver
    that can be manipulated to access the website's content. 
Return:
    * driver : Chromedriver to access a website.  
"""
def b3_FM_createWebdriver():
    # Create driver with Chromedriver
    driver = webdriver.Chrome()
    driver.set_window_position(2000, 0)
    driver.minimize_window()
    # driver.maximize_window()

    return driver

"""
Function: 
    b3_FM_collectStockTickers
Description: 
    Enters the website and collect all tickers that have options with Market Former
    (Formador de Mercado - FM).  
Return:
    * tickers : Tickers from stocks that have options with FM.
"""
def b3_FM_collectStockTickers():
    # Create driver and enter page
    driver = b3_FM_createWebdriver()
    driver.get("http://bvmf.bmfbovespa.com.br/formador-de-mercado/formador-opcoes.html")

    # Get stocks tickers
    elements = driver.find_elements_by_class_name("primary-text")
    tickers = [element.text.split(" ")[0] for element in elements]
    tickers = tickers[4:]
    print(sorted(tickers))

    # Close Chromedriver
    driver.quit()

    return sorted(tickers)

"""
Function: 
    b3_FM_getStockOptionsTickers
Description: 
    Enters the website and collect all the available stock options tickers that have 
    Market Former (Formador de Mercado - FM).  
Parameters:  
    * tickers : Tickers that the website has options for 
Return:
    * df_FM_options : DataFrame with stock options from B3 that have FM
"""
def b3_FM_getStockOptionsTickers(tickers):
    base_url = "http://bvmf.bmfbovespa.com.br/formador-de-mercado/formador-opcoes-detalhe.html?asset="

    # Create driver
    driver = b3_FM_createWebdriver()

    # Create DataFrame
    df_FM_options = pd.DataFrame(columns=["Ação", "Opção", "Tipo", "Strike", "Vencimento", "FM"])

    for ticker in tickers:
        driver.get(base_url + ticker)

        calls = driver.find_element_by_id("tbdetalheOpCall")
        calls = calls.text.split("\n")[2:]
        calls = [call + " Call" for call in calls]

        puts = driver.find_element_by_id("tbdetalheOpPut")
        puts = puts.text.split("\n")[2:]
        puts = [put + " Put" for put in puts]

        callsputs = calls + puts
        print(ticker, len(callsputs))
        for option in callsputs:
            tokens = option.split(" ")
            new_ticker = {}
            new_ticker["Ação"] = ticker
            new_ticker["Opção"] = tokens[0]
            new_ticker["Strike"] = float(tokens[1].replace(",", ""))
            new_ticker["Vencimento"] = tokens[2]
            new_ticker["Tipo"] = tokens[3]
            new_ticker["FM"] = "Sim"
            df_FM_options = df_FM_options.append(new_ticker, ignore_index=True)

    # Close Chromedriver
    driver.quit()

    return df_FM_options