import fitz  # PyMuPDF
import os

# El nombre del archivo PDF que deseas convertir
pdf_path = "archivos_21974-10042025124615-CERTREG.pdf"

# Abre el documento PDF
pdf_document = fitz.open(pdf_path)

# Crear carpeta para las imágenes extraídas
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

# Abre un archivo HTML para escribir el contenido
html_content = "<html><head><title>PDF a HTML</title></head><body>"

# Itera sobre todas las páginas
for page_num in range(pdf_document.page_count):
    page = pdf_document.load_page(page_num)

    # Extraer texto como HTML
    page_html = page.get_text("html")

    # Agregar el contenido HTML de la página al archivo
    html_content += f"<div class='page' id='page_{page_num}'>"
    html_content += page_html
    html_content += "</div>"

    # Extraer imágenes de la página
    img_list = page.get_images(full=True)
    for img_index, img in enumerate(img_list):
        xref = img[0]  # El identificador de la imagen
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        # Guardar la imagen en la carpeta output_images
        image_filename = f"{output_dir}/page_{page_num}_img_{img_index}.png"
        with open(image_filename, "wb") as img_file:
            img_file.write(image_bytes)

        # Reemplazar la referencia de la imagen en el HTML con la ruta de la imagen guardada
        html_content = html_content.replace(f"img{xref}.png", f"{output_dir}/page_{page_num}_img_{img_index}.png")

# Cerrar el archivo HTML
html_content += "</body></html>"

# Guardar el HTML en un archivo
output_html = "output.html"
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"PDF convertido a HTML con imágenes. El archivo HTML se guardó como {output_html}.")
