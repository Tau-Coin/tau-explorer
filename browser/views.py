from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from utils.tauchain import Tx
from utils.check_paramter import check_style
from django.http import HttpResponse, JsonResponse
import re

class IndexView(View):
    def get(self,request):
        tx = Tx()
        datas = tx.lastest_txs_100()
        context = {"datas": datas}
        return render(request, 'index.html', context)


class BlockView(View):
    def get(self, request, bhash):
        if not bhash or not re.match(r'^[a-zA-Z0-9]{40}$', bhash):
            context = {
                "search": bhash
            }
            return render(request, "searchindex.html", context)
        tx = Tx()
        datas = tx.get_block(bhash)
        context = {
            "datas": datas,
            "blockhash":bhash,
            "blockdata": datas[0] 
        }
        return render(request, "block.html", context)


class TxView(View):
    def get(self, request, txid):
        if not txid or not re.match(r"^[A-Za-z0-9]{64}$", txid):
            context = {
                "search": txid
            }
            return render(request, "searchindex.html", context)
        tx = Tx()
        datas = tx.get_txid(txid)
        context = {
            "datas": datas,
            "txhash":txid
        }
        return render(request, "txid.html", context)


class AddressView(View):
    def get(self, request, address):
        if address.endswith("/"): 
            address = address.split("/")[0]
        if not address or not re.match(r"^T\w{33}$", address):
            context = {
                "search": address
            }
            return render(request, "searchindex.html", context)
        tx = Tx()
        datas = tx.get_address(address)
        context = {
            "datas": datas,
            "address":address
        }
        return render(request, "address.html", context)


class SerchView(View):
    def post(self, request):
        query_data = request.POST.get("searchkey")
        if not query_data:
            context = {
               "search": query_data
            }
            return render(request, "searchindex.html", context) 
        style = check_style(query_data)
        if not style:
            context = {
                "search": query_data
            }
            return render(request, "searchindex.html", context)
        tx = Tx()
        if style == "blockheight":
            datas = tx.get_height(query_data)
            if not datas:
                context = {
                    "search": query_data
                }
                return render(request, "searchblock.html", context)
            else:
                context = {
                    "datas": datas,
                    "blockhash":datas[0].get("blockhash"),
                    "blockdata":datas[0]
                }
                return render(request, "block.html", context)
        elif style == "blockhash":
            datas = tx.get_block(query_data)
            if not datas:
                context = {
                    "search": query_data
                }
                return render(request, "searchblock.html", context)
            else:
                context = {
                    "datas": datas,
                    "txhash":query_data,
                    "blockdata": datas[0]
                }
                return render(request, "block.html", context)
        elif style == "txhash":
            datas = tx.get_txid(query_data)
            if not datas:
                context = {
                    "search": query_data
                }
                return render(request, "searchtxid.html", context)
            else:
                context = {
                    "datas": datas,
                    "txhash": query_data
                }
                return render(request, "txid.html", context)
        else:
            datas = tx.get_address(query_data)
            if not datas:
                context = {
                    "search": query_data
                }
                return render(request, "searchaddress.html", context)
            else:
                context = {
                    "datas": datas,
                    "address": query_data
                }
                return render(request, "address.html", context)
