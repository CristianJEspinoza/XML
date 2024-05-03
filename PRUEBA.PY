import xml.etree.ElementTree as ET
import numpy as np
 
 
def leer_factura(ruta):
    # Names spaces
    ns = {
        'sac':'urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1',
        'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
        'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
    }
 
    tree = ET.parse(ruta)
    root = tree.getroot()
   
    # Header
    doc_num = root.find('cbc:ID',ns).text
    dat_iss = root.find('cbc:IssueDate',ns).text
 
    # Cuenta de proveedor
    sup_acc = root.find('cac:AccountingSupplierParty',ns).find('cac:Party',ns).find('cac:PartyIdentification',ns).find('cbc:ID',ns).text
    pro_nam = root.find('cac:AccountingSupplierParty', ns).find('cac:Party', ns).find('cac:PartyLegalEntity',ns).find('cbc:RegistrationName',ns).text
    doc_typ = root.find('cac:AccountingSupplierParty',ns).find('cac:Party',ns).find('cac:PartyIdentification',ns).find('cbc:ID',ns).attrib['schemeID']
    # pay_met = root.find('cac:PaymentTerms',ns).find('cbc:PaymentMeansID',ns).text
 
    # Foot-er
    currency = root.find('cbc:DocumentCurrencyCode',ns).text
    tax_amo = root.find('cac:TaxTotal',ns).find('cbc:TaxAmount',ns).text
    tax_sub = root.find('cac:TaxTotal',ns).find('cac:TaxSubtotal',ns).find('cbc:TaxableAmount',ns).text
    pay_amo = root.find('cac:LegalMonetaryTotal',ns).find('cbc:PayableAmount',ns).text
   
 
    # # Details
    document = []
    for items in root.findall('cac:InvoiceLine',ns):
        # item = {'doc_num':doc_num, 'dat_iss':dat_iss, 'sup_acc':sup_acc, 'pro_nam':pro_nam, 'doc_typ':doc_typ, 'pay_met':pay_met, 'currency':currency, 'tax_amo':tax_amo, 'tax_sub':tax_sub, 'pay_amo':pay_amo}
        item = {'doc_num':doc_num, 'dat_iss':dat_iss, 'sup_acc':sup_acc, 'pro_nam':pro_nam, 'doc_typ':doc_typ, 'currency':currency, 'tax_amo':tax_amo, 'tax_sub':tax_sub, 'pay_amo':pay_amo}
        item['id'] = items.find('cbc:ID',ns).text
       
        cod_val = items.find('cac:Item',ns).find('cac:SellersItemIdentification',ns)
        if cod_val != None:
            item['codigo'] = items.find('cac:Item',ns).find('cac:SellersItemIdentification',ns).find('cbc:ID',ns).text
        else:
            item['codigo'] = ''
       
        item['pro_dec'] = items.find('cac:Item',ns).find('cbc:Description',ns).text
        item['cantidad'] = int(float(items.find('cbc:InvoicedQuantity',ns).text))
       
        emp_des_val = len(items.find('cac:Item',ns).findall('cbc:Description',ns))
        if emp_des_val > 2:
            item['emp_des'] = items.find('cac:Item',ns).findall('cbc:Description',ns)[2].text
        else:
            item['emp_des'] = ''
 
        item['emp_cod'] = items.find('cbc:InvoicedQuantity',ns).attrib['unitCode']
        item['pre_uni'] = items.find('cac:PricingReference',ns).find('cac:AlternativeConditionPrice',ns).find('cbc:PriceAmount',ns).text
        item['val_uni'] = items.find('cac:Price',ns).find('cbc:PriceAmount',ns).text
       
        des_val = items.find('cac:AllowanceCharge',ns)
        if des_val != None:
            item['descuento'] = items.find('cac:AllowanceCharge',ns).find('cbc:Amount',ns).text
        else:
            item['descuento'] = '0.00'
 
        item['tax'] = items.find('cac:TaxTotal',ns).find('cac:TaxSubtotal',ns).find('cac:TaxCategory',ns).find('cbc:Percent',ns).text
        item['pre_tax'] = items.find('cac:TaxTotal',ns).find('cbc:TaxAmount',ns).text
        item['pre_tot'] = items.find('cbc:LineExtensionAmount',ns).text
 
 
        # Porcentaje de diferencia
        if float(item['pre_tot']) > 0:
            item['tot'] = float(item['pre_uni']) * float(item['cantidad'])
            item['por_tot'] =  round(((float(item['tot']) - float(item['pre_tot'])) / float(item['pre_tot'])) * 100, 2)
        else:
            item['tot'] = 0.00
            item['por_tot'] = 0.00
 
        item['total'] = 0.00
        if item['por_tot'] > 15:
            item['total'] = float(item['pre_tot']) + float(item['pre_tax'])
        elif item['por_tot'] <= 0:
            item['total'] = float(item['pre_tot'])
 
        document.append(item)
       
    return document
 
data = leer_factura(r'C:\Users\cristianec\Documents\Python\Proyectos\XML\KIMBERLY CLARK PERYU\20100152941_01_F084-822177_21944399.xml')
print(data)