# Hotel-Air-Conditioning-Dispatching-System

北京邮电大学软件工程期末，酒店空调管理系统后端，利用 Python Flask 框架以及反馈优先级调度

由于我负责的是后端，因此这里没有贴出前端代码，如果需要参考可以访问我们团队项目的[主页面](https://github.com/Shayne-Ryu/Software-Engineering)

## 接口简介

> 请注意，目前以下所有接口参数都为 **_get_** 请求参数

### LoginController

> **控制器 url：** `/`

---

`/`

**_返回：_**

返回主页/登录页面 Html 模板

---

`/login`

**_参数：_**

**role:** _整数_，指示登录的角色：0 为客户，1 为管理员，2 为前台服务员，3 为经理

**name:** _可选_，_字符串_，客户以外的角色可以指定姓名，以便重复登录

**password:** _可选_，_字符串_，客户以外的角色可以指定密码，以便重复登录

**_返回：_**

json 格式数据，message 域指示返回信息，redirect 域指示前端下一步跳转的 url。请注意，登录操作后 redirect 域参数将会包含该角色唯一的 id，前端必须对其进行记录

### UserController

> **控制器 url：** `/user`

---

`/`

**_返回：_**

返回页面 Html 模板

---

`/roomInfo`

**_参数：_**

**user_id:** _字符串_，客户通过登录操作得到的 id

**_返回：_**

json 格式数据，message 域返回房间信息的多层 json，redirect 域指示前端下一步跳转的 url 并传递 id

---

`/request`

**_参数：_**

**user_id:** _字符串_，客户通过登录操作得到的 id

**temp:** _可选_，_整数_，目标温度，必须在温度范围内

**wind:** _可选_，_整数_，目标风速，必须在风速范围（0-3）内

**mode:** _可选_，_整数_，控温模式，必须为 0（制冷）或 1（制热）

**_返回：_**

json 格式数据，message 域返回请求已收到消息，redirect 域指示前端下一步跳转的 url 并传递 id

---

`/checkOut`

**_参数：_**

**user_id:** _字符串_，客户通过登录操作得到的 id

**_返回：_**

json 格式数据，message 域返回结账成功消息，redirect 域指示前端下一步跳转的 url 并传递 id

### AdministratorController

> **控制器 url：** `/admin`

---

`/`

**_返回：_**

返回页面 Html 模板

---

`/initServer`

**_参数：_**

**admin_id:** _字符串_，管理员通过登录操作得到的 id

**AirCondition_num:** _可选_，_整数_，空调/房间数量，即 ppt 中的对象数量，默认值 3

**default_temp:** _可选_，_整数_，默认温度，必须在温度范围内，默认值 26

**default_mode:** _可选_，_整数_，控温模式，必须为 0（制冷）或 1（制热），默认为制冷

**default_highest_temp:** _可选_，_整数_，最高温度，默认为 31

**default_lowest_temp:** _可选_，_整数_，最低温度，默认为 18

**default_wind_level:** _可选_，_整数_，默认风速，必须在风速范围（0-3），默认值 0，即无风

**time_slot:** _可选_，_整数_，时间片，用于时间片调度，单位为秒，默认值为 2

**scheduling_algorithm:** _可选_，_整数_，调度算法,必须为 0（优先级）或 1（时间片），默认为优先级

**tariff:** _可选_，_浮点数_，费率，必须为 0-1 之间的小数，默认值为 1.0

**_返回：_**

json 格式数据，message 域返回初始化成功消息，redirect 域指示前端下一步跳转的 url 并传递 id

---

`/allRoomInfo`

**_参数：_**

**admin_id:** _字符串_，管理员通过登录操作得到的 id

**_返回：_**

json 格式数据，message 域返回房间监控信息的多层 json，redirect 域指示前端下一步跳转的 url 并传递 id

### WaiterController

> **控制器 url：** `/waiter`

---

`/`

**_返回：_**

返回页面 Html 模板

---

`/specification`

**_参数：_**

**user_id:** _字符串_，客户向前台提供的 id

**waiter_id:** _字符串_，前台通过登录获得的 id

**_返回：_**

json 格式数据，message 域返回详单的多层 json，redirect 域指示前端下一步跳转的 url 并传递 waiter 的 id

---

`/checkOut`

**_参数：_**

**user_id:** _字符串_，客户向前台提供的 id
**waiter_id:** _字符串_，前台通过登录获得的 id

**_返回：_**

json 格式数据，message 域返回结账成功消息，redirect 域指示前端下一步跳转的 url 并传递 id

---

`/specFile`

> **注意！** 不建议使用该接口

**_参数：_**

**user_id:** _字符串_，客户向前台提供的 id

**waiter_id:** _字符串_，前台通过登录获得的 id

**_返回：_**

直接返回详单的 csv 文件

### ManagerController

> **控制器 url：** `/manager`

---

`/`

**_返回：_**

返回页面 Html 模板

---

`/dailySheet`

**_参数：_**

**manager_id:** _字符串_，经理通过登录获得的 id

**_返回：_**

json 格式数据，message 域返回日报表的多层 json，redirect 域指示前端下一步跳转的 url 并传递 id
