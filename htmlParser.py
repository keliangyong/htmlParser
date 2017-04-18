#!/usr/bin/python35
#-*- coding:utf-8 –*-


import os
import re
import json
import uuid
from bs4 import BeautifulSoup

class HtmlParser(object):
    def __init__(self, htmlStr, htmlType):
        self.configPath = './config/' + htmlType + '.json'
        self.templatePath = './config/template/' + htmlType + '.html'
        self.src = BeautifulSoup(htmlStr, 'html.parser')
        self.getConfig(htmlType)
    
    def main(self):
        resumeData = self.parseResume( self.src, self.config, {})
        with open('./test/resumeData.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(resumeData, ensure_ascii=False))
        return resumeData

    def parseResume(self, parentNode, configJson, resumeData): # 根据配置文件对来源文件进行解析
        for i in configJson:
            if 'path' in configJson[i]:
                resumeData[i] = {}
                for item in parentNode.select(configJson[i]['path']):
                    if re.search(configJson[i]['reg'], item.text):
                        resumeData[i]['value'] = item.text.replace(configJson[i]['replace'], "")
                        if 'breakpoint' in configJson[i]:
                            resumeData[i]['list'] = []
                            pathArr = configJson[i]['breakpoint']['path'].split(" ")
                            pathArr.insert(-1,'>')
                            path = " ".join(pathArr)
                            for j in item.select(path):
                                if re.search(configJson[i]['breakpoint']['reg'], j.text):
                                    resumeData[i]['list'].append(self.parseResume(j, configJson[i]['breakpoint'], {}))
                        else:
                            self.parseResume(item, configJson[i], resumeData[i])
        return resumeData

    def getConfig(self, htmlType): # 获取配置文件 没有则重新创建
        if os.path.isfile(self.configPath):
            with open(self.configPath, 'r', encoding='utf-8') as f:
                self.config = json.loads(f.read())
        elif os.path.isfile(self.templatePath):
            with open(self.templatePath, 'r', encoding='utf-8') as f:
                templateHtml = f.read()
            self.templateSoup = BeautifulSoup(templateHtml, 'html.parser')
            self.config = self.buildConfig(self.templateSoup, {})
            with open(self.configPath, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.config, ensure_ascii=False))
        else:
            raise BaseException("type.json or type.html not found")

    def buildConfig(self, node, obj): # 从模板中创建 配置规则
        for k,v in enumerate(node.children):
            if not v.name: 
                continue
            if v.children:
                if 'id' in v.attrs and re.search('edaice-', v.attrs['id']):
                    key = v.attrs['id'].split(":")[1][1:-2]
                    path = self.getPath(v)
                    # regReference = [ i.text[:30] for i in self.templateSoup.select(path)[:5]]
                    obj[key] = {
                        'path':path,
                        'value':v.text[:30],
                        'replace': "",
                        'reg':"",
                        # 'regReference':"" if len(regReference)==1 else regReference,
                    }
                    self.buildConfig(v, obj[key])
                else:
                    self.buildConfig(v, obj)
            else:
                if 'id' in v.attrs and re.search('edaice-', v.attrs['id']):
                    key = v.attrs['id'].split(":")[1][:-2]
                    obj[key] = v.text
        return obj
        
    def getPath(self, node): # 获取节点的路径
        path = node.name
        for i in node.parents:

            if (i.name == '[document]') or ('id' in i.attrs and re.search('edaice-', i.attrs['id'])):
                return path

            identifier = self.getIdentifier(i)
            path = identifier + " " + path

            if re.search('#', identifier):
                return path

        return path

    def getIdentifier(self, node): # 获取节点的标识符
        if 'id' in node.attrs and not re.search('edaice-', node.attrs['id']):
            return '#' + node.attrs['id']
        elif 'class' in node.attrs:
            return node.name + '.' + '.'.join([x for x in node.attrs['class'] if x])
        else:
            return node.name

if __name__ == '__main__':
    testFilePath = './test/job51/test3.html'
    htmlType = 'job51'
    with open(testFilePath, 'r', encoding='utf8') as f:
        html = f.read()
    data = HtmlParser(html, htmlType).main()
    pass