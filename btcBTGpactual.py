import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

"""
Function:
    BTGpactual_get99percentileDF
Description:
    Get the DataFrame with data values below the 99th percentile.
Parameters:
    * df : DataFrame with the original data.
Return:
    * df99 : DataFrame with data below the 99th percentile.
References:
    * Distribution of values and boxplot (1): https://medium.com/dayem-siddiqui/understanding-and-interpreting-box-plots-d07aab9d1b6c
    * Distribution of values and boxplot (2): https://www.wellbeingatschool.org.nz/information-sheet/understanding-and-interpreting-box-plots
"""
def BTGpactual_get99percentileDF(df):

    # Define percentiles so we can see how the data is distributed
    description = df.describe(percentiles=[.25, .5, .75, .9, .95, .99])
    description_dict = description.to_dict()

    # Get the value which delimits 99% of the samples in the DataFrame
    data_cut = float(description_dict["Taxa %"]["99%"])

    # Print the percentiles to get and overview of the data
    #print(description)

    # Select 99% of the samples, thus removing the outliers
    df99 = df[df["Taxa %"] <= data_cut]
    #print("Original DataFrame: ", df["Taxa %"].count())
    #print("Selected DataFrame:", df99["Taxa %"].count())

    return df99

"""
Function:
    BTGpactual_printBTCdata
Description:
    Plot the DataFrame data.
Requirements:
    > pip3 install matplotlib 
    > pip3 install seaborn
Parameters:
    * df_btcBTG : DataFrame with data.
"""
def BTGpactual_printBTCdata(df, bins):

    df99 = BTGpactual_get99percentileDF(df)

    # Specify which plots to show
    myplots = ["99percentile_scatter", "99percentile_distribution"]

    # Plotting
    sns.set_style("white")
    fig, ax = plt.subplots(1, len(myplots), figsize=(6*len(myplots), 6))
    for i, oneplot in enumerate(myplots):
        if len(myplots) == 1:
            my_ax = ax
        else:
            my_ax = ax[i]

        if oneplot == "scatter-matplotlib":
            g1 = df.plot.scatter(x="Ação", y="Taxa %", c="Taxa %", colormap="viridis", ax=my_ax)
            g1.set(xticklabels=[])

        if oneplot == "scatter-seaborn":
            g2 = sns.relplot(x="Ação", y="Taxa %",
                    data=df, kind="scatter",
                    size="Taxa %", hue="Taxa %",  ax=my_ax)
            g2.set(xticklabels=[])

        if oneplot == "99percentile_distribution":
            # First line of the plot
            g3 = sns.distplot(df99["Taxa %"], ax=my_ax, kde=True, hist=False)

            # Second line of the plot
            my_ax2 = my_ax.twinx()
            sns.distplot(df99["Taxa %"], ax=my_ax2, kde=False, hist=True, bins=bins, norm_hist=False)

            # Name axis
            g3.xaxis.set_major_locator(ticker.MultipleLocator((df99["Taxa %"].max()-df99["Taxa %"].min())/bins))
            g3.set_ylabel("Qtde")
            now = datetime.now()
            g3.set_title("BTC BTG Pactual - " + now.strftime("%Y-%m-%d %H:%M"))
            plt.setp(my_ax.get_xticklabels(), rotation=45)

            #g3.set_xticklabels(labels=g3.get_xticklabels())
            # yticks = np.arange(11, 17, 0.5).tolist()

        if oneplot == "99percentile_scatter":
            cmap = sns.cubehelix_palette(rot=-.4, as_cmap=True)
            g4 = sns.scatterplot(x="Ação", y="Taxa %",
                                hue="Taxa %", size="Taxa %",
                                palette=cmap,
                                data=df99,
                                ax=my_ax)
            g4.set(xticklabels=[])
            g4.set_xlabel("Ações")
            g4.yaxis.set_major_locator(ticker.MultipleLocator(1))
            g4.set_title("Taxas de BTC a.a no BTG Pactual")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # g1.set(xticklabels=[]) - Sem valores no eixo X
    # g1.set(xlabel=None) - Sem nome de eixo no eixo x

"""
Function:
    BTGpactual_printTreemap
Description:
    Plot the DataFrame data in a treemap
Requirements:
    > pip3 install plotly
Parameters:
    * df_btcBTG : DataFrame with data.
    * bins : Define the number of groups to categorize the data.
References:
    * Treemap Charts in Python: https://plotly.com/python/treemaps/
"""
def BTGpactual_printTreemap(df, bins):
    # Simple treemap
    fig1 = px.treemap(df, path=["Ação"], values="Taxa %", color="Ação")
    fig1.show()

    # Elaborate treemap
    df99 = BTGpactual_get99percentileDF(df)

    # Create categories
    min_value = df99["Taxa %"].min()
    max_value = df99["Taxa %"].max()
    bin_interval = (max_value - min_value) / bins
    ranges = [bin_interval * i for i in range(bins + 2)]
    group_names = ["Group" + str(i + 1) for i in range(bins + 1)]

    # Prepare treemap
    df99["Group"] = pd.cut(df99["Taxa %"], bins=ranges, labels=group_names)
    df99["BTC"] = "BTC"  # In order to have a single root node
    fig = px.treemap(df99, path=["BTC", "Group", "Ação"], values="Taxa %", color="Ação")

    fig.show()

"""
Function:
    BTGpactual_getBTC
Description:
    Collect the BTC taxes annual taxes from BTG Pactual website.
Parameters:
    * driver : Chromedriver to access a website.
Return:
    * df : DataFrame with BTC per stock.
"""
def BTGpactual_getBTC(driver):
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

    print("Info about BTC data From BTG Pactual:")
    print(df.info())

    return df

