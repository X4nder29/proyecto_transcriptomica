import os
import base64
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def extract_fastqc_data(html_path: str, output_dir: str):
    """
    Extrae las gráficas (segunda imagen) de cada módulo y las tablas “Basic statistics”
    y “Overrepresented sequences” de un informe FastQC en HTML. Guarda:
      - Cada módulo (solo la segunda imagen) como PNG en output_dir.
      - Las tablas en formato JSON en output_dir.

    Parámetros:
        html_path: Ruta al archivo HTML de FastQC.
        output_dir: Carpeta donde se guardarán los resultados.

    Retorna:
        Un dict con:
          - "images": lista de tuplas (módulo, ruta_png)
          - "basic_statistics_json": ruta al JSON de Basic Statistics (o None)
          - "overrepresented_sequences_json": ruta al JSON de Overrepresented sequences (o None)
    """
    # Crear carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Cargar y parsear el HTML con BeautifulSoup
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Nombres exactos de los módulos de los que queremos la segunda imagen
    modules = [
        "Per base sequence quality",
        "Per sequence quality scores",
        "Per base sequence content",
        "Per sequence GC content",
        "Per base N content",
        "Sequence Length Distribution",
        "Sequence Duplication Levels",
        "Adapter Content",
    ]

    extracted_images = []
    module_divs = soup.find_all("div", class_="module")

    for module_name in modules:
        for md in module_divs:
            # Buscar el tag <h2> o <h3> cuyo texto coincide exactamente con el nombre del módulo
            title_tag = md.find(["h2", "h3"])
            if title_tag and title_tag.text.strip() == module_name:
                img_tags = md.find_all("img")
                # Si hay al menos dos <img>, tomamos la segunda
                if len(img_tags) >= 2:
                    second_img = img_tags[1]
                    src = second_img.get("src", "")
                    if "base64," in src:
                        img_data = src.split("base64,")[1]
                        img_bytes = base64.b64decode(img_data)
                        # Formar nombre de archivo a partir del nombre del módulo
                        safe_name = (
                            module_name.lower().replace(" ", "_").replace("/", "_")
                        )
                        filename = f"{safe_name}.png"
                        file_path = os.path.join(output_dir, filename)
                        with open(file_path, "wb") as img_file:
                            img_file.write(img_bytes)
                        extracted_images.append((module_name, file_path))
                break  # Ya encontramos el módulo, salimos del bucle interno

    # --------------------------------------------------------------
    # Extraer tabla "Basic statistics" y guardarla como JSON
    # --------------------------------------------------------------
    basic_stats_json = None
    basic_stats_header = soup.find(
        lambda tag: tag.name in ["h2", "h3"] and tag.text.strip() == "Basic Statistics"
    )
    if basic_stats_header:
        basic_stats_table = basic_stats_header.find_next("table")
        if basic_stats_table:
            # Para evitar el FutureWarning, envolvemos el HTML en StringIO
            table_html = str(basic_stats_table)
            basic_df = pd.read_html(StringIO(table_html))[0]
            basic_stats_json = os.path.join(output_dir, "basic_statistics.json")
            basic_df.to_json(basic_stats_json, orient="records", indent=4)

    # --------------------------------------------------------------
    # Extraer tabla "Overrepresented sequences" y guardarla como JSON
    # --------------------------------------------------------------
    overrep_json = None
    overrep_header = soup.find(
        lambda tag: tag.name in ["h2", "h3"]
        and tag.text.strip() == "Overrepresented sequences"
    )
    if overrep_header:
        overrep_table = overrep_header.find_next("table")
        if overrep_table:
            table_html = str(overrep_table)
            overrep_df = pd.read_html(StringIO(table_html))[0]
            overrep_json = os.path.join(output_dir, "overrepresented_sequences.json")
            overrep_df.to_json(overrep_json, orient="records", indent=4)

    return {
        "images": extracted_images,
        "basic_statistics_json": basic_stats_json,
        "overrepresented_sequences_json": overrep_json,
    }
