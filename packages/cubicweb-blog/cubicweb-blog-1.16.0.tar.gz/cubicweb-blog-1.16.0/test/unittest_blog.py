"""Blog unit tests"""

import unittest
from cubicweb.devtools.testlib import CubicWebTC, MAILBOX


class BlogTestsCubicWebTC(CubicWebTC):
    """test blog specific behaviours"""

    def test_notifications(self):
        with self.admin_access.client_cnx() as cnx:
            cubicweb_blog = cnx.create_entity('Blog', title=u'cubicweb',
                                              description=u"cubicweb c'est beau")
            blog_entry_1 = cnx.create_entity(
                'BlogEntry', title=u"hop", content=u"cubicweb hop")
            blog_entry_1.cw_set(entry_of=cubicweb_blog)
            blog_entry_2 = cnx.create_entity(
                'BlogEntry', title=u"yes", content=u"cubicweb yes")
            blog_entry_2.cw_set(entry_of=cubicweb_blog)
            self.assertEqual(len(MAILBOX), 0)
            cnx.commit()
            self.assertEqual(len(MAILBOX), 0)
            blog_entry_1.cw_adapt_to(
                'IWorkflowable').fire_transition('publish')
            cnx.commit()
            self.assertEqual(len(MAILBOX), 1)
            mail = MAILBOX[0]
            self.assertEqual(mail.subject, '[data] hop')
            blog_entry_2.cw_adapt_to(
                'IWorkflowable').fire_transition('publish')
            cnx.commit()
            self.assertEqual(len(MAILBOX), 2)
            mail = MAILBOX[1]
            self.assertEqual(mail.subject, '[data] yes')

    def test_rss(self):
        with self.admin_access.client_cnx() as cnx:
            cubicweb_blog = cnx.create_entity('Blog', title=u'cubicweb',
                                              description=u"cubicweb c'est beau")
            content = u"""
<style> toto </style> tutu <style class=macin> toto
</style>
tutu
tutu
<style></style>

<tag>tutu</tag>

"""
            blog_entry_1 = cnx.create_entity('BlogEntry', title=u"hop",
                                             content=content, content_format=u"text/html")
            blog_entry_1.cw_set(entry_of=cubicweb_blog)

            xml = blog_entry_1.view('rssitem')
            self.assertEqual(xml.count("toto"), 0)
            self.assertEqual(xml.count("tutu"), content.count("tutu"))

    def test_prevnext(self):
        with self.admin_access.client_cnx() as cnx:
            e1 = cnx.create_entity('BlogEntry', title=u'a', content=u'a')
            cnx.create_entity('CWGroup', name=u'NotTheNextOfe1')
            e3 = cnx.create_entity('BlogEntry', title=u'b', content=u'b')
            cnx.commit()
            a1 = e1.cw_adapt_to('IPrevNext')
            self.assertIsNone(a1.previous_entity())
            self.assertEqual(u'b', a1.next_entity().title)
            a3 = e3.cw_adapt_to('IPrevNext')
            self.assertEqual(u'a', a3.previous_entity().title)
            self.assertIsNone(a3.next_entity())


if __name__ == '__main__':
    unittest.main()
