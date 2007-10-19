# -*- coding: utf-8 -*-
"""
>>> from django.core import mail
>>> from django.test import TestCase
>>> mail.outbox = []

>>> mail.send_mail('Subject here', 'Here is the message.',
...     'from@example.com', ['to@example.com'],
...     fail_silently=False)
1
>>> len(mail.outbox)
1
>>> mail.outbox[0].subject
'Subject here'

>>> email = mail.EmailMessage('Hello', 'Body goes here', 'from@example.com',
...     ['to1@example.com', 'to2@example.com'], ['bcc@example.com'],
...     headers = {'Reply-To': 'another@example.com'})

#>>> email.message().__dict__
#{'_headers': [('Content-Type', 'text/plain; charset="utf-8"'), ('MIME-Version', '1.0'), ('Content-Transfer-Encoding', 'quoted-printable'), ('Subject', 'Hello'), ('From', 'from@example.com'), ('To', 'to1@example.com, to2@example.com'), ('Date', 'Tue, 02 Oct 2007 14:05:05 -0000'), ('Message-ID', '<20071002140505.1952.80902@st0141.mas1201.iidabashi.nttpc.ne.jp>'), ('Bcc', 'bcc@example.com'), ('Reply-To', 'another@example.com')], '_payload': 'Body goes here', '_charset': utf-8, '_default_type': 'text/plain', 'preamble': None, 'defects': [], '_unixfrom': None, 'epilogue': None}
#>>> email.message().as_string()
#'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nSubject: Hello\nFrom: from@example.com\nTo: to1@example.com, to2@example.com\nDate: Tue, 02 Oct 2007 14:05:05 -0000\nMessage-ID: <20071002140505.1952.61920@st0141.mas1201.iidabashi.nttpc.ne.jp>\nBcc: bcc@example.com\nReply-To: another@example.com\n\nBody goes here'

>>> email.message().__dict__.keys()
['_headers', '_payload', '_charset', '_default_type', 'preamble', 'defects', '_unixfrom', 'epilogue']
>>> [header[0] for header in email.message()._headers]
['Content-Type', 'MIME-Version', 'Content-Transfer-Encoding', 'Subject', 'From', 'To', 'Date', 'Message-ID', 'Bcc', 'Reply-To']


>>> test_print(email)
([('Content-Type', 'text/plain; charset="utf-8"'), ('Subject', 'Hello')], 'Body goes here')

>>> subject = u"テスト Subject here"
>>> body = u"テスト Here is the message."
>>> email = mail.EmailMessage(subject, body, 'from@example.com', ['to1@example.com'])

>>> test_print(email)
([('Content-Type', 'text/plain; charset="utf-8"'), ('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?=')], '=C3=A3=C2=83=C2=86=C3=A3=C2=82=C2=B9=C3=A3=C2=83=C2=88 Here is the message.')

>>> email = mail.EmailMessage(subject, body, 'from@example.com', ['to1@example.com'])
>>> test_print(email)
([('Content-Type', 'text/plain; charset="utf-8"'), ('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?=')], '=C3=A3=C2=83=C2=86=C3=A3=C2=82=C2=B9=C3=A3=C2=83=C2=88 Here is the message.')

>>> message = email.message()
>>> message._charset
utf-8
>>> message.set_charset("ISO-2022-JP")
>>> message._charset
iso-2022-jp
>>> test_print(message)
([('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?='), ('Content-Type', 'text/plain; charset="iso-2022-jp"')], '=C3=A3=C2=83=C2=86=C3=A3=C2=82=C2=B9=C3=A3=C2=83=C2=88 Here is the message.')

>>> email.encoding
>>> email.encoding = "ISO-2022-JP"
>>> email.encoding
'ISO-2022-JP'
>>> test_print(email)
([('Content-Type', 'text/plain; charset="iso-2022-jp"'), ('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?=')], '\\xc3\\xa3\\xc2\\x83\\xc2\\x86\\xc3\\xa3\\xc2\\x82\\xc2\\xb9\\xc3\\xa3\\xc2\\x83\\xc2\\x88 Here is the message.')

>>> email.encoding = "Shift-JIS"
>>> email.encoding
'Shift-JIS'
>>> test_print(email)
([('Content-Type', 'text/plain; charset="shift-jis"'), ('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?=')], 'w6PCg8KGw6PCgsK5w6PCg8KIIEhlcmUgaXMgdGhlIG1lc3NhZ2Uu\\n')

>>> message = email.message()
>>> message._charset
shift-jis
>>> message.set_charset("Shift-JIS")
>>> message._charset
shift-jis
>>> test_print(message)
([('Content-Type', 'text/plain; charset="shift-jis"'), ('Subject', '=?utf-8?b?w6PCg8KGw6PCgsK5w6PCg8KIIFN1YmplY3QgaGVyZQ==?=')], 'w6PCg8KGw6PCgsK5w6PCg8KIIEhlcmUgaXMgdGhlIG1lc3NhZ2Uu\\n')

"""

