from weasyprint import CSS, HTML
from weasyprint.fonts import FontConfiguration
from django.core.files import File
from django.template.loader import render_to_string
import os
#Django==3.0.7
#WeasyPrint==52.5
def htmlToPdf(media_root_url,file_name,template_src,context_dict={}):
    ''' 
        This function return file with parameter media root url ,file name, template src with differents variables in context_dict
    
    '''
    html_content = render_to_string(template_src, context_dict) # render with dynamic value        
    font_config = FontConfiguration()
    html = HTML(string=html_content)
    css = CSS(string='@page { size: A3; margin: 1cm }',font_config=font_config)
    path_file = os.path.join(media_root_url,str(file_name)+".pdf")
    html.write_pdf(path_file, stylesheets=[css])
    f = open(path_file, "rb")
    new_file = File(f)
    return new_file

def htmlToPdfWithCss(media_root_url,file_name,template_src,context_dict={},stylesheet='@page { size: A3; margin: 850px }'):
    ''' 
        This function return file with parameter media root url ,file name, stylesheet css ,and template src with differents variables in context_dict
    
    '''
    html_content = render_to_string(template_src, context_dict) # render with dynamic value        
    font_config = FontConfiguration()
    html = HTML(string=html_content)
    css = CSS(string=stylesheet,font_config=font_config)
    path_file = os.path.join(media_root_url,str(file_name)+".pdf")
    html.write_pdf(path_file, stylesheets=[css])
    f = open(path_file, "rb")
    new_file = File(f)
    return new_file