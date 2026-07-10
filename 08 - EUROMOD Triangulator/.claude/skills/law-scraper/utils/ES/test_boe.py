import httpx
from bs4 import BeautifulSoup

def search_boe(law_type, number):
    url = "https://www.boe.es/buscar/legislacion.php"
    query = f"{law_type} {number}"
    params = {
        "accion": "Buscar",
        "campo[2]": "DOC",
        "dato[2]": query,
        "checkbox_solo_tit": "S",
        "operador[2]": "and",
        "sort_field[0]": "PESO",
        "sort_order[0]": "desc"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    with httpx.Client(headers=headers, verify=False) as client:
        r = client.get(url, params=params, follow_redirects=True)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find_all("li", class_="resultado-busqueda")
        print(f"[{query}] Found {len(results)} results")
        if results:
            print(results[0].prettify())

search_boe("Ley", "31/2022")
