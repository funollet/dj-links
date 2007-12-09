from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import markdown


@user_passes_test(lambda u: u.is_staff)
def preview (request):
    """Parses the value of the 'markup' field (POST). Used on the Admin
    preview button.
    """
    
    html = markdown.markdown ( request.POST['markup'] )
    return HttpResponse (html)
