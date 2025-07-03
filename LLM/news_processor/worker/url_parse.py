from urllib.parse import urlparse,parse_qs ,urlencode,urlunparse

#url to parse

url = "https://www.geeksforgeeks.org/python/python-pillow-a-fork-of-pil/"

parsed = urlparse(url)

print(parsed)

#output :
#ParseResult(scheme='https', netloc='www.geeksforgeeks.org',
#  path='/python/python-pillow-a-fork-of-pil/', params='', query='', fragment='')

query_dict = parse_qs(parsed.query)
query_dict['q']=['python tutorial']
query_dict['page'] =['2']

new_query = urlencode(query_dict,doseq=True)
#rebuilding new url
new_url = urlunparse((
    parsed.scheme,
    parsed.netloc,
    parsed.path,
    parsed.params,
    new_query,
    parsed.fragment   
))

print("New Url :",new_url)
print("Parsing new url:",urlparse(new_url))

#out put :
#New Url : https://www.geeksforgeeks.org/python/python-pillow-a-fork-of-pil/?q=python+tutorial&page=2
#Parsing new url: ParseResult(scheme='https',
#  netloc='www.geeksforgeeks.org',
#  path='/python/python-pillow-a-fork-of-pil/',
#  params='', query='q=python+tutorial&page=2', fragment='')
