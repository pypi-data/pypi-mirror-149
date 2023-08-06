def map_aza_stock_to_url(stock_tic, site='om-aktien.html'):
    """Return URL to Avanza. Map stock ticker to URL on Avanza.

    site = 'om-aktien.html' or 'om-bolaget.html'

    :param stock_tic:
    :param site:
    :returns stock: Dict with ticker and url
    """
    stock = {}
    aza_url = "https://www.avanza.se/aktier/" + site

    stock['ABB.ST'] = aza_url + "/5447/abb-ltd"
    stock['ATCO-B.ST'] = aza_url + "/5235/atlas-copco-b"
    stock['AXFO.ST'] = aza_url + "/5465/axfood"
    stock['ALIV-SDB.ST'] = aza_url + "/5236/autoliv-sdb"
    stock['ALIG.ST'] = aza_url + "/572678/alimak-group"
    stock['BOL.ST'] = aza_url + "/5564/boliden"
    stock['CAST.ST'] = aza_url + "/5353/castellum"
    stock['DIOS.ST'] = aza_url + "/43267/dios-fastigheter"
    stock['DNB.OL'] = aza_url + "/52628/dnb"
    stock['DUST.ST'] = aza_url + "/538819/dustin-group"
    stock['ESSITY-B.ST'] = aza_url + "/764241/essity-b"
    stock['EQT.ST'] = aza_url + "/1001617/eqt"
    stock['FABG.ST'] = aza_url + "/5300/fabege"
    stock['HUFV-A.ST'] = aza_url + "/5287/hufvudstaden-a"
    stock['HM-B.ST'] = aza_url + "/5364/hennes---mauritz-b"
    stock['HOLM-B.ST'] = aza_url + "/5251/holmen-b"
    stock['HEMF.ST'] = aza_url + "/470196/hemfosa-fastigheter"
    stock['ICA.ST'] = aza_url + "/31607/ica-gruppen"
    stock['INVE-B.ST'] = aza_url + "/5247/investor-b"
    stock['INDU-C.ST'] = aza_url + "/5245/industrivarden-c"
    stock['JM.ST'] = aza_url + "/5501/jm"
    stock['KINV-B.ST'] = aza_url + "/5369/kinnevik-b"
    stock['KLED.ST'] = aza_url + "/5434/kungsleden"
    stock['LUND.ST'] = aza_url + "/5375/lundbergforetagen-b"
    stock['LATO-B.ST'] = aza_url + "/5321/latour-b"
    stock['NP3.ST'] = aza_url + "/522855/np3-fastigheter"
    stock['PEXIP.OL'] = aza_url + "/1093877/pexip-holding"
    stock['PLEJD'] = aza_url + "/649096/plejd"
    stock['SAMPO.HE'] = aza_url + "/52810/sampo-oyj-a"
    stock['SBB-B.ST'] = aza_url + "/517316/samhallsbyggnadsbo--i-norden-b"
    stock['SCA-B.ST'] = aza_url + "/5263/sca-b"
    stock['SEB-C.ST'] = aza_url + "/5256/seb-c"
    stock['SHB-B.ST'] = aza_url + "/5265/handelsbanken-b"
    stock['SKA-B.ST'] = aza_url + "/5257/skanska-b"
    stock['SWED-A.ST'] = aza_url + "/5241/swedbank-a"
    stock['TIETO.HE'] = aza_url + "/5455/tietoevry"
    stock['UPM.HE'] = aza_url + "/52842/upm-kymmene-oyj"
    stock['WALL-B.ST'] = aza_url + "/5344/wallenstam-b"
    stock['VOLV-B.ST'] = aza_url + "/5269/volvo-b"

    return stock[stock_tic]
