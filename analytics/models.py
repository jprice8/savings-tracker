from django.db import models


class Issue(models.Model):
    fac = models.CharField(null=False, max_length=10)
    issue_date = models.DateField(null=False)
    imms = models.CharField(null=False, max_length=10)
    qty = models.IntegerField(null=False, default=0)
    uom = models.CharField(null=False, max_length=10)

    class Meta:
        ordering = ('issue_date', )

    def __str__(self):
        return f'Fac: {self.fac}, IMMS: {self.imms}, Qty: {self.qty}'


class PO(models.Model):
    fac = models.CharField(null=False, max_length=10)
    po_date = models.DateField(null=False)
    imms = models.CharField(null=False, max_length=10)
    qty = models.IntegerField(null=False, default=0)
    uom = models.CharField(null=False, max_length=10)

    class Meta:
        ordering = ('po_date', )

    def __str__(self):
        return f'Fac: {self.fac}, IMMS: {self.imms}, Qty: {self.qty}'