from django.test import TestCase
from django.core import mail


class MailTest(TestCase):
    subject = u"スパム Subject"
    body = u"スパム Body."
    email = mail.EmailMessage(subject, body)

    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            charset='iso-2022-jp')
        self.assertEqual(len(mail.outbox), 2)

    def test_default(self):
        message = self.email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="utf-8"')
        self.assertEqual(get_subject(message), '=?utf-8?b?44K544OR44OgIFN1YmplY3Q=?=')
        self.assertEqual(message._payload, '=E3=82=B9=E3=83=91=E3=83=A0 Body.')

    def test_iso_2022_jp(self):
        email = mail.EmailMessage(self.subject, self.body, charset='iso-2022-jp')
        self.assertEqual(email.encoding, 'iso-2022-jp')
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="iso-2022-jp"')
        self.assertEqual(get_subject(message),
            '=?iso-2022-jp?b?GyRCJTklUSVgGyhCIFN1YmplY3Q=?=')
        self.assertEqual(message._payload, '\x1b$B%9%Q%`\x1b(B Body.')

    def test_shift_jis(self):
        email = mail.EmailMessage(self.subject, self.body, charset='shift_jis')
        self.assertEqual(email.encoding, 'shift_jis')
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="shift_jis"')
        self.assertEqual(get_subject(message),
            '=?shift_jis?q?=83X=83p=83=80_Subject?=')
        self.assertEqual(message._payload, 'g1iDcIOAIEJvZHku\n')

    def test_shift_jis_(self):
        email = mail.EmailMessage(self.subject, self.body, charset='shift-jis')
        self.assertEqual(email.encoding, 'shift-jis')
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="shift-jis"')
        self.assertEqual(get_subject(message),
            '=?shift-jis?b?g1iDcIOAIFN1YmplY3Q=?=')
        self.assertEqual(message._payload, 'g1iDcIOAIEJvZHku\n')

    def test_changing_encode(self):
        email = mail.EmailMessage(self.subject, self.body)
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="utf-8"')
        self.assertEqual(get_subject(message), '=?utf-8?b?44K544OR44OgIFN1YmplY3Q=?=')
        self.assertEqual(message._payload, '=E3=82=B9=E3=83=91=E3=83=A0 Body.')

        email.encoding = "iso-2022-jp"
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="iso-2022-jp"')
        self.assertEqual(get_subject(message),
            '=?iso-2022-jp?b?GyRCJTklUSVgGyhCIFN1YmplY3Q=?=')
        self.assertEqual(message._payload, '\x1b$B%9%Q%`\x1b(B Body.')

        email.encoding = "shift_jis"
        message = email.message()
        self.assertEqual(get_content_type(message), 'text/plain; charset="shift_jis"')
        self.assertEqual(get_subject(message),
            '=?shift_jis?q?=83X=83p=83=80_Subject?=')
        self.assertEqual(message._payload, 'g1iDcIOAIEJvZHku\n')

def test_print(message):
    if isinstance(message, mail.EmailMessage):
        message = message.message()
    elif not isinstance(message, mail.SafeMIMEText):
        raise "test_print()"
    return [(header[0], str(header[1])) for header in message._headers
        if header[0] == "Content-Type" or header[0] == "Subject"], message._payload

get_header = lambda x, y: [str(header[1]) for header in x._headers
    if header[0] == y][0]
get_content_type = lambda x: get_header(x, "Content-Type")
get_subject = lambda x: get_header(x, "Subject")
