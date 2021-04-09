from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Sum
from django.urls import reverse
from django.contrib import messages

from .models import Issue, PO
from tracker.models import Conversion, OldItem, NewItem
from tracker.forms import OldItemForm, NewItemForm

@login_required
def analytics(request, pk):
    #### Query data

    # get conversion
    conversion = get_object_or_404(Conversion, pk=pk)
    # old items
    old_items = OldItem.objects.filter(
        conversion_plan=conversion,
    )
    # new items
    new_items = NewItem.objects.filter(
        conversion_plan=conversion,
    )

    #### Get savings over time for chart.
    #### Need to be able to filter by facility.


    context = {
        'conversion': conversion,
    }

    return render(request, 'analytics/analytics.html', context)

def savings_chart(request, pk):
    #### Get Querysets
    # get conversion
    conversion = get_object_or_404(Conversion, pk=pk)
    # get items
    old_items = OldItem.objects.filter(conversion_plan=conversion)
    new_items = NewItem.objects.filter(conversion_plan=conversion)

    # get list of new imms #s
    new_imms = list(new_items.values_list('imms', flat=True))

    # filter pos
    new_po = PO.objects.filter(
        imms__in=new_imms,
        po_date__gt=conversion.start_date,
        po_date__lt=conversion.end_date,
        fac__in=list(conversion.facilities),
    ).values_list(
        'po_date__year', 
        'po_date__month'
    ).annotate(
        Sum('qty')
    ).order_by(
        'po_date__year',
        'po_date__month',
    )

    print(new_po)

    # filter issues
    new_iss = Issue.objects.filter(
        imms__in=new_imms,
        issue_date__gt=conversion.start_date,
        issue_date__lt=conversion.end_date,
        fac__in=list(conversion.facilities),
    ).values_list(
        'issue_date__year',
        'issue_date__month',
    ).annotate(
        Sum('qty')
    ).order_by(
        'issue_date__year',
        'issue_date__month',
    )

    print(new_iss)

    total_labels = []
    total_data = []
    for i in new_po:
        total_labels.append(i[1])
        total_data.append(i[2])

    return JsonResponse(data={
        'total_labels': total_labels,
        'total_data': total_data,
    })

@login_required
def old_item_detail(request, pk):
    # get item
    item = get_object_or_404(OldItem, pk=pk)

    context = {
        'item': item,
        'new': False,
    }

    return render(request, 'analytics/item_detail.html', context)

@login_required
def old_item_edit(request, pk):
    # get item
    item = get_object_or_404(OldItem, pk=pk)

    # if request is post
    if request.method == 'POST':
        # process form
        item.imms = request.POST['imms']
        item.poum = request.POST['poum']
        item.uom_conv_factor = request.POST['uom_conv_factor']
        item.luom = request.POST['luom']
        item.mfr = request.POST['mfr']
        item.mfr_cat_no = request.POST['mfr_cat_no']
        item.unit_cost = request.POST['unit_cost']

        # save item to update
        item.save(update_fields=[
            'imms',
            'poum',
            'uom_conv_factor',
            'luom',
            'mfr',
            'mfr_cat_no',
            'unit_cost',
        ])

        # successful edit
        messages.success(request, 'Item updated')
        return HttpResponseRedirect(reverse('old-item-detail', args=(pk,)))

    context = {
        'item': item,
    }

    return render(request, 'analytics/edit_item.html', context)

@login_required
def old_item_delete(request, pk):
    # get item
    item = get_object_or_404(OldItem, pk=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted')
        return HttpResponseRedirect(reverse('conversions',))

    context = {
        'item': item,
        'new': False,
    }

    return render(request, 'analytics/confirm_delete_item.html', context)


@login_required
def new_item_detail(request, pk):
    # get item
    item = get_object_or_404(NewItem, pk=pk)

    context = {
        'item': item,
        'new': True,
    }

    return render(request, 'analytics/item_detail.html', context)

@login_required
def new_item_edit(request, pk):
    # get item
    item = get_object_or_404(NewItem, pk=pk)

    # if request is post
    if request.method == 'POST':
        # process form
        item.imms = request.POST['imms']
        item.poum = request.POST['poum']
        item.uom_conv_factor = request.POST['uom_conv_factor']
        item.luom = request.POST['luom']
        item.mfr = request.POST['mfr']
        item.mfr_cat_no = request.POST['mfr_cat_no']
        item.unit_cost = request.POST['unit_cost']

        # save item to update
        item.save(update_fields=[
            'imms',
            'poum',
            'uom_conv_factor',
            'luom',
            'mfr',
            'mfr_cat_no',
            'unit_cost',
        ])

        # successful edit
        messages.success(request, 'Item updated')
        return HttpResponseRedirect(reverse('new-item-detail', args=(pk,)))

    else:
        form = NewItemForm()

    context = {
        'item': item,
        'form': form,
    }

    return render(request, 'analytics/edit_item.html', context)

@login_required
def new_item_delete(request, pk):
    # get item
    item = get_object_or_404(NewItem, pk=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted')
        return HttpResponseRedirect(reverse('conversions',))

    context = {
        'item': item,
        'new': True,
    }

    return render(request, 'analytics/confirm_delete_item.html', context)