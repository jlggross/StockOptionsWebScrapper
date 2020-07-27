# StockOptionsWebScrapper

O objetivo desse projeto é acessar diferentes webistes para coletar dados sobre opções da bolsa de valores brasileira. Para quem não sabe, opções são derivativos de ações (derivam das ações) e conferem a quem a **compra** o **direito** de comprar ou vender uma ação. Já quem **vende** a opção tem o **dever** de comprar ou vender a ação. 

Comentários, sugestões e pedidos de novos recursos são sempre bem vindos.

*Observação*: Por hábito o código foi escrito em Inglês.

## Fontes de dados

Por enquanto este projeto coleta informações de dois websites bem conhecidos entre investidores. O primeiro é o website https://opcoes.net.br/ no qual estão disponíveis a maioria das opções negociadas em bolsa que possuem alguma liquidez, sendo, portanto, uma excelente fonte de dados. Neste website os dados são apresentados em uma forma condensada e organizda que facilita a coleta.

O segundo é o webiste http://bvmf.bmfbovespa.com.br/formador-de-mercado/formador-opcoes.html, o site oficial da bolsa de valores brasileira, mantido pela empresa B3. Este website em particular disponibiliza para consulta todas as opções que possuem "formador de mercado" (FM), que significa que são opções que sempre terão liquidez, pois algum player de mercado é obrigado pelas regras da B3 a sempre comprar e vender determinada opção. Para o investidor saber quais são essas opções é interessantes, pois auxilia na tomada de decisão sobre comprar ou vender determinada opção, visto que havendo necessidade de reverter a operação haverá liquidez.

Um conjunto das opções apresentadas no site da B3 não estão disponíveis no site Opcoes.Net, então coletar os dados em ambos e agregá-los pode ser muito útil para ter o conjunto de opções à disposição (ou pelo menos a maior quantidade possível).

Outros websites ou outros tipos de dados sobre as opções podem ser adicionados no futuro para que a coleta de dados seja ainda mais completa.

## Pré-requisitos

Esse projeto necessita dos seguints recursos de software:
* Python 3 e pip3
* Chromedirver
* Selenium webdriver
* Pacotes 'pandas' e 'openpyxl'

Eu desenvolvi esse projeto no Windows 10, então os materiais apresentados a seguir são para esse sistema operacional. Porém se você estiver utilizando Linux ou Mac uma pesquisa rápida no Google vai te trazer tutoriais de como instalar esses softwares.

### Instalar o Python 3 no Windows 10

Escrevi um tutorial detalhado do passo a passo para instalar o Python 3 no Windows 10 no LinkedIn. O artigo pode ser acessado pelo link https://www.linkedin.com/pulse/como-instalar-o-python-3-windows-10-jo%25C3%25A3o-gross/.

### Instalar o Chromedriver no Windows 10

Escrevi um tutorial com o passo a passo de como instalar o Chromedriver no Windows 10 no LinkedIn. O artigo pode ser acessado pelo link https://www.linkedin.com/pulse/como-instalar-o-chromedriver-windows-10-jo%25C3%25A3o-gross/.

### Instalar o Selenium no Windows 10

Escrevi um tutorial com o passo a passo de como instalar e testar o Selenium no Windows 10. O artigo está no LinkedIn e pode ser acesso pelo link https://www.linkedin.com/pulse/como-instalar-o-selenium-webdriver-windows-10-jo%25C3%25A3o-gross/?trackingId=cjHvNKvYjABYjH0VGHMFEg%3D%3D.

### Instalar pacotes pandas e openpyxl

Se você já seguiu os tutoriais anteriores, então basta entrar no cmd e digitar:

```pip3 install pandas openpyxl```

Utilizaremos o pandas para criar DataFrames e exportar os dados e o openpyxl para conseguir criar um arquivo .xlsx de destino.


## Tipos de dados

Cada website fornece informações únicas, porém algumas informações são comuns entre eles. Dentre as informações comuns aquelas que buscamos são apresentadas a seguir:

* **Ação**: Ticker (código) da ação na bolsa de valores.
* **Opção**: Ticker (código) da opção na bolsa de valores.
* **FM**: Formador de Mercado. Ou a opção possui formador de mercado ou não possui.
**Tipo**: A opção pode ser "Call" (opção de compra) ou "Put" (opção de venda).
**Strike**: É o preço de exercício da opção.
**Vencimento**: Data de vencimento da opção.

Abaixo você pode ser um exemplo do resultado da coleta do programa:

| **Ação** | **Opção** | **FM** | **Tipo** | **Strike** | **Vencimento** |
|:--------:|:---------:|:------:|:------:|:------:|:------:|
| ABEV3 | ABEVH11 | Não | Call | 11,08 | 17/08/2020 |
| ABEV3 | ABEVH14 | Sim | Call | 14,08 | 17/08/2020 |
| BRAP4 | BRAPH37 | Não | Call | 37 | 17/08/2020 |
| BRAP4 | BRAPH390 | Sim | Call | 39 | 17/08/2020 |
| ABEV3 | ABEVT232 | Não | Put | 22,83 | 17/08/2020 |
| AZUL4 | AZULT950 | Não | Put | 9,5 | 17/08/2020 |
| AZUL4 | AZULT152 | Não | Put | 15,25 | 17/08/2020 |

## Estrutura do projeto

O projeto possui um arquivo principal chamado de **main.py** que faz chamadas às funções de coleta de códigos de ações e códigos de opções e demais dados para os websites até o momento suportados. Cada webiste possui um arquivo em separado com as funções de coleta de dados específicas. As funções core do projeto são as seguintes:

*opcoesNet_collectStockTickers()* : Entra no website opcoes.net e coleta todos os tickers (códigos) das ações de possuem opções. Os tickers são utilizados posteriormente para acessar a página específica de cada ação com suas opções.

*opcoesNet_getStockOptionsTickers(stockTickers)* : A partir dos tickers de ações, entra na ágina de cada ação e coleta os tickers, strike, vencimento e tipo de todas as opções disponíveis daquela ação.

*b3_FM_collectStockTickers()* : Entra no website da B3 e coleta todos os tickers (códigos) das ações de possuem opções. Os tickers são utilizados posteriormente para acessar a página específica de cada ação com suas opções.

*b3_FM_getStockOptionsTickers(stockTickers)* : A partir dos tickers de ações, entra na ágina de cada ação e coleta os tickers, strike, vencimento e tipo de todas as opções disponíveis daquela ação.

## Apresentação dos dados

Após a coleta os dados são agregados em um único DataFrame e dados repetidos são excluídos. O DataFrame é dividido em outros dois, um para Calls e um para Puts e o conteúdo é exportado para uma planilha .xslx. O resultado da planilha pode ser visualizado na pasta raiz deste projeto.

## Configurações para acesso à página opcoes.net

O arquivo **optionsOpcoesNet.py** possui a função *opcoesNet_getStockOptionsTickers(stockTickers)* que realiza a coleta dos dados sobre opções. Nesta função há a variavel **deadlines** que descreve para quais vencimentos iremos pesquisar as opções. Fique atento a esta variável, pois ela precisa estar configurada com as strings dos vencimentos que você deseja coletar as opções, caso contrário a coleta vai dar errado.
