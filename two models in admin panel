class VenueEmailInline(admin.StackedInline):
    model = VenueEmail


class VenueAdmin(admin.ModelAdmin):
    inlines = [VenueEmailInline, ]
    list_display = ['name', 'user', 'website', 'is_visible']
    
# when you want add new Venue in admin panel added additional new Model in bottom VenueEmail.
