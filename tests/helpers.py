import requests

ns_19115_3 =  { 'mdb':"http://standards.iso.org/iso/19115/-3/mdb/2.0",
                'cat': "http://standards.iso.org/iso/19115/-3/cat/1.0",
                'gfc': "http://standards.iso.org/iso/19110/gfc/1.1",
                'cit': "http://standards.iso.org/iso/19115/-3/cit/2.0",
                'gcx': "http://standards.iso.org/iso/19115/-3/gcx/1.0",
                'gex': "http://standards.iso.org/iso/19115/-3/gex/1.0",
                'lan': "http://standards.iso.org/iso/19115/-3/lan/1.0",
                'srv': "http://standards.iso.org/iso/19115/-3/srv/2.1",
                'mas': "http://standards.iso.org/iso/19115/-3/mas/1.0",
                'mcc': "http://standards.iso.org/iso/19115/-3/mcc/1.0",
                'mco': "http://standards.iso.org/iso/19115/-3/mco/1.0",
                'mda': "http://standards.iso.org/iso/19115/-3/mda/1.0",
                'mds': "http://standards.iso.org/iso/19115/-3/mds/2.0",
                'mdt': "http://standards.iso.org/iso/19115/-3/mdt/2.0",
                'mex': "http://standards.iso.org/iso/19115/-3/mex/1.0",
                'mmi': "http://standards.iso.org/iso/19115/-3/mmi/1.0",
                'mpc': "http://standards.iso.org/iso/19115/-3/mpc/1.0",
                'mrc': "http://standards.iso.org/iso/19115/-3/mrc/2.0",
                'mrd': "http://standards.iso.org/iso/19115/-3/mrd/1.0",
                'mri': "http://standards.iso.org/iso/19115/-3/mri/1.0",
                'mrl': "http://standards.iso.org/iso/19115/-3/mrl/2.0",
                'mrs': "http://standards.iso.org/iso/19115/-3/mrs/1.0",
                'msr': "http://standards.iso.org/iso/19115/-3/msr/2.0",
                'mdq': "http://standards.iso.org/iso/19157/-2/mdq/1.0",
                'mac': "http://standards.iso.org/iso/19115/-3/mac/2.0",
                'gco': "http://standards.iso.org/iso/19115/-3/gco/1.0",
                'gml': "http://www.opengis.net/gml/3.2",
                'xlink': "http://www.w3.org/1999/xlink",
                'xsi': "http://www.w3.org/2001/XMLSchema-instance"
}

ns_19139 = { 'gmd':"http://www.isotc211.org/2005/gmd",
           'gco':"http://www.isotc211.org/2005/gco",
           'xsi':"http://www.w3.org/2001/XMLSchema-instance",
           'gml':"http://www.opengis.net/gml",
           'gts':"http://www.isotc211.org/2005/gts",
           'xlink':"http://www.w3.org/1999/xlink" }


def make_xpath(ns_dict, path_elems):
    """
    Makes an xpath with namespaces  given a list of tags

    :param ns_dict: namespace dictionary e.g. { 'cit': 'http://cit.org/1.0', 'dif': 'http://dif.org/2.0' }
    :param path_elems: list of tags e.g. ['cit:citation', 'dif:differential']
    :returns: xpath string
    """
    path = './/'
    for ele in path_elems:
        ns, dot, tag = ele.partition(':')
        path += f"{{{ns_dict[ns]}}}{tag}/"
    return path.rstrip('/')

def get_metadata(metadata_url):
    """
    Fethes metadata from a URL

    :param metadata_url: metadata URL
    :returns: metadata, encoding
    """
    meta = requests.get(metadata_url)
    if meta.encoding is not None:
        encoding = meta.encoding
    else:
        encoding = 'utf-8'

    # Read XML from URL
    return encoding, meta



