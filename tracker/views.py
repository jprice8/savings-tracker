from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Conversion, OldItem, NewItem
from .forms import OldItemForm, NewItemForm

@login_required
def index(request):
    return render(request, 'tracker/landing.html')

@login_required
def conversions(request):
    # get conversions
    conversions = Conversion.objects.all()

    context = {
        'conversions': conversions,
    }

    return render(request, 'tracker/conversions.html', context)

@login_required
def add_conversion(request):
    
    # if request is post
    if request.method == 'POST':
        # process form
        conversion_name = request.POST['conversion_name']
        created_by = request.user
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        facilities = request.POST.getlist('facilities')

        # create new conversion instance
        new_c = Conversion(
            conversion_name=conversion_name,
            created_by=created_by,
            start_date=start_date,
            end_date=end_date,
            facilities=facilities
        )
        new_c.save()

        messages.success(request, 'Conversion created!')
        return HttpResponseRedirect(reverse('conversions',))
        
    else:
        return render(request, 'tracker/add_conversion.html')

@login_required
def conversion_detail(request, pk):
    # get conversion
    conversion = get_object_or_404(Conversion, pk=pk)

    # get old items for conversion
    old_items = OldItem.objects.filter(
        conversion_plan=conversion,
    )

    # get new items for conversion
    new_items = NewItem.objects.filter(
        conversion_plan=conversion,
    )

    # We need metrics
    # Need to get POs and Issues models set up and populated
    # Get 

    context = {
        'conversion': conversion,
        'old_items': old_items,
        'new_items': new_items,
    }

    return render(request, 'tracker/detail.html', context)

@login_required
def add_old_item(request, pk):
    # get parent conversion
    conversion = get_object_or_404(Conversion, pk=pk)

    # if POST, clean and submit form
    if request.method == 'POST':
        form = OldItemForm(request.POST)
        form.instance.created_by = request.user
        form.instance.conversion_plan = conversion
        
        if form.is_valid():
            # create new instance
            form.save()
            messages.success(request, 'Old Item created!')
            return HttpResponseRedirect(reverse('conversion-detail', args=(pk,)))
    # if GET, render form
    else:
        form = OldItemForm()

    context = {
        'form': form,
    }

    return render(request, 'tracker/add_old_item.html', context)

@login_required
def add_new_item(request, pk):
    # get parent conversion
    conversion = get_object_or_404(Conversion, pk=pk)

    # if POST, clean and submit form
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        form.instance.created_by = request.user
        form.instance.conversion_plan = conversion
        
        if form.is_valid():
            # create new instance
            form.save()
            messages.success(request, 'New Item created!')
            return HttpResponseRedirect(reverse('conversion-detail', args=(pk,)))
    # if GET, render form
    else:
        form = NewItemForm()

    context = {
        'form': form,
    }

    return render(request, 'tracker/add_new_item.html', context)

    
