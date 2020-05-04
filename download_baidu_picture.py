import requests
from urllib import parse
import uuid
import os
def download_img(img_url):
	#新建一个文件夹存储图片
	if not os.path.exists('img2'):
		os.mkdir('img2')
	img=requests.get(img_url,headers=headers,stream=True) #获取数据流
	if img: #判断img是否为空，有时候code200也不一定是有内容的
		with open('img2/{}.jpg'.format(uuid.uuid4()),'wb') as f:
			chunks=img.iter_content(chunk_size=128)
			#防止CPU压力过大
			for chunk in chunks:
				f.write(chunk)
	'''
	当下载大的文件的时候，建议使用strea模式．
	默认情况下是false，他会立即开始下载文件并存放到内存当中，倘若文件过大就会导致内存不足的情况．
	当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines
	遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。
	转载至：https://www.cnblogs.com/nul1/p/9172068.html
	'''
def get_json(search_word,number):
	
	url='https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&' \
	    'queryWord={0:}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0' \
	    '&hd=&latest=&copyright=&word={0:}&s=&se=&tab=&width=&height=&face=0&' \
	    'istype=2&qc=&nc=1&fr=&expermode=&force=&pn={1:}&rn=30&gsm=1e&1586245023192='.format(search_word,number)
	#对于url分析在Word和queryWord内的内容为转码内容可以用parse内的quote进行转码
	html=requests.get(url,headers=headers).json()['data']
	#获取json内容
	try:
		for img in html:
			img_url=img['middleURL']
			#获取图片地址传给下载器
			download_img(img_url)
	except:
		pass
if __name__ == '__main__':
	headers = {
		'Connection': 'keep-alive',
		'Cookie': 'BIDUPSID=48E2DA4C7FAEF38154147CE188547C90; PSTM=1585356178; BAIDUID=48E2DA4C7FAEF38115106A9F5FF76160:FG=1; H_PS_PSSID=30969_1467_31170_21110_31186_31217_30823_31163_31196; delPer=0; PSINO=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
		'Referer': 'https://image.baidu.com/'
	}
	search_word=parse.quote(input('请输入要下载的图片'))
	for number in range(30,300,30):
		get_json(search_word,number)
