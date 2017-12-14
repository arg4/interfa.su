from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # add urls for pagination
    url(r'^(?P<page_id>\d+)/$', views.index, name='index'),
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article, name='article'),
    # add urls for filter modes
    url(r'^(?P<filter_mode>p|c|n|o)/$', views.index, name='index'),
    url(r'^(?P<page_id>\d+)/(?P<filter_mode>p|c|n|o)/$', views.index, name='index'),
    # add url for site information board
    url(r'^site_information/$', views.about_contact, name='information'),
    # add urls for mod panel AND comment moderation panel
    url(r'^site_infrastructure/', include([
        #Redirects to a page will all flagged comments mods will have the option to delete or reset the flagged count to zero.
        url(r'^mod/$', views.content_moderation, name='content_moderation'),
        #This view will also show all of the authors created articles.
        url(r'^staging/$', views.article_staging_all, name='staging_all'),
        # This is an in-depth view into an individual article.
        url(r'^staging/(?P<staged_article>[0-9]+)/$', views.article_staging_individual, name='staging_indv'),
    ])),
    # add urls for article creation AND article editing
    url(r'^author_panel/', include([
        url(r'^new_draft/$', views.new_draft, name='new_draft'),
        url(r'^new_draft/(?P<filter_m>l|e|t)/$', views.new_draft, name='new_draft'),
        url(r'^edit_draft/(?P<draft_id>[0-9]+)/$', views.edit_draft, name='edit_draft'),
        url(r'^edit_article/(?P<article_id>[0-9]+)/$', views.edit_article, name='edit_article'),
    ])),
]
