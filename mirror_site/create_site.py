import urllib2
import cookielib
import re
import os


def set_opener():
	cookie = cookielib.CookieJar()
	cookie_process = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookie_process)
	urllib2.install_opener(opener)
	
	
def write_to_file(file_name, data):
	#print (file_name)
	file = open(file_name, "w")
	file.write(data)
	file.close()
	
def get_main_page(main_page_name):
	global page_list
	
	if (page_list.has_key(main_page_name)):
		return
	
	page_list[main_page_name] = 1
	#print (main_page_name)
	
	main_url = "http://second.cloud.360.cn:8360"
	header = {
		"Host":"second.cloud.360.cn",
		"Referer":"http://second.cloud.360.cn:8360/",
		"User-Agent":'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
		"Cookie":'__huid=10umCvLr20q2EskH4Mu9OHpi5Fp4HwGiCuWa6ATYG0Sww%3D; __guid=132730903.752251499930644100.1434419342561.162; PHPSESSID=vcs2pj761ra0rm1mba13h426e0; Q=u%3Dmunat_86315127%26n%3Dkvnbcvat_11%26le%3DrzuuozqsBQLmZGHkZwpyAQNkAwZhL29g%26m%3DZGt3WGWOWGWOWGWOWGWOWGWOZGD2%26qid%3D33550014%26im%3D1_t01f45b967f9fddae65%26src%3Dpcw_ops_cdn%26t%3D1; T=s%3Ddd8ca2b48b3340c782a8a5f4d8047e30%26t%3D1434423453%26lm%3D%26lf%3D4%26sk%3D4f8524b25fa89ecd51c4613a20031cb2%26mt%3D1434423453%26rc%3D%26v%3D2.0%26a%3D1; CNZZDATA1253476719=1323888761-1434420169-%7C1434420169; test_cookie_enable=null; __hsid=2921e81aa9f8315d; PHPSESSID=u1ag500sl4fr3ue9ovl2tdu4b0'
	}
	
	data = get_page_data(main_url + "/" + main_page_name, header, main_page_name)
	
	#get css
	exp = re.compile('<link href="([a-z0-9A-Z_\-\/.%]+)" ', flags = 0)
	list = exp.findall(data)
	for link_page in list:
		get_page_data(main_url + link_page, header, link_page)
		
	#get js
	exp = re.compile('<script src="([a-z0-9A-Z_\-\/.%]+)" ', flags = 0)
	list = exp.findall(data)
	for link_page in list:
		#print (main_url + link_page)
		get_page_data(main_url + link_page, header, link_page)
		
	#get png
	exp = re.compile('<img src="([a-z0-9A-Z_\-\/.%]+)"', flags = 0)
	list = exp.findall(data)
	for link_page in list:
		#print (main_url + link_page)
		get_page_data(main_url + link_page, header, link_page)
		
	#get next page
	exp = re.compile('<a href="/([a-z0-9A-Z_\-\/.%]+)"', flags = 0)
	list = exp.findall(data)
	for link_page in list:
		#print (main_url + "/" + link_page)
		get_main_page(link_page)
		
		
def get_page_data(url_get, header_get, file_name):
	global page_list
	
	if (page_list.has_key(url_get)):
		return
	
	page_list[url_get] = 1
	print (url_get)
	
	req = urllib2.Request(
		url = url_get,
		headers = header_get,
		data = "")
	data = urllib2.urlopen(req).read()
	page_name = make_path(file_name)
	write_to_file(page_name, data)
	return data
	
def make_path(link_path):
	#print (link_path)
	index = link_path.rfind("/", 0, len(link_path))
	if (index == -1 or index  == 0):
		return "./" + link_path[0:len(link_path)]
	path = link_path[1:index]
	#print path
	os.system("mkdir -p " + path)
	return "./" + link_path[1:len(link_path)]

page_list = {}

if __name__ == "__main__":
	get_main_page("site")