import re


def check_style(data):
    query_style = None
    if re.match(r'^[a-zA-Z0-9]{40,64}|T\w{33}|\d+$', data):
        try:
            is_height = int(data)
        except:
            is_height = None
        if  is_height or is_height == 0:
            query_style = "blockheight"
            return query_style
        else:
            if len(data) == 40:
                query_style = "blockhash"
            elif len(data) == 34:
                query_style = "address"
            else:
                query_style = "txhash"
            return query_style

if __name__ == "__main__":
    print(check_style("2"))
