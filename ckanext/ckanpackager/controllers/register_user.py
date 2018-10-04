from ckan import model, authz, logic
from ckan.common import c, request
from ckan.controllers.user import check_access, NotAuthorized, abort, UserController, render, unflatten, get_action, \
    NotFound, DataError, ValidationError, set_repoze_user
import ckan.plugins.toolkit as t
from ckan.lib import captcha
import ckan.lib.helpers as h

from ckanext.ckanpackager.lib.swot.swot import Swot
from ckanext.ckanpackager.model.UserInfo import BIDUserInfo

_ = t._


class CustomUserController(UserController):

    def register(self, data=None, errors=None, error_summary=None):
        print('Custom user controller found')

        context = {'model': model, 'session': model.Session, 'user': c.user,
                   'auth_user_obj': c.userobj}

        # TODO grab the why?? field and save it

        try:
            check_access('user_create', context)
        except NotAuthorized:
            abort(403, _('Unauthorized to register as a user.'))

        res = self.new(data, errors, error_summary)

        # If user created, we don't reach this point - self.new() above redirects
        return self.new(data, errors, error_summary)

    def new(self, data=None, errors=None, error_summary=None):
        '''GET to display a form for registering a new user.
           or POST the form data to actually do the user registration.
        '''
        context = {'model': model,
                   'session': model.Session,
                   'user': c.user,
                   'auth_user_obj': c.userobj,
                   'schema': self._new_form_to_db_schema(),
                   'save': 'save' in request.params}

        try:
            check_access('user_create', context)
        except NotAuthorized:
            abort(403, _('Unauthorized to create a user'))

        if context['save'] and not data:
            return self._save_new(context)

        if c.user and not data and not authz.is_sysadmin(c.user):
            # #1799 Don't offer the registration form if already logged in
            return render('user/logout_first.html')

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        c.is_sysadmin = authz.is_sysadmin(c.user)
        c.form = render(self.new_user_form, extra_vars=vars)
        return render('user/new.html')

    def _save_new(self, context):
        print(request.params)
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))

            self._validate_academic_email(request.params['email'])
            self._validate_eula_accept(request.params)

            context['message'] = data_dict.get('log_message', '')
            captcha.check_recaptcha(request)

            user = get_action('user_create')(context, data_dict)
            self._after_signup(user)

        except NotAuthorized:
            abort(403, _('Unauthorized to create user %s') % '')
        except NotFound, e:
            abort(404, _('User not found'))
        except DataError:
            abort(400, _(u'Integrity Error'))
        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.new(data_dict)
        except ValidationError, e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.new(data_dict, errors, error_summary)
        if not c.user:
            # log the user in programatically
            set_repoze_user(data_dict['name'])
            h.redirect_to(controller='user', action='me')
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.
            h.flash_success(_('User "%s" is now registered but you are still '
                              'logged in as "%s" from before') %
                            (data_dict['name'], c.user))
            if authz.is_sysadmin(c.user):
                # the sysadmin created a new user. We redirect him to the
                # activity page for the newly created user
                h.redirect_to(controller='user',
                              action='activity',
                              id=data_dict['name'])
            else:
                return render('user/logout_first.html')

    def _after_signup(self, user_object):

        print(user_object)
        print(type(user_object))

        print(request.params)

        if 'why' in request.params:
            print('saving new user info')

            userinfo = BIDUserInfo(
                user=user_object['id'],
                signup_reason = request.params['why']
            )

            model.Session.add(userinfo)
            model.Session.commit()
        else:
            print('no user info to save')

    def _validate_academic_email(self, email):
        if len(email) and '@' in email:
            email = email.split('@')[1]
            if not Swot.is_academic(email):
                raise ValidationError(
                    {
                        'email': ['This is not a valid academic email for signup']
                    }
                )
        else:
            raise ValidationError(
                {
                    'email': ['This is not a valid academic email for signup']
                }
            )

    def _validate_eula_accept(self, request_params):

        agreement_steps = ['accept_1', 'accept_2', 'accept_3', 'accept_4',
                           'accept_5', 'accept_6', 'accept_7', 'accept_8',
                           'accept_9', 'accept_10', 'accept_11']

        for a in agreement_steps:
            if not a in request_params :
                raise ValidationError(
                    {
                        'letter_of_understanding_acceptance': ['You must accept all parts of the Letter of Understanding to continue']
                    }
                )