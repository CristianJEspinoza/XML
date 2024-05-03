from xml.etree import ElementTree


class invoiceModel:
 
    __xmlLabels = {
        "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        "sac": "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1",
    }
 
    def readHeadXmlGrupo1(self, urlFile: str):
        try:
            __xmlData = ElementTree.parse(urlFile).getroot()
 
            if "Invoice" not in __xmlData.tag:
                __xmlData = __xmlData.find(".//{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice")
 
            if __xmlData:
                __responseXML = {
                    "RUC": __xmlData.find("cac:AccountingSupplierParty", self.__xmlLabels)
                    .find("cac:Party", self.__xmlLabels)
                    .find("cac:PartyIdentification", self.__xmlLabels)
                    .find("cbc:ID", self.__xmlLabels)
                    .text,
                    "FACTURA": __xmlData.find("cbc:ID", self.__xmlLabels).text,
                    "FECHA": __xmlData.find("cbc:IssueDate", self.__xmlLabels).text,
                    "MONEDA": __xmlData.find("cbc:DocumentCurrencyCode", self.__xmlLabels).text,
                    "URLFILE": urlFile,
                }
 
                return __responseXML
 
            else:
                return "errorXML"
       
        except Exception as e:
            # Manejar cualquier excepción y devolver un mensaje de error
            print(f"Error en readHeadXmlGrupo1: {str(e)}")
            return "errorXML"


ap = invoiceModel()
ruta = r"C:\Users\cristianec\Documents\Python\Proyectos\XML\BAJOPONTINA SOCIEDAD ANONIMA\01_F700-0000665922.xml"

print(ap.readHeadXmlGrupo1(ruta))