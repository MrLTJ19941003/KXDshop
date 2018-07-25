import requests

def get_authorize_url():
    redirect_uri = "http://39.106.22.205:8000/index/"
    get_authorize_url = "https://api.weibo.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=2311962970,redirect_uri=redirect_uri)
    print(get_authorize_url)
#code=8348d3f384a6f8d3a31c4f8b16703b65

def get_access_token_url(code="5b2dae1c03cc877dde27a7e000c502f1"):
    get_access_token_url = "https://api.weibo.com/oauth2/access_token"

    resule = requests.post(get_access_token_url,data={
        'client_id':2311962970,
        'client_secret':'d44234d91c0e8b75c217672b0c037192',
        'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':"http://39.106.22.205:8000/index/"

    })
    print(resule)

# '{"access_token":"2.00IQEvbF1Ll9WCc985a3cf3c081usH","remind_in":"157679999","expires_in":157679999,"uid":"5140989664","isRealName":"true"}'

def get_userDetail(access_token='',uid=''):
    get_userDetail_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=access_token,uid=uid)
    print(get_userDetail_url)
    result = requests.get(get_userDetail_url)
    print(result)
# {"id":5140989664,"idstr":"5140989664","class":1,"screen_name":"MAX攻城狮","name":"MAX攻城狮","province":"43","city":"1","location":"湖南 长沙","description":"","url":"http://m.blog.csdn.net/blog/index?username=Mr_LIUTAOJUN","profile_image_url":"http://tvax1.sinaimg.cn/crop.0.0.1006.1006.50/005BV4g8ly8fdzaapbx3lj30ry0rymzw.jpg","cover_image_phone":"http://ww1.sinaimg.cn/crop.0.0.640.640.640/549d0121tw1egm1kjly3jj20hs0hsq4f.jpg","profile_url":"u/5140989664","domain":"","weihao":"","gender":"m","followers_count":51,"friends_count":152,"pagefriends_count":9,"statuses_count":29,"video_status_count":0,"favourites_count":2,"created_at":"Wed May 28 12:38:24 +0800 2014","following":false,"allow_all_act_msg":false,"geo_enabled":true,"verified":false,"verified_type":-1,"remark":"","insecurity":{"sexual_content":false},"status":{"created_at":"Thu Oct 26 13:50:04 +0800 2017","id":4167097820777787,"idstr":"4167097820777787","mid":"4167097820777787","can_edit":false,"text":"转发微博","source_allowclick":0,"source_type":1,"source":"<a href=\"http://app.weibo.com/t/feed/BuNZh\" rel=\"nofollow\">三星 Galaxy S7 Edge</a>","favorited":false,"truncated":false,"in_reply_to_status_id":"","in_reply_to_user_id":"","in_reply_to_screen_name":"","pic_urls":[],"geo":null,"is_paid":false,"mblog_vip_type":0,"annotations":[{"client_mblogid":"4dde09e1-19c8-4276-9545-48354c587cad"},{"mapi_request":true}],"reposts_count":0,"comments_count":0,"attitudes_count":0,"pending_approval_count":0,"isLongText":false,"multi_attitude":[{"type":4,"count":0},{"type":5,"count":0},{"type":3,"count":0},{"type":2,"count":0},{"type":1,"count":0}],"hide_flag":0,"mlevel":0,"visible":{"type":0,"list_id":0},"biz_feature":0,"hasActionTypeCard":0,"darwin_tags":[],"hot_weibo_tags":[],"text_tag_tips":[],"rid":"0","userType":0,"more_info_type":0,"positive_recom_flag":0,"content_auth":0,"gif_ids":"","is_show_bulletin":2,"comment_manage_info":{"comment_permission_type":-1,"approval_comment_type":0}},"ptype":0,"allow_all_comment":true,"avatar_large":"http://tvax1.sinaimg.cn/crop.0.0.1006.1006.180/005BV4g8ly8fdzaapbx3lj30ry0rymzw.jpg","avatar_hd":"http://tvax1.sinaimg.cn/crop.0.0.1006.1006.1024/005BV4g8ly8fdzaapbx3lj30ry0rymzw.jpg","verified_reason":"","verified_trade":"","verified_reason_url":"","verified_source":"","verified_source_url":"","follow_me":false,"like":false,"like_me":false,"online_status":0,"bi_followers_count":20,"lang":"zh-cn","star":0,"mbtype":0,"mbrank":0,"block_word":0,"block_app":0,"credit_score":80,"user_ability":33555456,"urank":8,"story_read_state":-1,"vclub_member":0}
if __name__=="__main__":
    #get_authorize_url()
    #get_access_token_url()
    get_userDetail('2.00IQEvbF1Ll9WCc985a3cf3c081usH','5140989664')

