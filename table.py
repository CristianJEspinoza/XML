import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import pandas

class tableModel:

    ##Group One
    def get_document_xml_lines_groupOne(self, ruta: str):
        ns = {
            'sac': 'urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }

        root = ElementTree.parse(ruta).getroot()
        if "Invoice" not in root.tag:
                root = root.find(".//{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice")

        # Definir listas para almacenar los datos de cada columna
        __xmlData = {
            "COD_PRODUCT": [],
            "PRODUCT_QUANTITY": [],
            "DESCRIPTION": [],
            "UNIT_PRICE": [],
            "SUBTOTAL": [],
            "SUBTOTALIGV": []
        }

        # Iterar sobre cada elemento <InvoiceLine> en el XML
        for items in root.findall('cac:InvoiceLine', ns):
            # Codigo del producto
            cod_val = items.find('cac:Item', ns).find('cac:SellersItemIdentification', ns)
            codigo = cod_val.find('cbc:ID', ns).text if cod_val is not None else None

            # Cantidad del producto
            productquantity = float(items.find('cbc:InvoicedQuantity', ns).text)

            # Descripción del producto
            descripcion = items.find('cac:Item', ns).find('cbc:Description', ns).text

            # Subtotal del producto
            subtotal = float(items.find('cbc:LineExtensionAmount', ns).text)

            # Sub total con IGV
            try:
                subtotalIGV = float(items.find('cac:Item', ns).findall('cbc:Description', ns)[2].text)
            except Exception as e:
                subtotalIGV = subtotal * 0.18
            
            

            # Agregar los datos a las listas
            __xmlData["COD_PRODUCT"].append(codigo)
            __xmlData["PRODUCT_QUANTITY"].append(productquantity)
            __xmlData["DESCRIPTION"].append(descripcion)
            __xmlData["UNIT_PRICE"].append(round(subtotal / productquantity, 4))
            __xmlData["SUBTOTAL"].append(round(subtotal, 4))
            __xmlData["SUBTOTALIGV"].append(round(subtotalIGV, 4))

        # Crear un DataFrame con los datos
        df = pandas.DataFrame(__xmlData)
        
        #Eliminando los productos repetidos por bonificación
        df_sin_suplicados = df.drop_duplicates(subset=["COD_PRODUCT"])
        
        # Calcular totales
        total_sin_igv = df_sin_suplicados['SUBTOTAL'].sum()
        igv = total_sin_igv * 0.18
        monto_total = total_sin_igv + igv

        # Crear un DataFrame con los totales
        __xmlDataFinally = {
            "TOTAL_SIN_IGV": [round(total_sin_igv, 4)],
            "IGV_DEL_TOTAL": [round(igv, 4)],
            "TOTAL": [round(monto_total, 4)]
        }
        df2 = pandas.DataFrame(__xmlDataFinally)

        return df, df2
ap = tableModel()
ruta = r"C:\Users\cristianec\Documents\Python\Proyectos\XML\KIMBERLY CLARK PERYU\20100152941_01_F084-1259411_55709536.xml"

resultado_df, resultado_final = ap.get_document_xml_lines_groupOne(ruta)
print(resultado_df)
print(resultado_final)