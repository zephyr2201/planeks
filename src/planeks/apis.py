import mimetypes
import logging
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from django.urls.base import reverse
from django.contrib.auth.models import Permission, User
from django.http.response import HttpResponse, HttpResponseRedirect

from .tasks import writer_csv
from .forms import UserRegistrationForm
from .selectors import fetch_csv
from rest_framework import serializers, status
from django.core.files.base import ContentFile


MODELS_VIEW = ['New schema', 'column']
PERMISSIONS_VIEW = ['view', 'change', 'delete', 'add']


class Callback(APIView):
    class InputSerializer(serializers.Serializer):
        file_uploaded = serializers.FileField()
        obj = serializers.IntegerField()

        class Meta:
            fields = ['file_uploaded']

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES['file_uploaded']
        pk = request.data.get('obj')
        csv_obj = fetch_csv(pk)
        csv_obj.csv_file = ContentFile(
            file.read(),
            name=f'{csv_obj.name}.csv'
        )
        csv_obj.save()
        return Response(
                {'result': 1, 'success': True},
                status=status.HTTP_201_CREATED
            )


def download_file(request, pk: int):
    print(request)
    obj = fetch_csv(pk)
    file = obj.csv_file
    filename = f'/code/src/{file}'
    mime_type, _ = mimetypes.guess_type(filename)
    with open(filename, 'r') as f:
        response = HttpResponse(f, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={obj.name}.csv'
    return response


def process_generate(request, pk: int):
    header = []
    types = []
    port = request.META['SERVER_PORT']
    csv_obj = fetch_csv(pk)
    for column in csv_obj.columns.all().order_by('order'):
        header.append(column.column_name)
        types.append(column.type)
    writer_csv.delay(pk, types, header, port)
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
            # Add permissions
            set_permissions(new_user)
            return render(
                request, 'planeks/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request, 'planeks/register.html',
        {'user_form': user_form}
    )


def set_permissions(user: User) -> None:
    for model in MODELS_VIEW:
        for permission in PERMISSIONS_VIEW:
            name = 'Can {} {}'.format(permission, model)
            print("Creating {}".format(name))

            try:
                model_add_perm = Permission.objects.get(name=name)
            except Permission.DoesNotExist:
                logging.warning(
                    "Permission not found with name '{}'.".format(name)
                )
                continue
            user.user_permissions.add(model_add_perm)
