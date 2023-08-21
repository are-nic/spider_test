from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)

        if search_param:
            queryset = queryset.filter(items__item__name__trigram_similar=search_param)
            return queryset
        return super().filter_queryset(request, queryset, view)