from datetime import datetime, timedelta

def adicionar_dias_uteis(data, dias):
    # Converter string para datetime se necessário
    if isinstance(data, str):
        data = datetime.strptime(data, '%Y-%m-%d')
    elif not isinstance(data, datetime):
        # Se for uma date, converter para datetime
        data = datetime.combine(data, datetime.min.time())
    
    # Adicionar os dias
    resultado = data + timedelta(days=dias)
    
    # Verificar se é fim de semana (5 = sábado, 6 = domingo)
    while resultado.weekday() >= 5:
        resultado += timedelta(days=1)
    
    return resultado
