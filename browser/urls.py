from django.conf.urls import url
from browser.views import IndexView, BlockView, TxView, AddressView, SerchView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    #url(r'^block/(?P<bhash>[a-zA-Z0-9]{40})', BlockView.as_view(), name="block"),
    url(r'^block/(?P<bhash>.*)', BlockView.as_view(), name="block"),
    #url(r'^tx/(?P<txid>[A-Za-z0-9]{64})', TxView.as_view(), name="tx"),
    url(r'^tx/(?P<txid>.*)', TxView.as_view(), name="tx"),
    #url(r'^address/(?P<address>T\w{33})', AddressView.as_view(), name="address"),
    url(r'^address/(?P<address>.*)', AddressView.as_view(), name="address"),
    url(r'^search/$', SerchView.as_view(), name="search"),
]
