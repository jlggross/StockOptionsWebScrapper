"""
Author: João Luiz Grave Gross
LinkedIn: https://www.linkedin.com/in/jlggross/
GitHub: https://github.com/jlggross
Email: joaolggross@gmail.com

About this project: This project aims to access different websites in order to collect data from
stock options, a type of stock derivative. For now the web scrapping is done for two websites well
known by many investors when it comes to have access to stock options information.

The first website is https://opcoes.net.br/ where almost all options are covered. This website
covers mainly stocks and stock options that have some liquidity, being a good source of information.
The data presented in the website is condensed in a way that makes scrapping easier.

The seconds website is http://bvmf.bmfbovespa.com.br/formador-de-mercado/formador-opcoes.html, the official
stock market website from B3 company. This particular URL makes available all the options that are "market
formers", or in portuguese "Formador de Mercado", which means that this options have always some liquidity
provided by a selection of players in the market.

The thing is that a set of options found in the B3 website are not covered in Opcoes.Net, so collecting data
from both and aggregating can be very useful to have the hole set of options available (or at least as many as possible).

Some other webistes or URLs may be added in the future to make the data collection even more complete.

Comments, suggestions and requests for new features are always welcomed.

P.S.: This project has been written in English, but you can communicate with me in Portuguese if you prefer.
"""

# Other important packages
import pandas as pd
from datetime import datetime

# My files
from optionsOpcoesNet import opcoesNet_collectStockTickers, opcoesNet_getStockOptionsTickers
from optionsB3 import b3_FM_collectStockTickers, b3_FM_getStockOptionsTickers

"""
Function:
    exportDFToExcel
Description:
    Export the DataFrames to a .xlsx file
Parameters: 
    * *args : Variable number of DataFrames.
"""
def exportDFToExcel(*args):

    df_calls = pd.DataFrame()
    df_puts = pd.DataFrame()

    for df in args:
        df_calls = df_calls.append(df[df["Tipo"] == "Call"])
        df_puts = df_puts.append(df[df["Tipo"] == "Put"])

    df_calls.drop_duplicates(subset="Opção", keep="first", inplace=True)
    df_calls.reset_index(drop=True, inplace=True)
    df_puts.drop_duplicates(subset="Opção", keep="first", inplace=True)
    df_puts.reset_index(drop=True, inplace=True)

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    with pd.ExcelWriter("opcoes" + current_time + ".xlsx") as writer:
        columns = ["Ação", "Opção", "FM", "Tipo", "Strike", "Vencimento"]
        df_calls[columns].to_excel(writer, sheet_name="Call")
        df_puts[columns].to_excel(writer, sheet_name="Put")

"""
Main - Where everything starts. 
"""
if "__main__" == __name__:

    # Web scrape stock options in Opcoes.net
    print("Web Scrapping: Opcoes.net")
    stockTickers = opcoesNet_collectStockTickers()
    df_opcoesNet = opcoesNet_getStockOptionsTickers(stockTickers)

    # Web scrape stock options in B3
    print("\n")
    print("Web Scrapping: B3 FM")
    stockTickers = b3_FM_collectStockTickers()
    df_B3_FM = b3_FM_getStockOptionsTickers(stockTickers)

    # Export DataFrame to .xlsx
    print(df_opcoesNet[["Ação", "Opção", "FM", "Tipo", "Strike", "Vencimento"]])
    print(df_B3_FM[["Ação", "Opção", "FM", "Tipo", "Strike", "Vencimento"]])

    exportDFToExcel(df_opcoesNet, df_B3_FM)