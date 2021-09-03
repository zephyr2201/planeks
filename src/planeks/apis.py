import mimetypes

from django.urls.base import reverse
from .tasks import writer_csv
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import UserRegistrationForm
from .selectors import fetch_csv


def download_file(request, pk):
    print(request)
    obj = fetch_csv(pk)
    file = obj.csv_file
    filename = f'/code/src/{file}'
    mime_type, _ = mimetypes.guess_type(filename)
    with open(filename, 'r') as f:
        response = HttpResponse(f, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={obj.name}.csv'
    return response


def process_generate(request, pk):
    header = []
    types = []
    csv_obj = fetch_csv(pk)
    for column in csv_obj.columns.all().order_by('order'):
        header.append(column.column_name)
        types.append(column.type)
    writer_csv.delay(pk, types, header)
    url = reverse('admin:planeks_csv_changelist')
    return HttpResponseRedirect(url)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_staff = True
            # Save the User object
            new_user.save()
            return render(request, 'planeks/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'planeks/register.html', {'user_form': user_form})
