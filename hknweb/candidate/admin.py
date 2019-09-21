from django.contrib import admin
from .models import OffChallenge, Announcement
from django.contrib.auth.models import User
from django.http import HttpResponse

import csv


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'reviewed', 'confirmed', 'description', 'proof', 'officer_comment', 'request_date']
    readonly_fields = ['request_date']
    list_display = ('name', 'requester', 'officer', 'reviewed', 'confirmed', 'request_date')
    list_filter = ['requester', 'officer', 'request_date']
    search_fields = ['requester', 'officer', 'name']

    actions = ["export_as_csv"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by('username')
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # @source: http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected as csv"


class AnnouncementAdmin(admin.ModelAdmin):

    fields = ['title', 'text', 'visible', 'release_date']
    readonly_fields = ['release_date']
    list_display = ('title', 'visible', 'release_date')
    list_filter = ['visible', 'release_date']
    search_fields = ['title', 'text']

    actions = ["set_visible", "set_invisible"]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)

    set_visible.short_description = "Set selected as visible"
    set_invisible.short_description = "Set selected as invisible"


admin.site.register(OffChallenge, OffChallengeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
