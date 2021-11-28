# 2021/11/28  
目前已经完成的接口：  
# 注册接口
url: /user/register/  
方法：post  
请求格式：  
{
    'first_name' : str,  
    'last_name'; : str,  
    'role' : str,  //其中'0'代表管理员，'1'代表捐赠者，'0'代表志愿者。  
    'password' : str  
}  
返回数据：  
{"code":200,"msg":"","data":{"id":"51923482","token":"3a93c15d92e94fa788e666f0134a2961"}}  
其中"id"为账号，"token"为token。  
当请求错误时，返回:  
{"code":400,"msg":"Bad request"}  
# 登录接口  
url: /user/login/  
方法：post  
请求格式：  
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
