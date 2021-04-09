from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum

from .models import Conversion, OldItem, NewItem
from .forms import OldItemForm, NewItemForm

from analytics.models import Issue, PO

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
def edit_conversion(request, pk):
    # get conversion
    conversion = get_object_or_404(Conversion, pk=pk)

    # if request is post
    if request.method == 'POST':
        # process form
        conversion.conversion_name = request.POST['conversion_name']
        conversion.created_by = request.user
        conversion.start_date = request.POST['start_date']
        conversion.end_date = request.POST['end_date']
        conversion.facilities = request.POST.getlist('facilities')

        # save conversion to update
        conversion.save(update_fields=['conversion_name', 'created_by', 'start_date', 'end_date', 'facilities'])

        # successful edit
        messages.success(request, 'Conversion updated')
        return HttpResponseRedirect(reverse('conversions',))

    context = {
        'conversion': conversion,
    }

    return render(request, 'tracker/edit_conversion.html', context)

@login_required
def delete_conversion(request, pk):
    # get conversion
    conversion = get_object_or_404(Conversion, pk=pk)

    if request.method == 'POST':
        conversion.delete()
        messages.success(request, 'Conversion deleted')
        return HttpResponseRedirect(reverse('conversions',))

    context = {
        'conversion': conversion,
    }
    
    return render(request, 'tracker/confirm_delete_conversion.html', context)

@login_required
def conversion_detail(request, pk):
    #### Query data
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

    #### Gross savings per each
    gross_savings_per_each = 0
    old_gross_unit_cost = 0
    new_gross_unit_cost = 0
    for i in old_items:
        old_gross_unit_cost += i.unit_cost

    for i in new_items:
        new_gross_unit_cost += i.unit_cost

    # subtract old from new gross unit cost to get savings per each
    gross_savings_per_each += (old_gross_unit_cost - new_gross_unit_cost)

    # get proportional savings
    p_savings = {} 
    for i in new_items:
        # add proportional savings to step array
        p_multiplier = (i.unit_cost / new_gross_unit_cost)
        p_savings[i.description] = round(p_multiplier * gross_savings_per_each, 2) 


    #### New Item Purchase Orders
    # get list of new items imms no's
    new_imms = list(new_items.values_list('imms', flat=True))
    
    # filter pos by:
    # imms in new item array
    # in between conversion start and end date
    # fac is in conversion facilities array
    new_item_po = PO.objects.filter(
        imms__in=new_imms,
        po_date__gt=conversion.start_date,
        po_date__lt=conversion.end_date,
        fac__in=list(conversion.facilities),
    )

    # loop through imms nos and create intake object
    new_po_dict = {}
    for i in new_imms:
        new_po_dict[i] = 0
        for x in new_item_po:
            if i == x.imms:
                new_po_dict[i] += x.qty


    #### New Item Issues
    # filter issues by:

    new_item_issue = Issue.objects.filter(
        imms__in=new_imms,
        issue_date__gt=conversion.start_date,
        issue_date__lt=conversion.end_date,
        fac__in=list(conversion.facilities),
    )

    # loop through imms nos and create issue object
    new_issue_dict = {}
    for i in new_imms:
        new_issue_dict[i] = 0
        for x in new_item_issue:
            if i == x.imms:
                new_issue_dict[i] += x.qty

    total_intake_dict = {}
    for index in range(len(new_items)):
        step_iss = new_issue_dict[new_imms[index]]
        step_po = new_po_dict[new_imms[index]] 

        total_intake_dict[new_items[index].description] = step_iss + step_po


    #### New Item Conversion Savings
    savings_dict = {}
    for i in new_items:
        savings_dict[i.description] = total_intake_dict[i.description] * p_savings[i.description]

    net_savings = 0
    for i in new_items:
        net_savings += savings_dict[i.description]

    context = {
        # querysets
        'conversion': conversion,
        'old_items': old_items,
        'new_items': new_items,

        # metrics
        'p_savings': p_savings,
        'intake_dict': total_intake_dict,
        'savings_dict': savings_dict,
        'net_savings': net_savings,
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
