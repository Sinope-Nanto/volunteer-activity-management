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
'start' : '2021-1-11', // '%Y-%m-%d %H:%M:%S'  
'end' : '2021-1-12',  
'program' : '090000' //event所属的program，不能为空    
}  
返回数据：  
{"code":200,"msg":"","data":{"event_id":"100000"}}  
"event_id"为创建的EVENT的id  
当权限不足时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
当program不存在时，返回：
{"code":404,"msg":"Program don't exist"}
# Program创建  
url: /event/newprogram/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {  
'title':'Act Movies with Janpanese Famous Actresses',  
}  
返回数据：  
{"code":200,"msg":"","data":{"program_id":"090000"}}  
"program_id"为创建的program的id  
当权限不足时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
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
# 结算志愿活动  
url: /event/finish/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}
data = {'event_id':'100000',  
'user_id' : '82705723',//结算的志愿者id  
'is_finish' : 'True' // True or False 是否完成任务  
}
token所有人只能为管理员。  
返回数据：  
{"code":200,"msg":"","data":{}}  
当权限不足时（不是管理员时），返回:  
{"code":401,"msg":"you don't enough permissions"}  
当user_id没有加入event_id时，返回:  
{"code":403,"msg":"The user havn't joined the event."}  
# 2021/11/30  
# 捐赠  
url: /event/donor/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}
data = {'id':'100000',//捐赠program或者event的id，当捐赠目标为本组织时，id为1.  
'amount' : '100.00',//捐赠金额，为字符串形式的float     
}
token所有人只能为Donor。  
返回数据：  
{"code":200,"msg":"","data":{"donor_amount":"100","time":"2021-11-30 16:02:17.778230","user_id":"12153262","donor_id":"090000"}}    
当权限不足时（不是捐赠员时），返回:  
{"code":401,"msg":"You are not Donor"}  
当活动不存在或者已经结束/被终止时，返回:  
{"code":403,"msg":"You can't donor the item."}  
# 2021/12/1  
# 信息查询  
url: /event/getinfo/
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}
data = {'id' : '100000'}  
当请求者是管理员，请求id为'1'时,返回组织收捐赠信息：  
{"code":200,"msg":"","data":{
    'amount_of_fund': 1000.00,   
    'info_donor': [{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100},{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100}]  
    }  
}  
当请求者不是管理员，请求id为Program时：
返回数据：  
{"code":200,"msg":"","data":{
    'title': 'ABCDEFG',   
    'status': '1',//活动状态，0代表进行中，1代表结束  
    'event' : [{'event_id' : '100000', 'title' : 'ABC'},{'event_id' : '100001', 'title' : 'ABCD'}]//program所属的event的id,title列表  
    }  
}  
当请求者是管理员，请求id为Program时：
返回数据：  
{"code":200,"msg":"","data":{
    'title': 'ABCDEFG',   
    'status': '1',//活动状态，0代表进行中，1代表结束  
    'event' : [{'event_id' : '100000', 'title' : 'ABC'},{'event_id' : '100001', 'title' : 'ABCD'}]//program所属的event的id,title列表  
    'amount_of_fund' : 100.00,
    'info_donor' : [{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100},{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100}]
    }
} 
当请求者不是管理员，请求id为Event时：
返回数据：  
{"code":200,"msg":"","data":{
    'title': 'ABCDEFG',   
    'status': '1',//活动状态，0代表进行中，1代表结束  
    'require_volunteers_number' = 100  
    'now_volunteers_number' = 1  
    'place' = 'Tokyo',  
    'start' = '2021-11-01 21:00:00',  
    'end' = '2021-11-02 21:00:00',  
    'description' = 'AWJFHHFUOWEHOUIF',  
    'program' = '090000'//Event所属的Program  
    }  
}  
当请求者是管理员，请求id为Event时：
返回数据：  
{"code":200,"msg":"","data":{
    'title': 'ABCDEFG',   
    'status': '1',//活动状态，0代表进行中，1代表结束  
    'require_volunteers_number' = 100  
    'now_volunteers_number' = 1  
    'place' = 'Tokyo',  
    'start' = '2021-11-01 21:00:00',  
    'end' = '2021-11-02 21:00:00',  
    'description' = 'AWJFHHFUOWEHOUIF',  
    'program' = '090000'//Event所属的Program  
    'amount_of_fund' : 100.00,
    'info_donor' : [{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100},{'donor_id': '123456', 'donor_time': '2021-11-01 21:00:00.55', 'amount': 100}],  
    'info_volunteer' : [{'user_id': '123456789', time_start: '2021-11-01 21:00:00.55', time_end: '2021-11-01 21:00:00.55', 'duty': 'leader', 'status': 1}]  
    //其中0代表进行中，1代表已完成，2代表已退出  
    }  
}  
# 目标搜索  
url: /event/search/  
方法：post  
请求格式：  
//下列字段均可为空或无  
data = {'place':'Tokyo',  
'program' : '090000',//event所属program的id  
'title' : 'ABCDEFG',  
'status' : '0'//活动状态，0代表进行中，1代表结束  
}
返回数据：  
{
    "code":200,"msg":"","data":{
    'result_list' : [{'id':'100000', 'type':'event', 'title':'ABCDER'}] 
    }
}   
# 活动状态更改  
url: /event/status/  
方法：post  
请求格式：  
headers = {"token":"393e510803d94fa2a6606d0f7be0fba5"}  
data = {'id':'100000',  
'status' : '0'//活动状态，0代表进行中，1代表结束,2代表终止/删除  
}
返回数据：  
{"code":200,"msg":""}   

