class TicketPriceUpdateView(OnlyVenueLoginRequiredMixin, generic.UpdateView):
    model = Application
    fields = ['ticket_resale_price', 'ticket_dayoff_price']

    def form_valid(self, form):
        form.save()

        Group("calendar-{0}".format(self.kwargs['pk'])).send({
            "text": json.dumps({'action': 'ticket', 'application_id': self.object.pk,
                                'data': render_to_string('_partials/_event_tickets.html',
                                                         {'application': self.object})})
        })

        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False})
