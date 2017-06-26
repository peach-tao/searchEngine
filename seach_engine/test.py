# coding:utf-8

# s=u'ABSDSD'
# print s.lower()
# print u'\u5b89\u5f92\u751f\u7ae5\u8bdd:\u6b22\u4e50\u5bb6\u5ead'
#
# print u'\u7b2c\u4e09\u6839'
# print u'\u706b\u67f4'
# print u'\u5b89\u5f92\u751f\u7ae5\u8bdd:\u5356\u706b\u67f4\u7684\u5c0f\u5973\u5b69-The\xa0Little\xa0Match-Girl\xa03'
# print u'\u5b89\u5f92\u751f\u7ae5\u8bdd:\u5356\u706b\u67f4\u7684\u5c0f\u5973\u5b69-The\xa0Little\xa0Match-Girl\xa04'
# su =  u'\u5b89\u5f92\u751f\u7ae5\u8bdd:\u5356\u706b\u67f4\u7684\u5c0f\u5973\u5b69-The\xa0Little\xa0Match-Girl\xa04'
# print su.encode("utf-8").decode("utf-8")
# def findSubStr(substr, str, i):
#     count = 0
#     while i > 0:
#         index = str.find(substr)
#         if index == -1:
#             return -1
#         else:
#             str = str[index+1:]   #第一次出现的位置截止后的字符串
#             print str
#             i -= 1
#             count = count + index + 1   #字符串位置数累加
#     return count - 1
#
#
#
#
#
# lalerhu = "i love a good good girl"
# print lalerhu.index('good')
# print lalerhu.index('good',10)
# print findSubStr('good',lalerhu,2)

a = {'a':{'val':3}, 'b':{'val':4}, 'c':{'val':1}, 'd':{'val2':0}}
dict= dict(sorted(a.iteritems(), key=lambda d:d[1].get('val',0), reverse = True))
print type(dict)
print dict