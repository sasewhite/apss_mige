YAML格式用例的约定
1、必须要包含一级关键字：name，request，validata   （这三个关键字必须有！）
2、在request关键字下必须包含：method，url，data  如果data没有的话，那么输入默认值{}
3、提取变量使用一级关键字extract，支持json提取和正则提取,使用{{}}的方式取值-（使用双大括号的方式取值）
4、可以使用热加载的方式调用debugtalk.py中的方法（DebugTalk是个类！），通过${}的方式进行调用 ---${function_name}
5、支持equals、contains两种断言
6、使用parameters做数据驱动，通过$csv{appid}这种方式取值
