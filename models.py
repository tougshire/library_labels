from django.db import models

class InsertTemplate(models.Model):
    template_title = models.CharField("template title", blank=True, max_length=50, help_text="The title of this template")
    template_filename = models.CharField("template file name", blank=True, max_length=50, help_text="The name of the template file")
    stylesheet_filename = models.CharField("stylesheet file name", blank=True, max_length=50, help_text="The name of the stylesheet file")

    def __str__(self):
        return self.template_title
    
    
