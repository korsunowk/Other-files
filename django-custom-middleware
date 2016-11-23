class WelcomeBackWindow(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not request.COOKIES.get('welcome_back_window') and request.user.is_authenticated() \
                    and request.user.venue and not request.user.venue.subscribed \
                    and request.user.venue.subscription is None and not request.user.venue.beta_user \
                    and not request.user.venue.fail_with_charge:
                request.COOKIES['welcome_back_window'] = 'true'
        except:
            pass
            
##########
MIDDLEWARE_CLASSES = (
    #####
    'sonum.middleware.WelcomeBackWindow'
    ###
)
