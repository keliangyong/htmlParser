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
* 1. 节点标识符：
    id='{"edaice-obj": attrName}'       // 主对象节点 attrName是自定义属性名 => 如: 个人信息、工作经验、项目经验等（注意：必须包裹从对象节点）
    id='{"edaice-obj-item": attrName}' // 从对象节点 attrName是自定义属性名 => 如：'年龄'、'婚姻状况'等从属于'个人信息'节点；'在职时间'、'岗位'、'工作描述'等从属于'工作经验'
    id='{"edaice-obj":"breakpoint"}'    // 列表分割节点 固定使用"breakpoint"属性名 => 如： 工作经验有多个，此时需要标识从哪里作为分割点（注意：尽量放在与子节点不同的节点上） 
* 2. 节点标识例子：
```
    <table id='{"edaice-obj":"summary"}'>
        <tbody>
            <tr>
                <td>最近工作（3个月）</td>
                <tr id='{"edaice-obj-item":"jobtitle"}'>
                    <td>职　位：</td>
                    <td>算法工程师</td>
                </tr>
            </tr>
            <tr id='{"edaice-obj-item":"company"}'>
                <td>公　司：</td>
                <td>智久机器人科技有限公司</td>
            </tr>
        </tbody>
    </table>
    {
        "summary": {
            "value": "\n\n\n\n\n\n\n\n                      ",
            "reg": "最近工作",
            "path": "#divResume table.column tr td table.box2",
            "replace": ""

            "jobtitle": {
                "value": "\n职　位：\n算法工程师\n",
                "reg": "职　位",
                "path": "tr td table tr td.tb2 table tbody tr tr",
                "replace": "职　位："
            },
            "company": {
                "value": "\n公　司：\n智久机器人科技有限公司\n",
                "reg": "公　司",
                "path": "tr td table tr td.tb2 table tbody tr",
                "replace": "公　司："
            }
        }
    }
```
```
    <table id='{"edaice-obj":"projectexperience"}'>
        <tr>
            <td class="plate1">项目经验</td>
        </tr>
        <tr>
            <td>
                <table id='{"edaice-obj":"breakpoint"}'>
                    <tr>
                        <td id='{"edaice-obj-item":"time"}'>2016/9-2016/12</td>
                        <td><strong id='{"edaice-obj-item":"name"}'>AGV叉车无人驾驶</strong></td>
                    </tr>
                    <tr>
                        <td>
                            <table>
                                <tbody>
                                    <tr id='{"edaice-obj-item":"prodesc"}'>
                                        <td>项目描述：</td>
                                        <td>结合惯导器件实现AGV叉车室内导航，按规定路径进行工作。</td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    {
        "projectexperience": {
            "value": "\n\n项目经验\n\n\n\n\n\n\n\n\n2016/9-2016/12\n",
            "reg": "项目经验",
            "path": "#divInfo td table",
            "replace": ""

            "breakpoint": {
                "value": "\n\n2016/9-2016/12\nAGV叉车无人驾驶\n\n\n\n",
                "reg": "",
                "path": "tr td.tbb table tr td.p15 table",
                "replace": ""

                "name": {
                    "value": "AGV叉车无人驾驶",
                    "reg": "",
                    "path": "tr td.rtbox strong",
                    "replace": ""
                },
                "time": {
                    "value": "2016/9-2016/12",
                    "reg": "\\d{4}\/\\d{1}-",
                    "path": "tr td",
                    "replace": ""
                },
                "prodesc": {
                    "value": "\n项目描述：\n结合惯导器件实现AGV叉车室内导航，按规定路径",
                    "reg": "项目描述",
                    "path": "tr td.tb1 table tbody tr",
                    "replace": ""
                }
            }
        }
    }
```

# 使用方式(以下以新增猎聘渠道为例)
    => 将标记后的模板html以渠道名的方式命名（liepin.html）并放入 './config/template'下
    => 在'./test'目录下新建以渠道名命名的目录，并放入测试文件
    => 使用VScode打开 htmlParser.py，修改最下方的 testFilePath 和 htmlType
        例如新增猎聘渠道 liepin
        testFilePath = './test/liepin/test.html'
        htmlType = 'liepin'
    => 运行 htmlParser.py，根据需要编辑'./config/liepin.json'，添加正则或填写需去除的指定文字
        例如 岗位名称这个字段：
        ```
        "jobtitle": {
            "value": "\n职　位：\n算法工程师\n",                     //  这是匹配到的文本值
            "reg": "职　位",                                       //  这是正则，文本值包含'职　位'的节点才是正确的岗位名称节点
            "path": "tr td table tr td.tb2 table tbody tr tr",      //  这是节点路径
            "replace": "职　位："                                   //  这是去除指定的文字，此处去除 '职　位：'
        }
        ```
    => 运行 htmlParser.py，打开'./test/resumeData.json'，查看提取结果