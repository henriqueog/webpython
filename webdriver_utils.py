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

def createWebDriver(driverType):
	"""Evita de que, quando esteja analisando e fazendo o download do webdriver, se alguma verificação de segurança será considerada"""
	os.environ['WDM_SSL_VERIFY']='0'
	global options
	global driver
	driver = chooseWebDriver(driverType.upper())
	

def chooseWebDriver(driverString):
    opcoes = {
       	'CHROME': createChromeDriver,
       	'EDGE': createEdgeDriver,
       	'FIREFOX':createFirefoxDriver,
    }
    return opcoes.get(driverString)()

def createChromeDriver():
	options = webdriver.ChromeOptions()
	options.add_argument("start-maximized")
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	return webdriver.Chrome(ChromeDriverManager(path=os.getcwd()).install(),options=options)

def createFirefoxDriver():
	return webdriver.Firefox(GeckoDriverManager(path=os.getcwd()).install())

def createEdgeDriver():
	options = Options()
	options.add_argument("start-maximized")
	return webdriver.Edge(EdgeChromiumDriverManager(path=os.getcwd()).install(),options=options)


def waitPageLoad():
    done_state = False
    while done_state == False:
        state = driver.execute_script('return window.document.readyState')
        if state != 'complete':
            sleep(1)
        else:
            done_state = True

def centralizeElement(element):
	actions = ActionChains(driver)
	actions.move_to_element(element).perform()

def navigateTo(URL):
	driver.get(URL)
	waitPageLoad()

def getElementByXPath(elementXPath):
	return driver.find_element_by_xpath(elementXPath)

def clickElementByXPath(elementXPath):
	element = getElementByXPath(elementXPath)
	actions = ActionChains(driver)
	actions.click(element).perform()
	waitPageLoad()

def getContentByAttribute(element,attributeType):
	value=''
	# consideraremos quando o parâmetro for vazio, para capturar o textContent como default
	if len(attributeType.strip())==0:
		value = element.get_attribute('textContent')
	else:
		value = element.get_attribute(attributeType)
	return value
