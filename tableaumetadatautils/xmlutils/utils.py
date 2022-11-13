
import xml.etree.ElementTree as ET

def create_xml_login(personalAccessTokenName : str , personalAccessTokenSecret : str, site : str) -> str:
    if site.lower() == "default":
        site = ""
    root  = ET.Element("tsRequest")
    credentials = ET.SubElement(root,"credentials",{"personalAccessTokenName":personalAccessTokenName,"personalAccessTokenSecret":personalAccessTokenSecret})
    ET.SubElement(credentials, "site", {"contentUrl": site})
    # credentials = ET.Element("credentials",{"personalAccessTokenName":"prueba","personalAccessTokenSecret":""})
    # root.append(credentials)
    return ET.tostring(root, short_empty_elements=True)