class GameGetTeamTagsByField(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['processed', ]
    serializer_class = TeamTagAdminSerializer

    def get_queryset(self):
        return TeamTag.objects.filter(deleted=0, game__id=self.kwargs.get('pk'),
                                      offensive_team__id=self.request.query_params.get('Team'))\
            .order_by('id')
