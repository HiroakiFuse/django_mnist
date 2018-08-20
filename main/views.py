import base64
from django.shortcuts import render,redirect
from django.views import generic
import numpy as np
from PIL import Image
from .cnn.simple_convnet import SimpleConvNet
# Create your views here.


network = SimpleConvNet(
    input_dim=(1,28,28),hidden_size=100,output_size=10)
network.load_params('params.pkl')

class Home(generic.TemplateView):
    template_name = 'home.html'

def upload(request):
    files = request.FILES.getlist("files[]")
    if request.method == 'POST' and files:
        array_list = []
        for file in files:
            img = Image.open(file)
            array = np.asarray(img)
            array_list.append(array)
        x = np.array(array_list).reshape(len(array_list), 1, 28, 28)
        labels = network.predict(x).argmax(axis=1)
        result = []
        for file, label in zip(files, labels):
            file.seek(0)
            src = base64.b64encode(file.read())
            result.append((src, label))
        context = {
            'result': result,
        }
        return render(request, 'result.html', context)
    else:
        return redirect('home')
