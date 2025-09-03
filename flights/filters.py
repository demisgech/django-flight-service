
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet


class CustomerLoyaltyPointsFilter(admin.SimpleListFilter):
    title = 'Loyalty Points'
    parameter_name = 'loyalty_points'
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("<1000","Below 1000 points"),
            (">1000",'About 1000 points')
        ]
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "<1000":
            return queryset.filter(loyalty_points__lte=1000)
        if self.value() == ">1000":
            return queryset.filter(loyalty_points__gt=1000)
        return None
    
    
