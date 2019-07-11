# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 20:50:34 2019

@author: EGrandgi


=================================URLS BILANS===================================

"""


# =============================================================================
#                                  Packages
# =============================================================================

from bs4 import BeautifulSoup
import requests



# =============================================================================
#                                 Fonctions
# =============================================================================


start_url = "https://bases.athle.fr/asp.net/liste.aspx?"

def generate_url(frmannee, frmsexe, frmepreuve,
                 frmcategorie, frmbase="bilans", frmposition=0,
                 frmnationalite="", frmamini="", frmamaxi="", 
                 frmvent="", frmathlerama="", frmfcompetition="", 
                 frmfepreuve0="", frmpostback=True, frmmode=1, 
                 frmplaces="", frmespace=0):
    url = start_url+"frmpostback="+str(frmpostback)+"&frmbase="+frmbase+"&frmmode="+str(frmmode)+"&frmespace="+str(frmespace)+"&frmannee="+str(frmannee)+"&frmathlerama="+frmathlerama+"&frmfcompetition="+frmfcompetition+"&frmfepreuve="+frmfepreuve0+"&frmepreuve="+str(frmepreuve)+"&frmplaces="+frmplaces+"&frmnationalite="+frmnationalite+"&frmamini="+frmamini+"&frmamaxi="+frmamaxi+"&frmsexe="+frmsexe+"&frmcategorie="+frmcategorie+"&frmvent="+frmvent+"&frmposition="+str(frmposition)
    return(url)
    
    
"""
    frmannee : depuis 2004
    frmsexe : F | M
    frmepreuve : chercher la liste des ids épreuves
    frmcategorie : "" | ES | JU | CA | MI
    frmbase : "bilans" | "podiums" | "resultats" | "qualifies" | autres catégories dans "navigation"
    frmposition : numéro de page, à partir de 0

"""


def create_soup(url):
    
    """ 
        In : url d'une page web
        Out : code source de la page  
        
    """
    
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    return(soup)
    


# =============================================================================
#                            Application à un exemple
# =============================================================================
    
    
# bilan 800m F 2019
test_url = generate_url(frmannee=2019, frmsexe="F", frmepreuve=208,
                         frmcategorie="", frmbase="bilans", frmposition=0,
                         frmnationalite="", frmamini="", frmamaxi="", 
                         frmvent="", frmathlerama="", frmfcompetition="", 
                         frmfepreuve0="", frmpostback=True, frmmode=1, 
                         frmplaces="", frmespace=0)

soup = create_soup(test_url)

    
  
