Default contact.csv

N,FN,TEL;TYPE=CELL,TEL;TYPE=HOME,TEL;TYPE=WORK,EMAIL;TYPE=HOME,EMAIL;TYPE=WORK,ADR;TYPE=HOME;CHARSET=UTF-8,ADR;TYPE=WORK;CHARSET=UTF-8,ORG;CHARSET=UTF-8,NOTE;CHARSET=UTF-8,URL
张朝臣,张朝臣,15872583695,1234,1234,sample@yahoo.com,sample@yahoo.com,肥西县桃花路,肥西县桃,合肥限公司,备注,www.baidu.com
张朝臣1,张朝臣1,15872583691,1234,,sample@yahoo.com,sample@yahoo.com,tghrthrt,,dd备科技有限公司,ddd,www.22.com
张朝臣2,张朝臣2,15872583692,,,sample@yahoo.com,,,gggggff,ddd333技有限公司,ddd,www.330.cn



ADR字段不区分['street', 'city', 'state', 'pcode', 'country']，第三方导出地址一般未详细区分，区分的话需要对地址列修改。
python .\mc2v3.py --csv ctn.csv
