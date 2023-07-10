string = b'POST /update HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\nContent-Length: 18\r\nsec-ch-ua: "Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"\r\nAccept: */*\r\nContent-Type: application/x-www-form-urlencoded; charset=UTF-8\r\nX-Requested-With: XMLHttpRequest\r\nsec-ch-ua-mobile: ?0\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\r\nsec-ch-ua-platform: "macOS"\r\nOrigin: http://127.0.0.1:5000\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: cors\r\nSec-Fetch-Dest: empty\r\nReferer: http://127.0.0.1:5000/\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7\r\nCookie: ajs_anonymous_id=70b54b3b-973a-47cc-a34a-0eb4e83f2984\r\n\r\nvalue=3&value2=asd'

def parse_query_string(query_string):
    data = {}
    pairs = query_string.decode().split()[-1].split('&')
    for pair in pairs:
        key, value = pair.split('=')
        data[key] = value
    return data

parsed_data = parse_query_string(string)
print(parsed_data)

value = parsed_data.get('value', '')
value2 = parsed_data.get('value2', '')

print('Value:', value)
print('Value2:', value2)


