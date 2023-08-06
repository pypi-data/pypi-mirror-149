
HTML TO PDF
===
Convert template html to pdf

Detailed documentation is in the "docs" directory.

## Quick start

1. Install the module:

         pip install htmltopdfy

2. EXAMPLE

   ### Import module

         from htmltopdfy.job import htmlToPdf

   Let suppose we have a model like this:



         class User():
            name = models.CharField(max_length=200)
            age = models.CharField(max_length=20)
            cni = models.FileField(null=True,blank=True)
   ### Let's create user
         user = User(name="dddd",age="23")
         user.save()
   ### We supposed we have a template named cni.html already designed on which we want to display name and age

         cni_file = htmlToPdf (
            media_root_url=settings.MEDIA_ROOT,
            file_name="cni",
            template_src = "cni.html",
            context_dict = {"name":"dddd","age":"20ans"}
         )
         user.cni.save("cni.pdf",cni_file)
   
   ### After you can print variable _cni_ in console to see result or send url file on  your response view:
         print(user.cni)
   or 

         return Response({"cni":user.cni.url})
