# 2021/11/28  
user app目前已经完成的接口：  
# 注册  
url: /user/register/  
方法：post  
请求格式：  
data:  
{
    'first_name' : str,  
    'last_name'; : str,  
    'role' : str,  //其中'0'代表管理员，'1'代表捐赠者，'2'代表志愿者。  
    'password' : str  
}  
返回数据：  
{"code":200,"msg":"","data":{"id":"51923482","token":"3a93c15d92e94fa788e666f0134a2961"}}  
其中"id"为账号，"token"为token。  
当请求错误时，返回:  
{"code":400,"msg":"Bad request"}  
# 登录  
url: /user/login/  
方法：post  
请求格式：  
data:  
{ 
    'id' : str,   
    'password' : str  
}  
返回数据：  
{"code":200,"msg":"","data":{"token":"4ffb703506694c9f9042a66659d16bca"}}  
"token"为token。  
当账号或密码错误时，返回:  
{"code":401,"msg":"Incorrect username or password"}  
当账号被限制登陆时，返回：  
{"code":403,"msg":"Account status is abnormal"}  
# 更改账号权限  
url: /user/permission/  
方法：post  
请求格式：  
headers:  
{  
    "token" : str  
}  
data:  
{   
    'id' : str, //要更改的用户的id  
    'role' : str,//想要把用户变成的角色，其中'0'代表管理员，'1'代表捐赠者，'2'代表志愿者。  
}  
返回数据：  
{"code":200,"msg":"","data":{}}    
当请求用户不是管理员或者目标用户是管理员时，返回:  
{"code":401,"msg":"you don't enough permissions","data":{}}   
当目标用户不存在时，返回：  
{"code":404,"msg":"The target user does not exist","data":{}}  
# 更改账号状态   
url: /user/status/    
方法：post  
请求格式：  
headers:  
{  
    "token" : str  
}  
data:  
{   
    'id' : str, //要更改的用户的id  
    'status' : str,//想要把用户变成的状态，其中'0'代表正常，'1'代表冻结，'2'代表删除。  
}  
返回数据：  
{"code":200,"msg":"","data":{}}    
当请求用户不是管理员或者目标用户是管理员时，返回:  
{"code":401,"msg":"you don't enough permissions","data":{}}   
当目标用户不存在或被删除时，返回：  
{"code":404,"msg":"The target user does not exist","data":{}}  
# 更改密码  
url: /user/changepassword/    
方法：post  
请求格式：  
data:  
{   
    'id' : str, //用户id   
    'password' : str,//用户密码。    
    'new_password' : str//新密码
}  
返回数据：  
{"code":200,"msg":"","data":{}}    
当账号或密码错误时，返回:  
{"code":401,"msg":"Incorrect username or password"}  
当账号被限制登陆时，返回：  
{"code":403,"msg":"Account status is abnormal"}  
# 更改账号信息  
url: /user/changeinformation/  
方法：post
headers:  
{  
    "token" : str  
}  
data:  
{     
    'first_name' : str,    
    'last_name' : str    
}  
返回数据：  
{"code":200,"msg":"","data":{}}  
当token错误或过期时，返回:  
{"code":401,"msg":"please login again"}  
# 按条件查询用户  
url: /user/search/  
方法：post
headers:  
{  
    "token" : str  
}  
//data中的键值为搜索条件，请求中没有该键或者该键内容为空时代表无限制。  
data:  
{     
    'first_name' : str,   
    'last_name' : str,   
    'role' : str  
}  
返回数据：  
{"code":200,"msg":"","data":{"id_list":["70671574","64162251","51923482"]}} 
token不属于管理员时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
# 获取用户信息  
url: /user/getuser/  
方法：post
headers:  
{  
    "token" : str  
}  
data:  
{     
    'id' : str // 想要获取用户的id  
}  
返回数据：  
{"code":200,"msg":"","data":{"id":"70671574","first_name":"Sinope","last_name":"Nanto","role":"administrator","status":"0"}}  
token不属于管理员或者查询的id自身时，返回:  
{"code":401,"msg":"you don't enough permissions"}  
# 2021/11/30  
'id' : id,
'token' : token,
'role' : role_to_str(int(post_data['role'])),
'first_name' : post_data['first_name'],
'last_name' : post_data['last_name']
# 注册
url: /user/register/  
方法：post  
请求格式：  
data:  
{
    'first_name' : str,  
    'last_name'; : str,  
    'role' : str,  //其中'0'代表管理员，'1'代表捐赠者，'2'代表志愿者。  
    'password' : str  
}  
返回数据：  
{"code":200,"msg":"","data":{"id":"51923482","token":"3a93c15d92e94fa788e666f0134a2961","role":"donor","first_name":"Sara","last_name":"Hammer"}}  
其中"id"为账号，"token"为token。  
当请求错误时，返回:  
{"code":400,"msg":"Bad request"}  