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
    f_write = open('page_stats_output.txt', 'w')
    f_write.write(str(page_counts) + '\n')

def access_pages(id_lst, url_prefix, access_token):
    param_page = {"access_token": access_token, "fields": "name,id,phone,emails,events,posts{story,message,created_time,shares,type,status_type}"}
    for pageid in id_lst:
        tmp_page_info = {'page_title':'','percnt_text':0,'percnt_video':0,'percnt_photo':0,'percnt_link':0,'percnt_offer':0,}
        tmp_type_counts = {"link": 0, "status": 0, "photo": 0, "video":0, "offer": 0}
        tmp_status_type_counts = {""}
        r = requests.get(url_prefix+pageid, params=param_page)
        r_json = r.json()
        page_json = r_json
        tmp_page_info['page_title'] = str(r_json.get('name'))
        tmp_posts_counts = 0
        while r_json.get('posts').get('paging').get('next')
            posts = page_json.get('posts').get('data')
            for post in posts:
                post_id = post.get('id')
                tmp_posts_counts = tmp_page_counts +1 
                tmp_type = access_posts(post_id, url_prefix, access_token)
                tmp_type_counts[str(tmp_type)] = tmp_type_counts[str(tmp_type)] + 1
            nextpageurl = r_json.get('posts').get('paging').get('next')
            nextpage = requests.get(nextpageurl)
            page_json = nextpage.json()
        write_page_stats(tmp_type_counts)

def access_posts(post_id, url_prefix, access_token):
    param_post = {"access_token": access_token, "fields": "type"}
    r = requests.get(url_prefix+post_id, params=param_post)
    r_json = r.json()
    post_type = r_json.get('type')
    return post_type

if __name__ == '__main__':
    access_token = 'CAACEdEose0cBALadwwp0TkpnP4bhSJomJCHbtPqEJxnORXXZCuSL5h3hFoftBsZBIJ388RkR3GHz82F9Q9wgNZAyHEM69nSmxESIQyAPAlsqVVpA2Y4uELuYxiYnZAKjWDWs7nN1VkzEFsomxIDhYksoGfK9GHF2zp8ugsc4CVKZACDoWDEjZAgGkUnc9Ax1RZBpwofYyvHGAT3RvUnyTZA6'
    f_read = open('page_ids.txt', 'r')
    id_lst = read_page_ids(f_read)
    access_pages(id_lst, 'https://graph.facebook.com/v2.5/', access_token)
