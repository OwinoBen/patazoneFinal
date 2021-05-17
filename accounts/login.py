from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth


def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username', '')
        psword = request.POST.get('password', '')
        user = auth.authenticate(username=uname, password=psword)
        # if the user logs in and is active
        if user is not None and user.is_active:
            auth.login(request, user)
            return render_to_response('main/main.html', {}, context_instance=RequestContext(request))
            # return redirect(main_view)
        else:
            return render_to_response('loginpage.html', {'box_width': '402', 'login_failed': '1', },
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('loginpage.html', {'box_width': '400', }, context_instance=RequestContext(request))


def logout_view(request):
    auth.logout(request)
    return render_to_response('loginpage.html', {'box_width': '402', 'logged_out': '1', },
                              context_instance=RequestContext(request))
