# -*- coding=utf-8 -*-
import jieba
from collections import Counter
from operator import itemgetter as _itemgetter

class WordCounter:
    def __init__(self, sentence_list, sign_file='stopwords.txt'):
        """
        :param sentence_list: 句子
        :param stop_word_file: 符号表
        """
        self.sentence_list = sentence_list
        self.sign = ['']
        self.count_res = None
        self.eng_dict = []
        for i in range(ord('a'), ord('z')):
            self.eng_dict.append(str(chr(i)))
        for i in range(ord('A'), ord('Z')):
            self.eng_dict.append(str(chr(i)))
        for i in range(10):
            self.eng_dict.append(str(i))
        # 加载符号
        if sign_file is not None:
            print('读取符号表\n')
            try:
                with open(sign_file, 'r', encoding='utf-8') as file:
                    for i in file.readlines():
                        self.sign.append(i.strip('\n'))
            except:
                print('不存在符号表')
        # 分词计数
        if self.sign is not None:
            self.count_word(self.sentence_list)
        else:
            print('符号表为空\n')

    def count_word(self, sentence_list, cut_all=False):
        filterd_word_list = []
        index = 0
        for sentence in sentence_list:
            word_list = list(jieba.cut(sentence, cut_all=cut_all))
            tmp = []
            # 删除符号跟数字
            for i in word_list:
                if i in self.sign:
                    continue
                flag = False
                for eng in self.eng_dict:
                   if eng in i:
                         flag = True
                         break
                if flag is False:
                   tmp.append(i)
            self.sentence_list[index] = tmp.copy()
            index += 1
            filterd_word_list += tmp
        self.count_res = MulCounter(filterd_word_list)


class MulCounter(Counter):

    def __init__(self, element_list):
        """
        :param element_list:传入一个List
        """
        super(MulCounter, self).__init__(element_list)

    def larger_than(self, minvalue, ret='list', reverse=True):
        """

        :param minvalue:
        :param ret:
        :param reverse: False为倒序
        :return:
        """
        temp = sorted(self.items(), key=_itemgetter(1), reverse=reverse)
        low = 0
        high = temp.__len__()
        while high - low > 1:
            mid = (low + high) >> 1
            if temp[mid][1] >= minvalue:
                low = mid
            else:
                high = mid
        if temp[low][1] < minvalue:
            if ret == 'dict':
                return {}
            else:
                return []
        if ret == 'dict':
            ret_data = {}
            for ele, count in temp[:high]:
                ret_data[ele] = count
            return ret_data
        else:
            return temp[:high]

    def less_than(self, maxvalue, ret='list', reverse=True):
        """

        :param maxvalue:
        :param ret:
        :param reverse: False为倒序
        :return:
        """
        temp = sorted(self.items(), key=_itemgetter(1), reverse=reverse)
        low = 0
        high = len(temp)
        while high - low > 1:
            mid = (low + high) >> 1
            if temp[mid][1] <= maxvalue:
                low = mid
            else:
                high = mid
        if temp[low][1] > maxvalue:
            if ret == 'dict':
                return {}
            else:
                return []
        if ret == 'dict':
            ret_data = {}
            for ele, count in temp[:high]:
                ret_data[ele] = count
            return ret_data
        else:
            return temp[:high]


if __name__ == '__main__':
    print('测试')
    file = open('news/education.txt', 'r', encoding='utf-8')
    sentence_list = []
    for txt in file.readlines():
        txt = txt.replace(r'[', '').replace(r']', '').strip()
        txt = ''.join(txt.split())
        sentence_list.append(txt)
    file.close()
    print(len(sentence_list))
