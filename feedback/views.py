
from .models import *
from django.http import HttpResponseRedirect
from techniqueOrder.models import *

# Create your views here.
def create_feedback(request):
    order = TechniqueOrder.objects.get(id=request.POST.get('id'))


    if request.POST.get('type') == 'by_w':
        UserFeedback.objects.create(from_user=order.worker,
                                    about_user=order.customer,
                                    rating=request.POST.get('rating'),
                                    text=request.POST.get('feedback'))

        order.customer.rate_times += 1
        order.customer.rating += int(request.POST.get('rating'))
        order.customer.save()
        order.worker_feedback = True
        order.save()
    if request.POST.get('type') == 'by_c':
        selected_apply= TechniqueOrderApply.objects.get(id=order.order_apply)
        TechniqueFeedback.objects.create(from_user=order.customer,
                                         techniqueitem=selected_apply.technique,
                                         rating=request.POST.get('rating'),
                                         text=request.POST.get('feedback'))

        selected_apply.technique.rate_times +=1
        selected_apply.technique.rating += int(request.POST.get('rating'))
        selected_apply.technique.save()
        order.customer_feedback = True
        order.save()

    return HttpResponseRedirect('/')
