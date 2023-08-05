import lxml.etree as ET


def make_pb(n, faks_url, faks_id):
    """ returns a tei:pb
    """
    pb_el = ET.Element("{http://www.tei-c.org/ns/1.0}pb")
    pb_el.attrib['n'] = f"{n}"
    pb_el.attrib['facs'] = f"{faks_url}"
    pb_el.attrib[
        "{http://www.w3.org/XML/1998/namespace}id"
    ] = f"faks__{faks_id}"

    return pb_el
