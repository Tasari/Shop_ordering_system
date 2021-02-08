from django.db.models import Sum

class CostSumMixin:
    cost_field=None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        queryset = context['object_list']
        sum_total_cost = queryset.aggregate(sum_cost=Sum(self.cost_field))['sum_cost']
        context['sum_cost'] = "{:.2f}".format(float(sum_total_cost))
        return context