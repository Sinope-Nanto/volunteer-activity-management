# 2021/11/29  
event app目前已经完成的接口：  
# Event创建  
url: /event/newevent/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {  
'title':'Act Movies with Janpanese Famous Actresses',  
'place' : 'Tokyo Ginza',  
'require_volunteers_number' : '114',  // 字符串形式的整数  
'description' : 'Go to Tokyo and act a movie',  
'start' : '2021-1-11', // '%Y-%M-%D'  
'end' : '2021-1-12'  
}  
返回数据：  
{"code":200,"msg":"","data":{"event_id":"100000"}}  
"event_id"为创建的EVENT的id  
当权限不足时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
# Program创建  
url: /event/newprogram/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {  
'event_id' : '100000',// program所属的enent的id  
'title':'Act Movies with Janpanese Famous Actresses',  
'start' : '2021-1-11', // '%Y-%M-%D'    
'end' : '2021-1-12'  
}  
返回数据：  
{"code":200,"msg":"","data":{"program_id":"090000"}}  
"program_id"为创建的program的id  
当权限不足时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
当enent_id不存在时，返回:  
{"code":404,"msg":"Event don't exist."}  
# 加入Event  
url: /event/join/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {  
'event_id' : '100000',// 加入的enent的id  
'duty' : 'leader' //任意字符串    
}  
返回数据：  
{"code":200,"msg":""}   
不是志愿者时，返回:  
{"code":401,"msg":"you are not volunteer.","data":{}}  
时间冲突/人员已满时，返回:  
{"code":403,"msg":"You can't join the event.","data":{}}  
# 退出Event  
url: /event/quit/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {  
'event_id' : '100000',// program所属的enent的id  
'user_id':'64162251'  
}  
token所有人只能为user_id本人或者管理员。  
返回数据：  
{"code":200,"msg":"","data":{}}  
当权限不足时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
当user_id没有加入event_id时，返回:  
{"code":403,"msg":"The user havn't joined the event."}  