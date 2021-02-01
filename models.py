import uuid
from django.db import models


class Detmir(models.Model):
    detmir_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detmir_fullprice = models.IntegerField()
    detmir_discprice = models.IntegerField(blank=True, null=True)
    detmir_date = models.ForeignKey('Dates', on_delete=models.DO_NOTHING)
    lego_sets_set = models.ForeignKey('LegoSets', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'detmir'
        verbose_name = 'Детский мир единица'
        verbose_name_plural = 'Детский мир база'

    def __str__(self):
        return str(self.detmir_date) + ' - ' + str(self.lego_sets_set)


class Wildberries(models.Model):
    wildberries_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wildberries_fullprice = models.IntegerField()
    wildberries_discprice = models.IntegerField(blank=True, null=True)
    wildberries_date = models.ForeignKey('Dates', on_delete=models.DO_NOTHING)
    lego_sets_set = models.ForeignKey('LegoSets', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'wildberries'
        verbose_name = 'Вайлдбериз единица'
        verbose_name_plural = 'Вайлдбериз база'

    def __str__(self):
        return str(self.wildberries_date) + ' - ' + str(self.lego_sets_set)


class LegoSets(models.Model):
    set_id = models.IntegerField(primary_key=True)
    set_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'lego_sets'
        verbose_name = 'Набор LEGO'
        verbose_name_plural = 'Наборы LEGO'

    def __str__(self):
        return self.set_name


class Dates(models.Model):
    date_id = models.DateField(primary_key=True)
    detmir_count = models.IntegerField(blank=True, null=True)
    wildberries_count = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['date_id']
        db_table = 'dates'
        verbose_name = 'Дата запросов'
        verbose_name_plural = 'Даты запросов'

    def __str__(self):
        return str(self.date_id)
