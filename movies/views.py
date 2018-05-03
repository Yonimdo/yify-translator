from django.shortcuts import render

# Create your views here.
from movies.forms import SearchForm
from movies.tools import subs
from movies.tools.subs import OrderBy


def import_subtitles(request):
    search = ""
    order = ""
    if request.method == 'POST':
        # form = SearchForm()(request.POST)
        search = request.POST.get('search')
        order = request.POST.get('order')
        subs.create_json_from_folder(dir, OrderBy.getsort(order))
        # order = options.get('order')
        # subs.insert_lengua_text(subs.get_json(search, order))
        if all:
            folders = subs.get_options()
            while folders:
                subs.create_json_from_folder(folders.pop(), OrderBy.getsort(order))
        else:
            subs.create_json_from_folder(dir, OrderBy.getsort(order))
    return render(request, 'movies.html', {'form': SearchForm(),
                                           'Search': search,
                                           'Order': order,
                                           'Subs': subs.get_options(),
                                           'Jsons': subs.get_import_options(),
                                           "title": "Import Movies"})
