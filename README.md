# HtmlParser （简历数据解析）
> 手动标记 提取简历数据

# 目录结构
```
    config                              // 配置目录
        template                            // 模板文件夹
            job51.html                          // 模板文件
        job51.json                          // 生成的规则
    test                                // 测试文件夹
        job51                               // 前程无忧的测试文件目录
        zhilian                             // 智联招聘的测试文件目录
        resumeData.json                     // 测试提取出的数据
    htmlParser.py                       // 解析主程序
    README.md                           // 文档
```

# 标记方式
* 1. 创建一个简单的服务 http.createServer()
* 2. 增加静态资源返回（html css img）
* 3. 增加json数据返回 引入Promise（get请求）
* 4. 引入stream处理post请求 Promise串接各个服务
* 5. 学习Buffer Promise重构流式中间件
* 6. 学习ejs 使用webpack2构建前端
* 7. 构建动态路由 & 学习markdown

# 使用方式
	=> 将标记后的模板html以渠道名的方式命名并放入 './config/template'下
	=> 在'./test'目录下新建以渠道名命名的目录，并放入测试文件
	=> 使用VScode打开 htmlParser.py，修改最下方的 testFilePath 和 htmlType
        例如新增猎聘渠道 liepin
        testFilePath = './test/liepin/test.html'
        htmlType = 'liepin'
    => 运行 htmlParser.py，根据需要编辑'./config/liepin.json'，添加正则或填写需去除的指定文字

 
