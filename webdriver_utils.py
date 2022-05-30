""""""
from selenium import webdriver
from selenium.webdriver.support.relative_locator import RelativeBy
from selenium.webdriver.edge.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import os
from time import sleep



def criarWebDriver(tipoDriver='Chrome'):
	"""Cria uma instância de webdriver do selenium"""
	os.environ['WDM_SSL_VERIFY']='0'
	global opcoes
	global driver
	global acoes
	driver = escolherWebDriver(tipoDriver.upper())
	acoes = ActionChains(driver)
	

def escolherWebDriver(driverString):
	"""Função interna que trabalha a partir da chamada da função criarWebDriver"""
	opcoes = {
       	'CHROME': criarChromeDriver,
       	'EDGE': criarEdgeDriver,
       	'FIREFOX':criarFirefoxDriver,
       	}
	return opcoes.get(driverString)()

def criarChromeDriver():
	"""Cria e retorna o webdriver do navegador Chrome"""
	opcoes = webdriver.ChromeOptions()
	opcoes.add_argument("start-maximized")
	opcoes.add_experimental_option('excludeSwitches', ['enable-logging'])
	return webdriver.Chrome(ChromeDriverManager(path=os.getcwd()).install(),options=opcoes)

def criarFirefoxDriver():
	"""Cria e retorna o webdriver do navegador Firefox"""
	return webdriver.Firefox(GeckoDriverManager(path=os.getcwd()).install())

def criarEdgeDriver():
	"""Cria e retorna o webdriver do navegador Edge"""
	opcoes = Options()
	opcoes.add_argument("start-maximized")
	return webdriver.Edge(EdgeChromiumDriverManager(path=os.getcwd()).install(),options=opcoes)

def aguardarPagina():
	"""Define um wait para o carregamento da página, aguardando estar pronta para a próxima ação"""
	yield WebDriverWait(driver, 3).until(EC.staleness_of(driver.find_element(By.TAG_NAME,'html')))
	WebDriverWait(driver, 10).until(lambda driver: driver.execute_script("return document.readyState;") == "complete")

def checaExistenciaElementopeloXPath(elementoXPath):
	"""Verifica a existância de algum elemeno"""
	return True if len(driver.find_elements(By.XPATH,elementoXPath))>0 else False

def centralizarElemento(elemento):
	"""Focaliza (centralizando, rolando a página para) no elemento passado como parâmetro"""
	acoes.move_to_element(elemento).perform()

def navegarPara(URL):
	"""instruí o webdriver criado a navegar para o endereço passado como parâmetro"""
	driver.get(URL)
	aguardarPagina()

def pegaElementopeloXPath(elementoXPath):
	"""Captura um dado elemento (o parâmetro) e o retorna"""
	return driver.find_element(By.XPATH,elementoXPath)

def clicaElementopeloXPath(elementoXPath):
	"""Clica no elemento passado como parâmetro utilizando actions"""
	elemento = pegaElementopeloXPath(elementoXPath)
	acoes.click(elemento).perform()
	aguardarPagina()

def pegaConteudopeloAtributo(elemento,tipoAtributo='textContent'):
	"""Captura o valor do atributo do elemento passado como parâmetro"""
	valor = elemento.get_attribute(tipoAtributo)
	return valor

def moveparaElemento(elemento):
	"""Focaliza e move o cursor do mouse para o elemento passado como parâmetro"""
	acoes.move_to_element(elemento).perform()

def preencheInputpeloXPath(elemXPath,valorInput):
	"""Preenche o campo de input passado como parâmetro, com o valor de 'valorInput', performando a escrita através de actions"""
	elemInput = pegaElementopeloXPath(elementoXPath)
	centralizarElemento(elemInput)
	elemInput.send_keys(valorInput.strip())

def capturaAlerta(confirmacao=True):
	"""Intercepta alertas que aparecem na página, dando ok ou cancel e retornando o texto"""
	alerta=''
	mensagem=''
	try:
		WebDriverWait(driver, 10).until(EC.alert_is_present())
		alerta = driver.switch_to_alert()
		mensagem = srt(alerta.text).strip()
		if confirmacao:
			alerta.accept()
		else:
			alerta.dismiss()
	except:
		print("Nenhum alerta achado")	
	return mensagem
