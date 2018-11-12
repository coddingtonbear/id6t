from django.contrib import admin

from .models import DataType, Data, DataSet

# Register your models here.


class DataTypeAdmin(admin.ModelAdmin):
    ordering = ('name', )
    search_fields = ('name', )
    list_display = ('name', 'slug', 'type', )


class DataSetAdmin(admin.ModelAdmin):
    ordering = ('-created', )
    list_display = ('id', 'created', )
    list_filter = ('created', )


class DataAdmin(admin.ModelAdmin):
    ordering = ('-id', )
    list_display = ('type', 'value', )
    list_filter = ('type', 'dataset__created', )
    raw_id_fields = ('dataset', )


admin.site.register(Data, DataAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataType, DataTypeAdmin)
