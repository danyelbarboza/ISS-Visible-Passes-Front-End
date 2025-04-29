import requests

class NominatimClient():
    def obter_coordenadas_nominatim(cidade):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': cidade,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'RastreadorISS/1.0 (hazmil178@gmail.com)'
        }

        resposta = requests.get(url, params=params, headers=headers)

        if resposta.status_code == 200 and resposta.json():
            dados = resposta.json()[0]
            
            if dados:
                lat = round(float(dados['lat']), 2)
                lon = round(float(dados['lon']), 2)
                return lat, lon
        else:
            print("Cidade não encontrada.")
            return None
        

    def obter_localizacao_por_coordenadas(lat, lon):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'zoom': 10,
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'RastreadorISS/1.0 (hazmil178@gmail.com)'
        }

        resposta = requests.get(url, params=params, headers=headers)

        if resposta.status_code == 200:
            dados = resposta.json()
            endereco = dados.get("address", {})

        cidade = (
            endereco.get("city") or
            endereco.get("town") or
            endereco.get("village") or
            endereco.get("municipality") or
            endereco.get("county")
        )
        estado = endereco.get("state")

        if cidade and estado:
            return f"{cidade}, {estado}"
        elif estado:
            return estado
        else:
            return "Localização desconhecida"