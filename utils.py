from datetime import datetime

def pegarDataeHorario(valorData='total'):
	"""Tenta resgatar a data atual"""
	parametroRequisitado  = valorData.upper()
	agora = datetime.now()
	opcoes = {
       	'TOTAL': agora.strftime("%d/%m/%Y, %H:%M:%S"),
       	'DIA': agora.strftime("%d"),
       	'MÊS': agora.strftime("%m"),
       	'ANO':agora.strftime("%Y"),
       	'MINUTO':agora.strftime("%M"),
       	'MINUTOS':agora.strftime("%M"),
       	'SEGUNDO':agora.strftime("%S"),
       	'SEGUNDOS':agora.strftime("%S")
       	}
	return opcoes.get(parametroRequisitado)


	
