import os
import urllib.request
import urllib.parse
import re
import threading
import pymysql

def get_html(url):
    request = urllib.request.Request(url)
    request.set_proxy('135.2.77.29:8895','http')
    page = urllib.request.urlopen(request)
    html = page.read()
    return html

def download_ppt(ppt_url, name):
	if os.path.exists(name):
		print("file exist")
	else:
		print("download ", ppt_url)
		ppt_data = get_html(ppt_url)
		output = open(name, 'wb+')
		output.write(ppt_data)
		output.close

class mythread(threading.Thread):
	def __init__(self, pages):
		self.pages = pages
		threading.Thread.__init__(self) 
		try:
			self.conn=pymysql.connect(host='localhost',user='root',passwd='',db='python_learn',port=3306, charset='utf8')
			self.cur = self.conn.cursor()
		except Exception as e:
			print(e)

	def download_page(self,pages):
		download_num = 0
		for index in pages:
			url = ''
			if index == 1:
				url = 'http://sc.chinaz.com/ppt/index.html'
			else:
				url = 'http://sc.chinaz.com/ppt/index_%d.html' % index
			
			html = get_html(url)
			mod_re = r'<p><a target="_blank" href="(.+?)"'
			mod_matchRe = re.compile(mod_re)
			html = html.decode('utf-8')
			matchResult = mod_matchRe.findall(html)
		
			for mod_page in matchResult:
				try:
					select_sql = "select * from ppt_sp where inPage = '%s'" % mod_page 
					out = self.cur.execute(select_sql)
					if not out:
						print("in page ", mod_page)
						page = get_html('http://sc.chinaz.com'+mod_page)
			
						ppt_re = "a href='(http://jsdx.+?)'"
						ppt_match = re.compile(ppt_re)
						page = page.decode('utf-8')
						ppt_result_list = ppt_match.findall(page)
						ppt_url = ppt_result_list[0]

						intr_re ='<.span><div class="smr">(.+)<p>'
						intr_match = re.compile(intr_re)
						intr_result_list = intr_match.findall(page)
						intr = 'none'
						if intr_result_list:
							intr = intr_result_list[0]
						print("get intr %s" % intr)
							
						if ppt_url:
							select_sql = "select * from ppt_sp where downloadUrl = '%s'" % ppt_url
							out = self.cur.execute(select_sql)
							if not out:
								tmp = ppt_url.split('/')
								name = tmp[-1]
								download_ppt(ppt_url,name)
	
								mod_page_tmp = mod_page.replace('/','#')
								ppt_url_tmp = ppt_url.replace('/','#')
								insert_sql = "INSERT INTO ppt_sp (inPage,downloadUrl,name,introduce) VALUES ('%s','%s','%s','%s'); " % (mod_page, ppt_url,name,intr)
								print(insert_sql)
								self.cur.execute(insert_sql)
								self.conn.commit()
							else:
								print("url exit")
						else:
							print("not match")
					else:
						print("page has been download")
				except Exception as e:
					print(e)

	def run(self):
		if self.cur:
			self.download_page(self.pages)


pages1 = range(1,3) 
pages2 = range(4,6)
pages3 = range(7,9)
mythread1 = mythread(pages1)
mythread2 = mythread(pages2)
mythread3 = mythread(pages3)
mythread1.start();
mythread2.start();
mythread3.start();

