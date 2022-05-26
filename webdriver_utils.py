from selenium import webdriver
from selenium.webdriver.edge.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
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


def aguardarPagina():
    done_state = False
    while done_state == False:
        state = driver.execute_script('return window.document.readyState')
        if state != 'complete':
            sleep(1)
        else:
            done_state = True

def centralizarElemento(element):
	actions = ActionChains(driver)
	actions.move_to_element(element).perform()

def navegarPara(URL):
	driver.get(URL)
	waitPageLoad()

def pegaElementopeloXPath(elementoXPath):
	return driver.find_element_by_xpath(elementoXPath)

def clicaElementopeloXPath(elementoXPath):
	elemento = getElementByXPath(elementoXPath)
	actions = ActionChains(driver)
	actions.click(elemento).perform()
	waitPageLoad()

def pegaConteudopeloAtributo(elemento,tipoAtributo):
	valor=''
	# consideraremos quando o parâmetro for vazio, para capturar o textContent como default
	if len(tipoAtributo.strip())==0:
		valor = elemento.get_attribute('textContent')
	else:
		valor = elemento.get_attribute(tipoAtributo)
	return valor
