from django import forms

from .models import Propiedad


class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
            "titulo",
            "descripcion",
            "ciudad",
            "direccion",
            "tamano",
            "capacidad_maxima",
            "precio_por_noche",
            "tiene_piscina",
            "tiene_jardin",
            "tiene_wifi",
            "admite_mascotas",
            "tiene_aire_acondicionado",
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all",
                    "rows": 4,
                }
            ),
            "ciudad": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                }
            ),
            "tamano": forms.NumberInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all",
                    "min": "1",
                }
            ),
            "capacidad_maxima": forms.NumberInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all",
                    "min": "1",
                }
            ),
            "precio_por_noche": forms.NumberInput(
                attrs={
                    "class": "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all",
                    "step": "0.01",
                }
            ),
            "tiene_wifi": forms.CheckboxInput(
                attrs={
                    "class": "rounded text-blue-500 focus:ring-blue-500 bg-gray-900 border-gray-700 h-4 w-4"
                }
            ),
            "tiene_piscina": forms.CheckboxInput(
                attrs={
                    "class": "rounded text-blue-500 focus:ring-blue-500 bg-gray-900 border-gray-700 h-4 w-4"
                }
            ),
            "tiene_jardin": forms.CheckboxInput(
                attrs={
                    "class": "rounded text-blue-500 focus:ring-blue-500 bg-gray-900 border-gray-700 h-4 w-4"
                }
            ),
            "admite_mascotas": forms.CheckboxInput(
                attrs={
                    "class": "rounded text-blue-500 focus:ring-blue-500 bg-gray-900 border-gray-700 h-4 w-4"
                }
            ),
            "tiene_aire_acondicionado": forms.CheckboxInput(
                attrs={
                    "class": "rounded text-blue-500 focus:ring-blue-500 bg-gray-900 border-gray-700 h-4 w-4"
                }
            ),
        }
