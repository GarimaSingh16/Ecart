from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# It in taking all the category and converting it into a dictionary format.

# So basically it is a function used to return context dictionaries or create context dictionaries using models and because of this we don't have to mention manually each item like context = {'shirts':shirts...}

# It is a preprocessor so we need to mention it inside the context_processor in Options in Templates in settings.py

# settings.py -> TEMPLATES -> OPTIONS -> context_processors

# and mention function name we have just created like -> 'category.context_processors.menu_links'

# The reason of doing this is that 'menu_links' function will be available to use in any templates/app we wantincluding the main project.