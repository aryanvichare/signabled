import pdfreader
from pdfreader import  SimplePDFViewer


file_name = "test1.pdf"

fd = open(file_name, "rb")
viewer = SimplePDFViewer(fd)

st = ""
pt = ""

for canvas in viewer:
     page_images = canvas.images
     page_forms = canvas.forms
     page_text = canvas.text_content
     page_inline_images = canvas.inline_images
     page_strings = canvas.strings

     pt = pt + page_text
     for s in canvas.strings:
         st = st + s
    #  st = st + canvas.strings



print ("************")
# print (pt)
print("--------------")
print(st)

