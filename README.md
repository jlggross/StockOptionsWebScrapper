# StockOptionsWebScrapper

O objetivo desse projeto é acessar diferentes webistes para coletar dados sobre opções da bolsa de valores brasileira. Para quem não sabe, opções são derivativos de ações (derivam das ações) e conferem a quem a **compra** o **direito** de comprar ou vender uma ação. Já quem **vende** a opção tem o **dever** de comprar ou vender a ação. 

Comentários, sugestões e pedidos de novos recursos são sempre bem vindos.

*Observação*: Por hábito o código foi escrito em Inglês.

## Fontes de dados

Por enquanto este projeto coleta informações de dois websites bem conhecidos entre investidores. O primeiro é o website https://opcoes.net.br/ no qual estão disponíveis a maioria das opções negociadas em bolsa que possuem alguma liquidez, sendo, portanto, uma excelente fonte de dados. Neste website os dados são apresentados em uma forma condensada e organizda que facilita a coleta.

O segundo é o webiste http://bvmf.bmfbovespa.com.br/formador-de-mercado/formador-opcoes.html, o site oficial da bolsa de valores brasileira, mantido pela empresa B3. Este website em particular disponibiliza para consulta todas as opções que possuem "formador de mercado" (FM), que significa que são opções que sempre terão liquidez, pois algum player de mercado é obrigado pelas regras da B3 a sempre comprar e vender determinada opção. Para o investidor saber quais são essas opções é interessantes, pois auxilia na tomada de decisão sobre comprar ou vender determinada opção, visto que havendo necessidade de reverter a operação haverá liquidez.

Um conjunto das opções apresentadas no site da B3 não estão disponíveis no site Opcoes.Net, então coletar os dados em ambos e agregá-los pode ser muito útil para ter o conjunto de opções à disposição (ou pelo menos a maior quantidade possível).

Outros websites ou outros tipos de dados sobre as opções podem ser adicionados no futuro para que a coleta de dados seja ainda mais completa.

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

## Pré-requisitos

Esse projeto necessita dos seguints recursos de software:
* Python 3 e pip3
* Chromedirver
* Selenium webdriver
* Pacotes 'pandas' e 'openpyxl'

Eu desenvolvi esse projeto no Windows 10, então os materiais apresentados a seguir são para esse sistema operacional. Porém se você estiver utilizando Linux ou Mac uma pesquisa rápida no Google vai te trazer tutoriais de como instalar esses softwares.

### Como instalar o Python 3 no Windows 10



