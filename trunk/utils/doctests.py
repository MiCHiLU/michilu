from urlparse import urlparse, urljoin
from django.test.client import Client
from django.core import management
from django.db.models import get_app, get_apps


class TestBase(object):
    def assertRedirects(self, response, expected_path, status_code=302, target_status_code=200, \
                            base_path=None):
        """Assert that a response redirected to a specific URL, and that the
        redirect URL can be loaded.
        
        """
        self.assertEqual(response.status_code, status_code, 
            "Response didn't redirect as expected: Reponse code was %d (expected %d)" % 
                (response.status_code, status_code))
        scheme, netloc, path, params, query, fragment = urlparse(response['Location'])
        self.assertEqual(path, expected_path, 
            "Response redirected to '%s', expected '%s'" % (path, expected_path))
        path = urljoin(base_path or "", path)
        redirect_response = self.client.get(path)
        self.assertEqual(redirect_response.status_code, target_status_code, 
            "Couldn't retrieve redirection page '%s': response code was %d (expected %d)" % 
                (path, redirect_response.status_code, target_status_code))
    
    def assertContains(self, response, text, count=1, status_code=200):
        """Assert that a response indicates that a page was retreived successfully,
        (i.e., the HTTP status code was as expected), and that ``text`` occurs ``count``
        times in the content of the response.
        
        """
        self.assertEqual(response.status_code, status_code,
            "Couldn't retrieve page: Response code was %d (expected %d)'" % 
                (response.status_code, status_code))
        real_count = response.content.count(text)
        self.assertEqual(real_count, count,
            "Found %d instances of '%s' in response (expected %d)" % (real_count, text, count))
    
    def assertFormError(self, response, form, field, errors):
        "Assert that a form used to render the response has a specific field error"
        if not response.context:
            self.fail('Response did not use any contexts to render the response')

        # If there is a single context, put it into a list to simplify processing
        if not isinstance(response.context, list):
            contexts = [response.context]
        else:
            contexts = response.context

        # If a single error string is provided, make it a list to simplify processing
        if not isinstance(errors, list):
            errors = [errors]
        
        # Search all contexts for the error.
        found_form = False
        for i,context in enumerate(contexts):
            if form in context:
                found_form = True
                for err in errors:
                    if field:
                        if field in context[form].errors:
                            self.failUnless(err in context[form].errors[field], 
                            "The field '%s' on form '%s' in context %d does not contain the error '%s' (actual errors: %s)" % 
                                (field, form, i, err, list(context[form].errors[field])))
                        elif field in context[form].fields:
                            self.fail("The field '%s' on form '%s' in context %d contains no errors" % 
                                (field, form, i))
                        else:
                            self.fail("The form '%s' in context %d does not contain the field '%s'" % (form, i, field))
                    else:
                        self.failUnless(err in context[form].non_field_errors(), 
                            "The form '%s' in context %d does not contain the non-field error '%s' (actual errors: %s)" % 
                                (form, i, err, list(context[form].non_field_errors())))
        if not found_form:
            self.fail("The form '%s' was not used to render the response" % form)
            
    def assertTemplateUsed(self, response, template_name):
        "Assert that the template with the provided name was used in rendering the response"
        if isinstance(response.template, list):
            template_names = [t.name for t in response.template]
            self.failUnless(template_name in template_names,
                "Template '%s' was not one of the templates used to render the response. Templates used: %s" %
                    (template_name, template_names))
        elif response.template:
            self.assertEqual(template_name, response.template.name,
                "Template '%s' was not used to render the response. Actual template was '%s'" %
                    (template_name, response.template.name))
        else:
            self.fail('No templates used to render the response')

    def assertTemplateNotUsed(self, response, template_name):
        "Assert that the template with the provided name was NOT used in rendering the response"
        if isinstance(response.template, list):            
            self.failIf(template_name in [t.name for t in response.template],
                "Template '%s' was used unexpectedly in rendering the response" % template_name)
        elif response.template:
            self.assertNotEqual(template_name, response.template.name,
                "Template '%s' was used unexpectedly in rendering the response" % template_name)


    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        print msg

    def failIf(self, expr, msg=None):
        "Fail the test if the expression is true."
        if expr: print msg

    def failUnless(self, expr, msg=None):
        """Fail the test unless the expression is true."""
        if not expr: print msg

    def failUnlessRaises(self, excClass, callableObj, *args, **kwargs):
        """Fail unless an exception of class excClass is thrown
           by callableObj when invoked with arguments args and keyword
           arguments kwargs. If a different type of exception is
           thrown, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.
        """
        try:
            callableObj(*args, **kwargs)
        except excClass:
            return
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            print "%s not raised" % excName

    def failUnlessEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.
        """
        if not first == second:
            print (msg or '%r != %r' % (first, second))

    def failIfEqual(self, first, second, msg=None):
        """Fail if the two objects are equal as determined by the '=='
           operator.
        """
        if first == second:
            print (msg or '%r == %r' % (first, second))

    def failUnlessAlmostEqual(self, first, second, places=7, msg=None):
        """Fail if the two objects are unequal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most signficant digit).
        """
        if round(second-first, places) != 0:
            print (msg or '%r != %r within %r places' % (first, second, places))

    def failIfAlmostEqual(self, first, second, places=7, msg=None):
        """Fail if the two objects are equal as determined by their
           difference rounded to the given number of decimal places
           (default 7) and comparing to zero.

           Note that decimal places (from zero) are usually not the same
           as significant digits (measured from the most signficant digit).
        """
        if round(second-first, places) == 0:
            print (msg or '%r == %r within %r places' % (first, second, places))

    assertEqual = assertEquals = failUnlessEqual

    assertNotEqual = assertNotEquals = failIfEqual

    assertAlmostEqual = assertAlmostEquals = failUnlessAlmostEqual

    assertNotAlmostEqual = assertNotAlmostEquals = failIfAlmostEqual

    assertRaises = failUnlessRaises

    assert_ = assertTrue = failUnless

    assertFalse = failIf


def to_tuple(args):
    if isinstance(args, basestring):
        args = (args,)
    return args

def reset(app_label=None, verbosity=0):
    app_labels = to_tuple(app_label)

    if (not app_labels) or (len(app_labels) == 0):
        app_list = get_apps()
    else:
        app_list = [get_app(app_label) for app_label in app_labels]

    if verbosity:
        print "Reset databases..."
    for app in app_list:
        try:
            management.reset(app, interactive=False)
            if verbosity:
                print "  %s" % app.__name__
        except IndexError:
            pass

def loaddata(fixtures, verbosity=0):
    fixtures = fixtures or None
    if not fixtures:
        return
    fixtures = to_tuple(fixtures)

    if fixtures:
        management.load_data(fixtures, verbosity)

def flush(verbosity=0):
    management.flush(verbosity, interactive=False)


class Test(TestBase):
    def __init__(self, fixtures=None, auth=None, **extra):
        self.extra = extra
        self.fixtures = fixtures
        self.auth = auth
        self.logined = None
        self.set_client()
        if self.auth:
            self.login()
        self.c = self.client

    def login(self, auth=None):
        if auth:
            _auth = auth
        else:
            _auth = self.auth
        self.logined = self.client.login(**_auth)

    def logout(self):
        self.set_client()
        self.logined = None

    def set_client(self):
        _extra = {}
        if hasattr(self, 'cookies'):
            _extra["HTTP_COOKIE"] = self.cookies
        if hasattr(self, 'ipaddr'):
            _extra["REMOTE_ADDR"] = self.ipaddr
        _extra.update(self.extra)
        self.client = Client(**_extra)

    def refresh_data(self, app_label=None, fixtures=None, verbosity=0):
        reset(app_label, verbosity)
        if (not fixtures) and hasattr(self, 'fixtures'):
            fixtures = self.fixtures
        loaddata(fixtures, verbosity)

    redirect_status_code = (301, 302)

    def assertUrlsDict(self, urls_dict):
        for key, value in urls_dict.items():
            if value[0] in self.redirect_status_code:
                base_path, status_code, expected_path = key, value[0], value[1]
                response = self.client.get(base_path)
                self.assertRedirects(response, expected_path, status_code=status_code, \
                                        base_path=base_path)
            elif isinstance(value[0], int):
                base_path, status_code = key, value[0]
                response = self.client.get(base_path)
                self.assertEqual(response.status_code, status_code, 
                    "Response didn't redirect as expected: Reponse code was %d (expected %d). in '%s'" % 
                        (response.status_code, status_code, key))
                try:
                    if not value[1]:
                        continue
                except IndexError:
                    continue
                if isinstance(value[1], str):
                    self.assertTemplateUsed(response, value[1])
                else:
                    [self.assertTemplateUsed(response, template_name) for template_name in value[1]]
            else:
                print "Bad test. '%s': %s" % (key, value)
