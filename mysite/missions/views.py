from mysite.base.decorators import view
from mysite.missions.controllers import TarMission, TarUploadForm, IncorrectTarFile

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

@view
def main_page(request):
    return (request, 'missions/main.html', {})

@view
def diffpatch_info(request):
    return (request, 'missions/diffpatch_info.html', {})

def diffpatch_start(request):
    # TODO: mark mission as in progress
    return HttpResponseRedirect(reverse(diffpatch_progress))

@view
def diffpatch_progress(request):
    # TODO: make the mission actually do stuff
    return (request, 'missions/diffpatch_progress.html', {})

@view
def tar_upload(request):
    data = {'success': False, 'what_was_wrong_with_the_tarball': ''}
    if request.method == 'POST':
        form = TarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                TarMission.check_tarfile(form.cleaned_data['tarfile'].read())
                data['success'] = True
            except IncorrectTarFile, e:
                data['what_was_wrong_with_the_tarball'] = str(e)
        data['form'] = form
    else:
        data['form'] = TarUploadForm()
    return (request, 'missions/tar_upload.html', data)

def tar_file_download(request, name):
    if name in TarMission.FILES:
        response = HttpResponse(TarMission.FILES[name])
        # force it to be presented as a download
        response['Content-Disposition'] = 'attachment; filename=%s' % name
        response['Content-Type'] = 'application/octet-stream'
        return response
    else:
        raise Http404