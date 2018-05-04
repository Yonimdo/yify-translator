from django.shortcuts import render, redirect

# Create your views here.
from movies.models import import_json
from movies.tools import subs, yify
from movies.tools.subs import OrderBy


def import_subtitles(request):
    search = ""
    order = ""
    if request.method == 'POST':
        # form = SearchForm()(request.POST)
        search = request.POST.get('search')
        yify.search_subtitles(search, 5)
        # order = options.get('order')
        # subs.insert_lengua_text(subs.get_json(search, order))
        # order = request.POST.get('order')
    if request.GET.get('import-json', None) == '':
        folders = subs.get_import_options()
        while folders:
            import_json(folders.pop()[0])
        return redirect('/import')
    if request.GET.get('create-json', None) == '':
        folders = subs.get_options()
        while folders:
            subs.create_json_from_folder(folders.pop(), OrderBy.getsort(order))
        return redirect('/import')
    return render(request, 'movies.html', {
        'Search': search,
        'Order': order,
        'subs': subs.get_options(),
        'jsons': subs.get_import_options(),
        "title": "Import Movies"})
