from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
# import win32gui, win32con

# hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hide,win32con.SW_HIDE)

def criarWebDriver(tipoDriver):
	"""Evita de que, quando esteja analisando e fazendo o download do webdriver, se alguma verificação de segurança será considerada"""
	os.environ['WDM_SSL_VERIFY']='0'
	global opcoes
	global driver
	driver = escolherWebDriver(tipoDriver.upper())
	

def escolherWebDriver(driverString):
    opcoes = {
       	'CHROME': criarChromeDriver,
       	'EDGE': criarEdgeDriver,
       	'FIREFOX':criarFirefoxDriver,
    }
    return opcoes.get(driverString)()

def criarChromeDriver():
	opcoes = webdriver.ChromeOptions()
	opcoes.add_argument("start-maximized")
	opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
	return webdriver.Chrome(ChromeDriverManager(path=os.getcwd()).install(),options=opcoes)

def criarFirefoxDriver():
	return webdriver.Firefox(GeckoDriverManager(path=os.getcwd()).install())

def criarEdgeDriver():
	opcoes = Options()
	opcoes.add_argument("start-maximized")
	return webdriver.Edge(EdgeChromiumDriverManager(path=os.getcwd()).install(),options=opcoes)


def verificarDOMCarregado():
    carregado = False
    while carregado == False:
        estadoAtual = driver.execute_script('return window.document.readyState')
        if estadoAtual != 'complete':
            sleep(1)
        else:
            carregado = True

def centralizarElemento(elemento):
	acoes = ActionChains(driver)
	acoes.move_to_element(elemento).perform()

def navegarPara(URL):
	driver.get(URL)
	verificarDOMCarregado()
	print('carregou')

def pegaElementopeloXPath(elementoXPath):
	return driver.find_element_by_xpath(elementoXPath)

def clicaElementopeloXPath(elementoXPath):
	elemento = getElementByXPath(elementoXPath)
	acoes = ActionChains(driver)
	acoes.click(elemento).perform()
	verificarDOMCarregado()

def pegaConteudopeloAtributo(elemento,tipoAtributo):
	valor=''
	# consideraremos quando o parâmetro for vazio, para capturar o textContent como default
	if len(tipoAtributo.strip())==0:
		valor = elemento.get_attribute('textContent')
	else:
		valor = elemento.get_attribute(tipoAtributo)
	return valor
