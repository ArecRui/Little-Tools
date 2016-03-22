import requests

def read_page_ids(ids_file):
    id_lst = []
    for line in ids_file.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        id_lst.append(line)
    return id_lst

def write_page_stats(page_counts):
    f_write = open('page_stats_output.txt', 'a')
    f_write.write(str(page_counts) + '\n')

def access_pages(id_lst, url_prefix, access_token):
    param_page = {"access_token": access_token, "fields": "name,id,phone,emails,events,posts"}
    print('make page param')
    for page_id in id_lst:
        tmp_page_info = {'page_title':'','percnt_text':0,'percnt_video':0,'percnt_photo':0,'percnt_link':0,'percnt_offer':0}
        tmp_type_counts = {"link": 0, "status": 0, "photo": 0, "video":0, "offer": 0}
        tmp_origpost_counts = 0
        tmp_posts_counts = 0
        r = requests.get(url_prefix+page_id, params=param_page)
        print('get web page using requests')#,r#)
        r_json = r.json()
        print('jsonlize web page')#, r_json#)
        page_json = r_json.get('posts')
        print('duplicate r_json')#, page_json#)
        tmp_page_info['page_title'] = str(r_json.get('name'))
        while (page_json.get('paging')== None) == False:
            posts = page_json.get('data')
            print('get posts data')#,posts)
            for post in posts:
                post_id = post.get('id')
                print('get post id', post_id)
                tmp_posts_counts = tmp_posts_counts +1
                print('caculate posts count',tmp_posts_counts)
                tmp_type = access_posts(post_id, url_prefix, access_token)
                print('get post type', tmp_type)
                tmp_type_counts[str(tmp_type)] = tmp_type_counts[str(tmp_type)] + 1
                print('caculate post types', tmp_type_counts)
            nextpageurl = page_json.get('paging').get('next')
            print('get url of next page', nextpageurl)
            nextpage = requests.get(nextpageurl)
            print('get data of next page of posts', nextpage)
            page_json = nextpage.json()
            print('jsonlize next page', page_json)
        write_page_stats(tmp_type_counts)

def access_posts(post_id, url_prefix, access_token):
    param_post = {"access_token": access_token, "fields": "story,message,created_time,shares,type,status_type"}
    r = requests.get(url_prefix+post_id, params=param_post)
    r_json = r.json()
    post_type = r_json.get('type')
    return post_type

if __name__ == '__main__':
    access_token = 'CAACEdEose0cBAJ55oxnrHss7kV2WoZCwHdd4U5mdc34blsLaZBqS2jc2sgxAZBMZBhdzt9yaMy8fMZCvBdKCVRM1vCQkrDQmEtDhDbIRbRq1AhsxSN16DEJyOPfYXqxsCl30ZC8ZAtaYOVY0idhIxhnXTZBLZAU6Ot53OFVHwI1dY042ImjpeuS3aOpQjyZCdnHFXqqPODNLK4ZA2UH3Tmn1XQM'
    print("get access_token")
    f_read = open('page_ids.txt', 'r')
    print('open id list file')
    id_lst = read_page_ids(f_read)
    print('read id list')
    print('start access pages')
    access_pages(id_lst, 'https://graph.facebook.com/v2.5/', access_token)
