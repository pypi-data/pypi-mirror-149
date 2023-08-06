"""entity classes for Blog entities

:organization: Logilab
:copyright: 2003-2010 LOGILAB S.A. (Paris, FRANCE)
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: Lesser General Public License version 2 or above - http://www.gnu.org/
"""
# __docformat__ = "restructuredtext en"

from logilab.common.date import todate

from rdflib import URIRef, Literal, Namespace

from cubicweb.entities import AnyEntity, fetch_config
from cubicweb.entities.adapters import (
    EntityRDFAdapter, CWUserRDFAdapter as _CWUserRDFAdapter,
)
from cubicweb.entity import EntityAdapter
from cubicweb.predicates import is_instance
from cubicweb.rdf import NAMESPACES

NAMESPACES["sioc"] = Namespace("http://rdfs.org/sioc/ns#")
NAMESPACES["sioct"] = Namespace("http://rdfs.org/sioc/types#")
NAMESPACES["dcterms"] = Namespace("http://purl.org/dc/terms/")

__docformat__ = "restructuredtext en"


class CWUserRDFAdapter(_CWUserRDFAdapter):
    def triples(self):
        yield from super().triples()
        SIOC = self._use_namespace("sioc")
        uri = URIRef(self.uri)
        blog_entries = self._cw.find("BlogEntry", created_by=self.entity)
        for entry in blog_entries.entities():
            yield (uri, SIOC.creator_of, URIRef(entry.cwuri))


class BlogRDFAdapter(EntityRDFAdapter):
    __regid__ = "rdf"
    __select__ = is_instance("Blog")

    def triples(self):
        SIOC = self._use_namespace("sioc")
        SIOCT = self._use_namespace("sioct")
        RDF = self._use_namespace("rdf")
        DCTERMS = self._use_namespace("dcterms")
        uri = URIRef(self.uri)
        yield (uri, RDF.type, SIOCT.Weblog)
        yield (uri, DCTERMS.title, Literal(self.entity.dc_title()))
        if self.entity.description:
            yield (uri, DCTERMS.description, Literal(self.entity.description))
        yield (uri, SIOC.num_items, Literal(len(self.entity.reverse_entry_of)))
        yield (uri, SIOC.feed, URIRef(self.entity.cw_adapt_to('IFeed').rss_feed_url()))

        if self.entity.creator:
            yield (uri, SIOC.has_creator, URIRef(self.entity.creator.cwuri))

        for blog_entry in self.entity.reverse_entry_of:
            yield (uri, SIOC.container_of, URIRef(blog_entry.cwuri))


class BlogEntryRDFAdapter(EntityRDFAdapter):
    __regid__ = "rdf"
    __select__ = is_instance("BlogEntry")

    def triples(self):
        SIOC = self._use_namespace("sioc")
        SIOCT = self._use_namespace("sioct")
        RDF = self._use_namespace("rdf")
        DCTERMS = self._use_namespace("dcterms")
        uri = URIRef(self.uri)
        yield (uri, RDF.type, SIOCT.BlogPost)
        yield (uri, DCTERMS.title, Literal(self.entity.dc_title()))
        yield (uri, DCTERMS.date, Literal(self.entity.creation_date))
        yield (uri, DCTERMS.modified, Literal(self.entity.modification_date))
        yield (uri, SIOC.content, Literal(self.entity.content))
        yield (uri, DCTERMS['format'], Literal(self.entity.content_format))
        if self.entity.entry_of:
            yield (uri, SIOC.container, URIRef(self.entity.entry_of[0].cwuri))
        if self.entity.creator:
            yield (uri, SIOC.has_owner, URIRef(self.entity.creator.cwuri))


class MicroBlogRDFAdapter(BlogRDFAdapter):
    __regid__ = "rdf"
    __select__ = is_instance("MicroBlog")

    def triples(self):
        yield from super().triples()
        SIOCT = self._use_namespace("sioct")
        RDF = self._use_namespace("rdf")
        uri = URIRef(self.uri)
        yield(uri, RDF.type, SIOCT.Microblog)


class MicroBlogEntryRDFAdapter(BlogEntryRDFAdapter):
    __regid__ = "rdf"
    __select__ = is_instance("MicroBlogEntry")

    def triples(self):
        yield from super().triples()
        SIOCT = self._use_namespace("sioct")
        RDF = self._use_namespace("rdf")
        uri = URIRef(self.uri)
        yield (uri, RDF.type, SIOCT.MicroblogPost)


###################################################

class BlogIFeedAdapter(EntityAdapter):
    __regid__ = 'IFeed'
    __select__ = is_instance('Blog', 'MicroBlog')

    def rss_feed_url(self):
        if getattr(self.entity, 'rss_url', None):
            return self.entity.rss_url
        rql = ('Any E ORDERBY D DESC '
               'WHERE E entry_of X, X eid %s, E creation_date D'
               )
        return self._cw.build_url(rql=rql % self.entity.eid, vid='rss',
                                  vtitle=self.entity.dc_title())


class BlogISiocContainerAdapter(EntityAdapter):
    __regid__ = 'ISIOCContainer'
    __select__ = is_instance('Blog')

    def isioc_type(self):
        return 'Weblog'

    def isioc_items(self):
        return self.entity.reverse_entry_of


class BlogEntry(AnyEntity):
    """customized class for BlogEntry entities"""
    __regid__ = 'BlogEntry'
    fetch_attrs, cw_fetch_order = fetch_config(
        ['creation_date', 'title'], order='DESC')

    def dc_title(self):
        return self.title

    def dc_description(self, format='text/plain'):
        return self.printable_value('content', format=format)

    def dc_date(self, date_format=None):
        dc_date = self.creation_date
        for tr_info in self.reverse_wf_info_for:
            if tr_info.new_state.name == 'published':
                dc_date = tr_info.creation_date
                break
        return self._cw.format_date(dc_date, date_format=date_format)


class BlogEntryICalendarableAdapter(EntityAdapter):
    __regid__ = 'ICalendarable'
    __select__ = is_instance('BlogEntry')

    @property
    def start(self):
        return self.entity.creation_date

    @property
    def stop(self):
        return self.entity.creation_date


class BlogEntryICalendarViewsAdapter(EntityAdapter):
    __regid__ = 'ICalendarViews'
    __select__ = is_instance('BlogEntry')

    def matching_dates(self, begin, end):
        """calendar views interface"""
        mydate = self.entity.creation_date
        if not mydate:
            return []
        mydate = todate(mydate)
        if begin < mydate < end:
            return [mydate]
        return []


class BlogEntryISiocItemAdapter(EntityAdapter):
    __regid__ = 'ISIOCItem'
    __select__ = is_instance('BlogEntry')

    def isioc_content(self):
        return self.entity.content

    def isioc_container(self):
        return self.entity.entry_of and self.entity.entry_of[0] or None

    def isioc_type(self):
        return 'BlogPost'

    def isioc_replies(self):
        # XXX link to comments
        return []

    def isioc_topics(self):
        # XXX link to tags, folders?
        return []


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (CWUserRDFAdapter, ))
    vreg.register_and_replace(CWUserRDFAdapter, _CWUserRDFAdapter)
