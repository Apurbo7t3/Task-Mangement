from django import forms
from tasks.models import Task,TaskDetail

class TaskForm(forms.Form):
    title=forms.CharField(max_length=100,label='Title ')
    description=forms.CharField(label='Description ',widget=forms.Textarea)
    due_date=forms.DateField(widget=forms.SelectDateWidget)
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self,*args, **kwargs):
        employee=kwargs.pop('employee')
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices=[(emp.id,emp.name) for emp in employee]


class TaskFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def style_fileds(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })


# Model form



class TaskModelForm(TaskFormMixin,forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description','assigned_to','due_date']
        widgets={
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fileds()

class TaskDetailModelForm(TaskFormMixin,forms.ModelForm):
    class Meta:
        model= TaskDetail
        fields= ['priority','notes']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fileds()