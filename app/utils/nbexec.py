import io, nbformat, tempfile, os
import papermill as pm
from nbconvert import HTMLExporter
def execute_notebook_html_csv(nb_path: str, params: dict):
    out_nb_path = tempfile.mktemp(suffix=".ipynb")
    pm.execute_notebook(nb_path, out_nb_path, parameters=params, log_output=True)
    nb = nbformat.read(out_nb_path, as_version=4)
    html_exporter = HTMLExporter()
    (body, resources) = html_exporter.from_notebook_node(nb)
    html_bytes = body.encode("utf-8")
    csv_map = {}
    for cell in nb.cells:
        if cell.cell_type != "code" or not cell.get("outputs"):
            continue
        for out in cell.outputs:
            data = getattr(out, "data", {}) if hasattr(out, "data") else out.get("data", {})
            if isinstance(data, dict) and "text/csv" in data:
                name = (getattr(out, "metadata", None) or {}).get("name", "export")
                base = name; i = 1
                while name in csv_map:
                    name = f"{base}_{i}"; i += 1
                csv_map[name] = data["text/csv"].encode("utf-8")
    return html_bytes, csv_map
