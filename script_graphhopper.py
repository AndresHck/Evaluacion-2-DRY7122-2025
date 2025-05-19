import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "b73dedb9-ff8d-4237-91a1-c15ac5d88f86"

DEFAULT_FROM = "Santiago, Chile"
DEFAULT_TO = "Ovalle, Chile"

def geocoding(location, key):
    while not location or location in ["q", "quit", "salir"]:
        if location in ["q", "quit", "salir"]:
            return None, None, None, None
        location = input("Introduce la ubicación de nuevo (o ‘q’ para salir): ")
    url = "https://graphhopper.com/api/1/geocode?" + urllib.parse.urlencode({
        "q": location,
        "limit": "1",
        "key": key,
        "locale": "es"
    })
    r = requests.get(url)
    data = r.json()
    if r.status_code == 200 and data["hits"]:
        hit = data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit["osm_value"]
        country = hit.get("country", "")
        state = hit.get("state", "")
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {state}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        print(f"URL de Geocodificación para {new_loc} (Tipo: {value})")
        print(url)
        return r.status_code, lat, lng, new_loc
    else:
        print(f"Error Geocodificación ({r.status_code}): {data.get('message','sin mensaje')}")
        return r.status_code, None, None, location

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (coche), bike (bicicleta), foot (a pie)  —  ‘q’ para salir")
    profile = ["car", "bike", "foot"]
    vehicle = input("Perfil de vehículo: ")
    if vehicle in ["q", "quit", "salir"]:
        break
    if vehicle not in profile:
        print("Perfil no válido, se usará ‘car’.")
        vehicle = "car"
    vehicle_spanish = {"car": "coche", "bike": "bicicleta", "foot": "a pie"}

    loc1 = input(f"Ciudad de Origen [{DEFAULT_FROM}] (o ‘q’ para salir): ") or DEFAULT_FROM
    if loc1 in ["q", "quit", "salir"]:
        break
    orig = geocoding(loc1, key)
    if orig[0] != 200:
        continue

    loc2 = input(f"Ciudad de Destino [{DEFAULT_TO}] (o ‘q’ para salir): ") or DEFAULT_TO
    if loc2 in ["q", "quit", "salir"]:
        break
    dest = geocoding(loc2, key)
    if dest[0] != 200:
        continue

    print("=================================================")
    op = f"&point={orig[1]}%2C{orig[2]}"
    dp = f"&point={dest[1]}%2C{dest[2]}"
    paths_url = route_url + urllib.parse.urlencode({
        "key": key,
        "vehicle": vehicle,
        "locale": "es"
    }) + op + dp

    r = requests.get(paths_url)
    pd = r.json()
    print(f"Estado Rutas: {r.status_code}")
    print(paths_url)
    print("=================================================")
    if r.status_code == 200:
        total_s = pd["paths"][0]["time"] / 1000
        hr = int(total_s // 3600)
        mn = int((total_s % 3600) // 60)
        sc = total_s % 60
        km = pd["paths"][0]["distance"] / 1000
        print(f"Distancia: {km:.2f} km")
        print(f"Duración: {hr:02d}:{mn:02d}:{sc:05.2f}")
        print("=================================================")
        print(f"Indicaciones ({vehicle_spanish[vehicle]}):")
        for inst in pd["paths"][0]["instructions"]:
            text = inst["text"]
            d = inst["distance"] / 1000
            mi = d / 1.61
            print(f"{text} ({d:.2f} km / {mi:.2f} millas)")
        print("=================================================")
    else:
        print("Error:", pd.get("message", "sin detalle"))

