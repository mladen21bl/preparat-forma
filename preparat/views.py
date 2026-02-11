from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy


from .models import BiljniDodatak
from .forms import (
    BiljniDodatakForm,
    BiljnaDrogaFormSet,
    AktivnaSupstancaFormSet,
    StudijaFormSet,
)


class BiljniDodatakCreateView(CreateView):
    model = BiljniDodatak
    form_class = BiljniDodatakForm
    template_name = "preparat/test.html"
    success_url = reverse_lazy("uspjeh")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["droge_formset"] = BiljnaDrogaFormSet(self.request.POST)
            context["supstance_formset"] = AktivnaSupstancaFormSet(self.request.POST)
            context["studije_formset"] = StudijaFormSet(self.request.POST)
        else:
            context["droge_formset"] = BiljnaDrogaFormSet()
            context["supstance_formset"] = AktivnaSupstancaFormSet()
            context["studije_formset"] = StudijaFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        droge = context["droge_formset"]
        supstance = context["supstance_formset"]
        studije = context["studije_formset"]

        if droge.is_valid() and supstance.is_valid() and studije.is_valid():
            self.object = form.save()

            droge.instance = self.object
            supstance.instance = self.object
            studije.instance = self.object

            droge.save()
            supstance.save()
            studije.save()

            return redirect(self.success_url)

        return self.form_invalid(form)




def index(request):
    return render(request, 'preparat/index.html')


def test2(request):
    return render(request, 'preparat/test2.html')