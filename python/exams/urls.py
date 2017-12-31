from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.exam, name='exam'),
    re_path(r'^aware/(?P<study_id>[0-9]+)$', views.aware, name='aware'),
    re_path(r'^forgot/(?P<study_id>[0-9]+)$', views.forgot, name='forgot'),
    re_path(r'^do_add_random/(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.do_add_random, name='do_add_random'),
    re_path(r'^do_next/(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.do_next, name='do_next'),
    re_path(r'^do_review/(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.do_review, name='do_review'),
    re_path(r'^list/(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.list_page, name='list'),
    re_path(r'^new_words/(?P<book_id>[0-9]+)/(?P<exam_type>[wm])$', views.new_words, name='new_words'),
    re_path(r'^search/(?P<book_id>[0-9]+)$', views.search_page, name='search'),
    re_path(r'^detail/(?P<word_id>[0-9]+)$', views.detail_page, name='detail'),
    re_path(r'^reset_meaning/(?P<study_id>[0-9]+)$', views.reset_meaning, name='reset_meaning'),
]
