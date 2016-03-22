import requests

def read_page_ids(ids_file):
    id_lst = []
    for line in ids_file.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        id_lst.append(line)
    return id_lst

def write_page_stats(page_info,post_info):
    f_write = open('page_stats_output.txt', 'a')
    f_write.write(str(page_info) + str(post_info)+ '\n')

def access_pages(id_lst, url_prefix, access_token):
    param_page = {"access_token": access_token, "fields": "name,id,phone,emails,likes,events,posts{type}"}
    print('make page param')
    for page_id in id_lst:
        tmp_page_info = {'page_title':'','percnt_text':0,'percnt_video':0,'percnt_photo':0,'percnt_link':0,'percnt_other':0,'phone':'','emails':'','likes':'','online':0}
        tmp_post_info = {'averlikes':0,'avercomts':0,'avershares':0,'percorig':0,'percrepost':0,'responseto':0}
        tmp_type_counts = {"link": 0, "status": 0, "photo": 0, "video":0, "offer": 0}
        tmp_postattri_info = {'tmp_sharescount_list':[],'tmp_likecount_list':[],'tmp_comentcount_list':[],'tmptype':'','repostcount':0}
        tmp_posts_counts = 0
        r = requests.get(url_prefix+page_id, params=param_page)
        r_json= r.json()
        print('jsonlize web page')#, r_json)
        page_json = r_json.get('posts')
        print('duplicate r_json')#, page_json)
        tmp_page_info['page_title'] = str(r_json.get('name'))
        if not r_json.get('phone')==None:
            tmp_page_info['phone'] = 1
        else:
            tmp_page_info['phone'] = 0
        if not r_json.get('emails')==None:
            tmp_page_info['emails'] = 1
        else:
            tmp_page_info['emails'] = 0
        tmp_page_info['likes'] = str(r_json.get('likes'))
        tmp_page_info['online'] = str(r_json.get('events'))
        while (page_json.get('paging')== None) == False:
            posts = page_json.get('data')
            print('get posts data')#,posts)
            for post in posts:
                post_id = post.get('id')
                print('get post id', post_id)
                tmp_posts_counts = tmp_posts_counts +1
                print('caculate posts count',tmp_posts_counts)
                tmp_postattri_info_return = access_posts(post_id, url_prefix, access_token,tmp_postattri_info)
                tmp_type = tmp_postattri_info_return['tmptype']
                tmp_postattri_info['repostcount'] = tmp_postattri_info_return['repostcount'] + tmp_postattri_info['repostcount']
                print('tmp postattri info repost count', tmp_postattri_info['repostcount'])
                tmp_postattri_info['tmp_sharescount_list'] = tmp_postattri_info['tmp_sharescount_list'] + tmp_postattri_info_return['tmp_sharescount_list']
                print('tmp_postatrri_info shares count list', tmp_postattri_info['tmp_sharescount_list'])
                print('get post type', tmp_type)
                tmp_type_counts[str(tmp_type)] = tmp_type_counts[str(tmp_type)] + 1
                print('caculate post types', tmp_type_counts)
            nextpageurl = page_json.get('paging').get('next')
            print('get url of next page', nextpageurl)
            nextpage = requests.get(nextpageurl)
            print('get data of next page of posts', nextpage)
            page_json = nextpage.json()
            print('jsonlize next page', page_json)
        tmp_page_info['percnt_text'] = tmp_type_counts['status']/tmp_posts_counts
        tmp_page_info['percnt_video'] = tmp_type_counts['video']/tmp_posts_counts
        tmp_page_info['percnt_photo'] = tmp_type_counts['photo']/tmp_posts_counts
        tmp_page_info['percnt_link'] = tmp_type_counts['link']/tmp_posts_counts
        tmp_post_info['avershares'] = sum(tmp_postattri_info['tmp_sharescount_list'])/len(tmp_postattri_info['tmp_sharescount_list'])
        #tmp_post_info['averlikes'] = sum(tmp_postattri_info['tmp_sharescount_list'])/len(tmp_postattri_info['tmp_sharescount_list'])
        #tmp_post_info['avercomts'] = sum(tmp_postattri_info['tmp_sharescount_list'])/len(tmp_postattri_info['tmp_sharescount_list'])
        tmp_post_info['percorig'] = len(tmp_postattri_info['tmp_sharescount_list'])/tmp_posts_counts
        #tmp_post_info['percrepost'] = 1 - 
        tmp_post_info['responseto']
        write_page_stats(tmp_page_info,tmp_post_info)
        
def access_posts(post_id, url_prefix, access_token,tmp_postattri_info):
    param_post = {"access_token": access_token, "fields": "type,shares,likes,comments"}
    tmp_postattri_info = {'tmp_sharescount_list':[],'tmp_likecount_list':[],'tmp_comentcount_list':[],'tmptype':'','repostcount':0}
    print('make post params')
    r = requests.get(url_prefix+post_id, params=param_post)
    print('get posts')
    r_json = r.json()
    print('r_json')
    if r_json.get('shares') == None:
        tmp_postattri_info['repostcount'] = tmp_postattri_info['repostcount']+ 1
        print(tmp_postattri_info['repostcount'])
    else:
        tmp_shares_count = r_json.get('shares').get('count')
        print('tm shares count', tmp_shares_count)
        tmp_postattri_info['tmp_sharescount_list']=[0]
        tmp_postattri_info['tmp_sharescount_list'][0] = int(tmp_shares_count)
        print('tmp sharescount list', tmp_postattri_info['tmp_sharescount_list'][0])
    post_type = r_json.get('type')
    print(post_type)
    tmp_postattri_info['tmptype'] = post_type
    return tmp_postattri_info

if __name__ == '__main__':
    access_token = 'CAACEdEose0cBAOGrZBX1CZASduuLueRofPv4FoFgfUPUaDAvKDxWxTt2AOSehqDBxuSDOSyvhD15jNXvkmcMB1v1q3frjJiAPBeQWalu1oSvEifX6VPhTdK8sTO5BJoRliwBBytlZCl8pPboEWBIsjBSapond6BLUdKWl287rjmMEoWK3brIrKCZCu1krJI4dTNZCSL6up6DU1KZBZBuInQ'
    print("get access_token")
    f_read = open('page_ids.txt', 'r')
    print('open id list file')
    id_lst = read_page_ids(f_read)
    f_write = open('page_stats_output.txt', 'w')
    f_write.write('')
    testv = 1
    print('read id list')
    print('start access pages')
    access_pages(id_lst, 'https://graph.facebook.com/v2.5/', access_token)
