# encoding: utf-8
__author__ = 'liutj'

import requests,json

class YunPian(object):

    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_smsUrl = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_Sms(self,code,mobile):
        params = {
            'apikey':self.api_key,
            'text':'【融鑫源】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code),
            'mobile':mobile
        }
        response = requests.post(self.single_send_smsUrl,params)
        result_sms = json.loads(response.text)
        print(result_sms)
        return result_sms

if __name__ == "__main__":
    yunpian = YunPian('2bf59c6509a610f7901ca932df9205fb')
    yunpian.send_Sms('6666',15101030127)