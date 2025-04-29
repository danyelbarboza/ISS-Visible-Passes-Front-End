from n2yo_client import N2yoClient
from openmeteo_client import OpenMeteoClient
from config import Config
from nominatim_client import NominatimClient

class RunTheProgram:
    
    def coordenadas_nominatim(cidade_usuario):
        # Obtém as coordenadas da cidade informada utilizando a API Nominatim
        coordenadas = NominatimClient.obter_coordenadas_nominatim(cidade_usuario)
        latitude = coordenadas[0]
        longitude = coordenadas[1]
        return latitude, longitude
    
    def nome_da_cidade_nominatim(latitude, longitude):
        return NominatimClient.obter_localizacao_por_coordenadas(latitude, longitude)
    
    def obter_informacoes(cidade_usuario):
        # Obter coordenadas
        latitude, longitude = RunTheProgram.coordenadas_nominatim(cidade_usuario)
        if latitude is None or longitude is None:
            return None, "Cidade não encontrada"
        
        # Obter nome real da cidade
        nome_real_cidade = RunTheProgram.nome_da_cidade_nominatim(latitude, longitude)
        
        # Cria um objeto de configuração com as coordenadas da cidade
        config = Config(latitude, longitude)
        
        # Cria um cliente N2yo e obtém as passagens da ISS para as coordenadas fornecidas
        n2yo = N2yoClient(config)
        all_passes = n2yo.display_passes()
        
        # Obtém os dados meteorológicos para cada passagem
        weather_data_id = []
        id = 1
        for item in all_passes:
            start_time = item['start']
            openmeteo = OpenMeteoClient()
            weather_data = openmeteo.get_weather_data(latitude, longitude, start_time)
            weather_data_id.append({
                "id": id,
                "weather": weather_data
            })
            id += 1
            
        resultados = []
        avaliacoes = []
        # Extrai os dados de cada lista e adiciona a um dicionário
        for pass_data, weather_data in zip(all_passes, weather_data_id):
            resultado = {
                "id": pass_data['id'],
                "start": pass_data['start'],
                "duration": pass_data['duration'],
                "temperature": weather_data['weather']['temperature_2m'],
                "cloudcover": weather_data['weather']['cloudcover'],
                "visibility": weather_data['weather']['visibility'],
                "humidity": weather_data['weather']['relative_humidity_2m'],
                "is_day": "Day" if weather_data['weather']['is_day'] == 1 else "Night"
            }
            resultados.append(resultado)
            avaliacoes.append(RunTheProgram.avaliar_visibilidade_iss(resultado))
            
        return resultados, nome_real_cidade, avaliacoes
    
    def avaliar_visibilidade_iss(ponto):
        # Cobertura de nuvens (quanto menor, melhor)
        nota_nuvem = max(0, 1 - ponto['cloudcover'] / 100)

        # Umidade ideal entre 40-70%
        if ponto['humidity'] <= 70:
            nota_umidade = 1
        elif ponto['humidity'] < 90:
            nota_umidade = max(0, 1 - (ponto['humidity'] - 70) / 20)
        else:
            nota_umidade = 0

        # Duração da passagem (ótimo >= 600s)
        nota_duracao = min(1, ponto['duration'] / 600)

        # Temperatura confortável (20–26 ºC)
        temp = ponto['temperature']
        if 20 <= temp <= 26:
            nota_temp = 1
        elif 16 <= temp < 20 or 26 < temp <= 30:
            nota_temp = 0.7
        else:
            nota_temp = 0.4

        # Visibilidade ideal > 20000 m
        vis = ponto['visibility']
        nota_visibilidade = min(1, vis / 20000)  # acima disso fica 1.0

        # Nota final com novos pesos
        nota_final = (
            0.4 * nota_nuvem +
            0.15 * nota_umidade +
            0.2 * nota_duracao +
            0.1 * nota_temp +
            0.15 * nota_visibilidade
        )

        return round(nota_final * 10, 1)

