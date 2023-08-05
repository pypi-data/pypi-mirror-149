from printPersian import arabic_reshaper 
from printPersian  import get_display 

#__________________________________________________

def convertPersian(str):
    reshaped_text = arabic_reshaper.reshape(str)
    persianText = get_display(reshaped_text)
    return persianText

