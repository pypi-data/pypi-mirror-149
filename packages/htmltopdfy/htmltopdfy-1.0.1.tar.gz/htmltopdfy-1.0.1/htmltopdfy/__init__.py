def __init__(self,media_root_url,file_name,template_src,context_dict):
  
    self.file_name = file_name #It's file name 
    self.media_root_url = media_root_url #Tt's your settings.media_root
    self.template_src = template_src #It's your template name
    self.context_dict = context_dict # Optionnel[It's variable or variables who is linked with template]

