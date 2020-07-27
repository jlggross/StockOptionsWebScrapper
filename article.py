from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

class Checkbox:

    def __init__(self, driver, checkbox_id):
        self.checkbox_id = checkbox_id
        self.driver = driver
        self.checkbox = driver.find_element_by_id(checkbox_id)

    def get_id(self):
        return self.checkbox_id

    def is_enabled(self):
        return self.driver.execute_script(
            "return document.getElementById('{}').checked".format(self.checkbox_id))

    def click_checkbox(self):
        if not self.is_enabled():
            self.checkbox.click()

class RadioButton:

    def __init__(self, driver, radiobutton_id):
        self.radiobutton_id = radiobutton_id
        self.driver = driver
        self.radiobutton = driver.find_element_by_id(radiobutton_id)

    def get_id(self):
        return self.radiobutton_id

    def click_radiobutton(self):
        self.radiobutton.click()

serie_call = {
    'A': ('01-Jan', '2020-01-20'),
    'B': ('02-Fev', '2020-02-17'),
    'C': ('03-Mar', '2020-03-16'),
    'D': ('04-Abr', '2020-04-20'),
    'E': ('05-Mai', '2020-05-18'),
    'F': ('06-Jun', '2020-06-15'),
    'G': ('07-Jul', '2020-07-20'),
    'H': ('08-Ago', '2020-08-17'),
    'I': ('09-Set', '2020-09-21'),
    'J': ('10-Out', '2020-10-19'),
    'K': ('11-Nov', '2020-11-16'),
    'L': ('12-Dez', '2020-12-21')
}

serie_put = {
    'M': ('01-Jan', '2020-01-20'),
    'N': ('02-Fev', '2020-02-17'),
    'O': ('03-Mar', '2020-03-16'),
    'P': ('04-Abr', '2020-04-20'),
    'Q': ('05-Mai', '2020-05-18'),
    'R': ('06-Jun', '2020-06-15'),
    'S': ('07-Jul', '2020-07-20'),
    'T': ('08-Ago', '2020-08-17'),
    'U': ('09-Set', '2020-09-21'),
    'V': ('10-Out', '2020-10-19'),
    'W': ('11-Nov', '2020-11-16'),
    'X': ('12-Dez', '2020-12-21')
}

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def exportarExcel(df):
    df.drop_duplicates(subset="Opção", keep="first", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_excel("opcoesLREN3.xlsx")

def coletaDados(driver, ticker):
    tableOp = driver.find_element_by_id("tblListaOpc")
    rows = tableOp.find_elements(By.TAG_NAME, "tr")
    rows = rows[2:]  # Ignora o header da tabela

    # Adiciona dados ao DataFrame
    df_stockOptions = pd.DataFrame(columns=["Ação", "Opção", "Tipo", "Strike", "Série", "Vencimento"])
    for row in rows:
        new_derivative = {}
        for i, cell in enumerate(row.find_elements(By.TAG_NAME, "td"), start=1):
            if i == 1:
                new_derivative["Ação"] = ticker
                new_derivative["Opção"] = cell.text
                new_derivative["Série"] = cell.text[4]
            elif i == 3:
                new_derivative["Tipo"] = cell.text.capitalize()
                if new_derivative["Tipo"] == "Call":
                    new_derivative["Vencimento"] = serie_call[new_derivative["Série"]][1]
                elif new_derivative["Tipo"] == "Put":
                    new_derivative["Vencimento"] = serie_put[new_derivative["Série"]][1]
            elif i == 2 or i == 4 or i == 5:
                continue # Segue para próxima iteração
            elif i == 6:
                new_derivative["Strike"] = float(cell.text.replace(",", "."))
            else:
                break
        df_stockOptions = df_stockOptions.append(new_derivative, ignore_index=True)
    return df_stockOptions


# Cria o driver para navegar na web
driver = webdriver.Chrome()

# Define todos os tickers de ações
tickers = ["LREN3"] # <--- inserir mais tickers aqui

for ticker in tickers:
    # Acessa o website para o ticker
    driver.get("https://opcoes.net.br/opcoes/bovespa/" + ticker)

    # Define os ids dos checkboxes dos vencimentos
    idVencimentos = ["v2020-08-17", "v2020-09-21"]
    # Define os ids dos checkboxes das distâncias de strike
    idDistStrikes = ["ITM_acima_de_15", "ITM_entre_5_e_15",
                     "ATM_entre_5_e_5", "OTM_entre_5_e_15",
                     "OTM_acima_de_15"]
    idsCheckboxes = idVencimentos + idDistStrikes
    for elementID in idsCheckboxes:
        checkboxElem = Checkbox(driver, elementID)
        checkboxElem.click_checkbox()

    # Define o id do radiobutton 'todas'
    radioTodas = RadioButton(driver, "todas")
    radioTodas.click_radiobutton()

    df_opcoes = coletaDados(driver, ticker)
    exportarExcel(df_opcoes)
    print(df_opcoes)
    driver.quit()