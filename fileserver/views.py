# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect

from mimetypes import guess_type

from models import SecureFile


@login_required
def serve(request, basename):
    """ Serve file from repository folder to HTTP client """

    secure_file = get_object_or_404(SecureFile, anonymous_file__contains=basename)
    if request.user in secure_file.users.all() or not secure_file.users.all():  # Empty user list means public access
        secure_file.anonymous_file.open('rb')
        content = secure_file.anonymous_file.read()
        secure_file.anonymous_file.close()
        # Should we check this more thoroughly?
        (mimetype, encoding) = guess_type(secure_file.name)

        response = HttpResponse(content, mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=' + secure_file.name.encode("us-ascii", "replace")

        return response
    else:
        raise Http404
