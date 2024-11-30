import requests
import os 

host = "https://harkiratapi.classx.co.in"
authkey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc0MzEyIiwiZW1haWwiOiJraHVtYXBva2hhcmVsMjA3OEBnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MzI3MjgyMDZ9.ZjwXhMHVYdcO4DqaXcDCgIqavyD5uKcr7V_F55epXis"

headers = {
    "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Ijc0MzEyIiwiZW1haWwiOiJraHVtYXBva2hhcmVsMjA3OEBnbWFpbC5jb20iLCJ0aW1lc3RhbXAiOjE3MzI3MjgyMDZ9.ZjwXhMHVYdcO4DqaXcDCgIqavyD5uKcr7V_F55epXis", 
    "User-Id": "74312",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Auth-Key": "appxapi",
}


purchased_cousrse = []

def get_purchased_data():
    url = "https://harkiratapi.classx.co.in/get/coursenew_by_idv2?id=12"
    try:
        response = requests.get(url, headers=headers).json()
        return response
    except Exception as e:
        return None


def choose_course():
    c =0
    for i in purchased_cousrse:
        c = c+1
        print(f"{c} - {i['course_slug']} \n")
    position = int(input("enter the position \n"))
    return position


def download_file(token:str,videotitle):
    watermark=""
    url = f"https://player.akamai.net.in//secure-player?token={token}&watermark={watermark}"
    
    try:
        htmlfile = requests.get(url=url).text
        htmlfile = htmlfile.replace('src="/','src="https://player.akamai.net.in/')
        htmlfile = htmlfile.replace('href="/','href="https://player.akamai.net.in/')
        
        os.makedirs("./videosfile",exist_ok=True)
        
        # put unique number in each file
        with open(f"./videosfile/{videotitle}.html",'w') as file:
            file.write(htmlfile)
       
    except Exception as e:
        print(e)
        
# /get/fetchVideoDetailsById?course_id=12&video_id=2820&ytflag=0&folder_wise_course=1

def get_video_details(course_id:str,video_id:int):
    url = f'{host}//get/fetchVideoDetailsById?course_id={course_id}&video_id={video_id}&ytflag=0&folder_wise_course=1'
    try:
        return requests.get(url=url,headers=headers).json()
    except Exception as e:
        print(e)
    
# /get/folder_contentsv2?course_id=12&parent_id=2688
# it provides the video id   parent id
def get_folder_contents(course_id:int,parent_id:int):
   
    url = f'{host}//get/folder_contentsv2?course_id={course_id}&parent_id={parent_id}'
    try:
        return requests.get(url=url,headers=headers).json()
    except Exception as e:
        print(e)
        
def choose_folder_contents(course_data):
    c = 0
    for i in course_data['data']:
        c = c+1
        print(f'{c}--{i["Title"]}')
    position = int(input("enter the position to choose a content , enter position"))
    return position-1
    
    
    
    
def main():
    course_data = get_purchased_data()
    
    for i in course_data['data']:
        purchased_cousrse.append({"course_id":i['id'],"parent_id":i['parent_id'],"course_slug":i['course_slug']}) 
    # print(purchased_cousrse)
    position = choose_course()
    
    course_id = purchased_cousrse[position-1]['course_id']
    parent_id = purchased_cousrse[position-1]['parent_id']
    
    
    folder_contents = get_folder_contents(course_id,parent_id)
    folder_positon = choose_folder_contents(folder_contents)
    
    while 1:
        folder_id = folder_contents['data'][folder_positon]['id']
        folder_parent_id = folder_contents['data'][folder_positon]['parent_id']
        material_type = folder_contents['data'][folder_positon]['material_type']

        if (material_type!="VIDEO"):
            folder_contents = get_folder_contents(course_id,folder_id)
            folder_positon = choose_folder_contents(folder_contents)
        else:
            print("choosing a video")
            break
        
    video_id = folder_contents['data'][folder_positon]['id']
    video_title = folder_contents['data'][folder_positon]['Title']
    
    video_details = get_video_details(course_id,video_id)
    print(video_details['data']['video_player_token'])
    video_token = video_details['data']['video_player_token']
    
    download_file(video_token,video_title)
    
    
    
    
    
    
    
    
    

    
main()
   
    