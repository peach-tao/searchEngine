# coding:utf-8
import os
import jieba
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

_STOP_WORDS = frozenset([
    'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
    'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
    'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
    'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as',
    'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been',
    'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
    'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can',
    'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
    'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
    'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
    'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
    'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
    'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
    'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
    'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
    'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
    'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
    'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
    'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
    'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
    'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
    'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
    'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
    'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
    'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
    'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
    'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
    'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
    'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
    'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
    'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
    'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
    'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
    'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
    'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
    'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'the'])


# search the exact times occurance of the string

def findSubStr(substr, str, i):
    count = 0
    while i > 0:
        index = str.find(substr)
        if index == -1:
            return -1
        else:
            str = str[index+1:]   #第一次出现的位置截止后的字符串
            # print str
            i -= 1
            count = count + index + 1   #字符串位置数累加
    return count - 1



def word_split(text):
    word_list = []
    pattern = re.compile(u'[\u4e00-\u9fa5]+')

    jieba_list = list(jieba.cut(text))
    time = {}
    for i, c in enumerate(jieba_list):
        # time.setdefault(c,0)
        # if c in time:  # record appear time
        #     time[c] += 1
        if c in time:  # record appear time
            time[c] += 1
        else:
            time.setdefault(c, 0)

        if pattern.search(c):  # if Chinese
            lalaerhu = text.decode("utf-8")
            word_list.append((len(word_list), (findSubStr(c,lalaerhu, time[c]+1), c)))
            continue
        if c.isalnum():  # if English or number
            lalaerhu = text.decode("utf-8")
            word_list.append((len(word_list), (findSubStr(c,lalaerhu, time[c]+1), c.lower())))  # include normalize

    return word_list


def words_cleanup(words):
    cleaned_words = []
    for index, (offset, word) in words:  # words-(word index for search,(letter offset for display,word))
        if word in _STOP_WORDS:
            continue
        cleaned_words.append((index, (offset, word)))
    return cleaned_words


def word_index(text):
    words = word_split(text)
    words = words_cleanup(words)
    return words


def inverted_index(text):
    inverted = {}

    for index, (offset, word) in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append((index, offset))

    return inverted


def inverted_index_add(inverted, doc_id, doc_index):
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted


def search(inverted, query):
    words = [word for _, (offset, word) in word_index(query) if word in inverted]  # query_words_list
    results = [set(inverted[word].keys()) for word in words]
    # x = map(lambda old: old+1, x)
    doc_set = reduce(lambda x, y: x & y, results) if results else []
    precise_doc_dic = {}
    if doc_set:
        for doc in doc_set:
            index_list = [[indoff[0] for indoff in inverted[word][doc]] for word in words]
            offset_list = [[indoff[1] for indoff in inverted[word][doc]] for word in words]

            precise_doc_dic = precise(precise_doc_dic, doc, index_list, offset_list, 1)  # 词组查询
            precise_doc_dic = precise(precise_doc_dic, doc, index_list, offset_list, 2)  # 临近查询
            precise_doc_dic = precise(precise_doc_dic, doc, index_list, offset_list, 3)  # 临近查询

        return precise_doc_dic
    else:
        return {}


def precise(precise_doc_dic, doc, index_list, offset_list, range):
    if precise_doc_dic:
        if range != 1:
            return precise_doc_dic  # 如果已找到词组,不需再进行临近查询
    phrase_index = reduce(lambda x, y: set(map(lambda old: old + range, x)) & set(y), index_list)
    phrase_index = map(lambda x: x - len(index_list) - range + 2, phrase_index)

    if len(phrase_index):
        phrase_offset = []
        for po in phrase_index:
            phrase_offset.append(offset_list[0][index_list[0].index(po)])  # offset_list[0]代表第一个单词的字母偏移list
        precise_doc_dic[doc] = phrase_offset
    return precise_doc_dic


def search1(query):
    # Build Inverted-Index for documents
    inverted = {}
    # documents = {}
    #
    # doc1 = u"开发者可以指定自己自定义的词典，以便包含jieba词库里没有的词"
    # doc2 = u"军机处长到底是谁，Python Perl"
    #
    # documents.setdefault("doc1", doc1)
    # documents.setdefault("doc2", doc2)
    jilu = []
    documents = {}
    for filename in os.listdir('story'):
        f = open('story//' + filename).read()
        documents.setdefault(filename.decode('utf-8'), f)
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

        # Print Inverted-Index
        # for word, doc_locations in inverted.iteritems():
        # print word, doc_locations

    # Search something and print results
    # queries = [spell.correct('boak'),spell.correct('abook'),spell.correct('fish')]
    result_docs = search(inverted, query)
    str1 = ("Search for '%s': %s " % (query, u','.join(result_docs.keys()))) # %s是str()输出字符串%r是repr()输出对象
    jilu.append(str1.encode("utf-8").decode("utf-8"))
    def extract_text(doc, index):
        return documents[doc].decode('utf-8')[index:index + 50].replace('\n', ' ')

    if result_docs:
        for doc, offsets in result_docs.items():
            result_docs_list = sorted(result_docs.items(),key=lambda x:len(x[1]), reverse = True)
            for doc, offsets in result_docs_list:
                for offset in offsets:
                    str2 = '   - %s......%s ' % (extract_text(doc, offset),doc)
                    jilu.append(str2.encode("utf-8").decode("utf-8"))
    else:
        jilu.append( 'Nothing found!'.encode("utf-8").decode("utf-8"))

    print


    return jilu