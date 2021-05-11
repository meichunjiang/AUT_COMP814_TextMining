# Comp814 Text Mining Assignment 2
# Author : Chunjiang Mei 20100106
# Date   : 1/5/2021

# Task Brief
# You are employed by an innovation company who has bought the blogs with the objective of innovating new products/services based on what people have been talking about on popular blog sites.
#
# In particular your boss wants to know the two most popular topics that the bloggers have been talking about in the following demographics :
# a)	Males
# b)	Females
# c)	Age brackets <=20 and over 20.
# d)	Everyone
#
#
#
# Task Requirements
# In order to achieve the objectives of the project, you will firstly need to read in the data, extract the meta data and segment it into the required demographics.
# You will then need to design strategies to extract and cluster topics.
#
# To be consistent within the class, let us use the same definition for a topic. Let us define a topic to be the mention of an OBJECT or a THING.
# So, for instance you could simply take the THING that is mentioned as the highest number of times as the popular topic and correspondingly the second most popular topic.
#
# Once you get the two most dominant “things” mentioned, expand the topic to be 2 verb/noun before and 2 verb/noun after the topic.
# Output them as “what has been said about the dominant “thing” in terms of the 4 surrounding nouns/verbs.
#
# Repeat what you done using frequency above, but this time use TFIDF. For this consider all the blogs from one person as a document.
#
# Compare the results from the two modes of counting and comment on which one is more accurate in your opinion with justifications.
#
# Note that you will need to use various techniques such as stemming, lemmatization, PCA, stop word removal, inter alia, in order to get as accurate results as possible.
# The results will need to be evaluated manually and the strategy for evaluation should be described in your writeup.
#
#
#
# Write up
#
# 1.	You need to document the research project as a scientific paper using latex double column IEEE conference format. The latex template can be downloaded from Blackboard.
# 2.	You should also submit a well commented and formatted python code as part of the appendix.
#
# 3.	 Your paper should describe:
#         a)	The task you set out to solve.
#         b)	A literature review of same or similar tasks attempted by other researchers.
#         c)	The details of your strategy to solve the problem. In this part you should describe the details of how you processed the data from start
#               to finish including the details of how the data got processed in any external library you have used (if you have used it).
#         d)	How you ensured the accuracy of your results.
#         e)	The conclusion and how you would do the task differently if you were to do it again.
#
#
#


# import nltk
import os
import shutil
import re
import xml.sax
import xml.dom.minidom
from xml.dom.minidom import parse

BLOGS_PATH      = '/Users/chunjiangmei/Documents/OneDrive - AUT University/00 Semester 1 2021/Text Mining - COMP814/Assessment/blogs/'
BLOGS_PATH1     = '/Users/chunjiangmei/Documents/OneDrive - AUT University/00 Semester 1 2021/Text Mining - COMP814/Assessment/blogs_UnicodeDecodeError/'
path            = '/Users/chunjiangmei/Documents/OneDrive - AUT University/00 Semester 1 2021/Text Mining - COMP814/Assessment/'
MACOS_SYS_FILE  = '.DS_Store'
XML_FILE_NUM    = len(os.listdir(BLOGS_PATH))
XML_FILE_LIST   = os.listdir(BLOGS_PATH)

if os.path.exists(path+'meta_data_file.txt'):
    os.remove(path+'meta_data_file.txt')
    os.remove(path + 'log.txt')

meta_data_file  = open(path+'meta_data_file.txt', 'w')
log_file        = open(path+'log.txt', 'w')

class XML_Meta_Data():

    def __init__(self,filepath,filename):
        if filename == MACOS_SYS_FILE:
            print("[Error] except in " + filename, file=log_file)
            return
        try:
            self.dates          = []
            self.posts          = []
            self.filepath       = filepath
            self.filename       = filename
            self.ID             = self.filename .split('.', 6)[0]
            self.Gender         = self.filename .split('.', 6)[1]
            self.Age            = self.filename .split('.', 6)[2]
            self.Occupation     = self.filename .split('.', 6)[3]
            self.Constellation  = self.filename .split('.', 6)[4]

            # Get dates and posts Meta Dat with Regular Expression Matching
            with open(self.filepath + self.filename, "r") as f:
                blogs = f.read()
                pattern_dates = re.compile('<date>\d\d,[a-zA-Z]+,\d\d\d\d</date>')
                partern_posts = re.compile('<post>[\s\S]*?</post>', re.M)
                self._result_dates = pattern_dates.findall(blogs)
                self._result_posts = partern_posts.findall(blogs)
                self.postNum = len(self._result_posts)
                self.dateNum = len(self._result_dates)
                if(self.postNum!=self.dateNum):
                    print("[CRITICAL] dates number(",self.dateNum,") and posts number(",self.postNum,") are different in file  ",self.filename, file=log_file)
                else:
                    # print("dates number(",self.dateNum,") and posts number(",self.postNum,") are same ! ")
                    self.XML_Normalization()
            f.close()
        except xml.parsers.expat.ExpatError as err:
            print("[CRITICAL] XML_Meta_Data.__init__() except xml.parsers.expat.ExpatError in " + self.filename, '\t\tError Code is ',err.code, file=log_file)
            return
        except UnicodeDecodeError as err:
            print("[CRITICAL] Extract_Dates_Posts() except Error in " + self.filename, file=log_file)
            return

    def XML_Normalization(self):
        # del words in the XML
        words = [
                 ['<post>', ''], ['</post>', '']
                ,['&nbsp;',' '],['\^_\^',' ']
                ,['\n',' '],['\r',' '],['\t',' ']
                ]

        # normalization dates
        for num in range(self.dateNum):
            self.dates.append(re.sub('</date>', '',re.sub('<date>', '', self._result_dates[num])))

        # normalization posts
        for num in range(self.postNum):
            newpost = self._result_posts[num]
            for i in range(len(words)-1):
                newpost = re.sub(words[i][0],words[i][1], newpost)
            self.posts.append(newpost)
            # print("匹配new post结果：",self.posts ,'\n')

        # with open(self.filepath+self.filename, "r") as f1, open("%s.bak" % (self.filepath+self.filename), "w") as f2:
        #     try:
        #         for line in f1:
        #             f2.write(re.sub('&nbsp;', '', line))
        #     except UnicodeDecodeError as err:
        #         shutil.move(self.filepath+self.filename, BLOGS_PATH1+self.filename)
        #         print("[CRITICAL] XML_Meta_Data.XML_Normalization() except UnicodeDecodeError in " + self.filename,  file=log_file)
        #         return
        # os.remove(self.filepath+self.filename)
        # os.rename("%s.bak" % (self.filepath+self.filename), (self.filepath+self.filename))
        return
    def Get_Posts(self):
        print('ID is  :', self.ID,' Gender is  :', self.Gender,'Age is  :', self.Age,'Occupation is :', self.Occupation,'Constellation is :', self.Constellation)
        for i in range(self.postNum):
            print('【Data】:',self.dates[i])
            print('【Post】:',self.posts[i])

#####################################################################################################################################



print("------------- Start -------------")
for i in range(XML_FILE_NUM):
    # print('Processing XML file No.',i,'--->','%.2f%% ' % (100 * i / XML_FILE_NUM),XML_FILE_LIST[i])
    XML_FILE_NAME = XML_FILE_LIST[i]                                      # Get xml file name
    if XML_FILE_NAME == MACOS_SYS_FILE:
        print("[Error] except in " + XML_FILE_NAME, file=log_file)
        continue
    B = XML_Meta_Data(BLOGS_PATH,XML_FILE_NAME)                           # 初始化类
    # if XML_FILE_NAME == '113390.male.24.Museums-Libraries.Gemini.xml':
    #     print(B.postNum,B.dateNum)
    B.Get_Posts()
# 当前进展：
# 1. XML文件处理阶段 (基本数据已经提取完毕，)
# 下一步动作：
# 1. date and post 作为XML_Meta_Data类的属性存储.
# 2. post 中去除特殊字符
# 发现的问题：
# 1.发现113390.male.24.Museums-Libraries.Gemini.xml 中posts的date数据缺失
# 2.特殊字符待处理：发现&nbsp;(空格),& 字符 ，&copy; 等 in the posts
# 3.发现部分600个文件左右有UnicodeDecodeError 的错误，已经暂时移动到～/blogs_UnicodeDecodeError文件夹下了

print("------------- End -------------")



# ################################## Testing Code ##################################################################################################
print("------------- Testing Start-------------")
# words = [ ['<post>', ''], ['</post>', '']
#                 ,['&nbsp;',' '],['\^_\^',' ']
#                 ,['\n',' '],['\r',' ']
#         ]
# file = path+"Test.xml"
# with open(file, "r") as f:
#     try:
#         blogs = f.read()
#         pattern_dates = re.compile('<date>\d\d,[a-zA-Z]+,\d\d\d\d</date>')  # '<date>\s\d\d,[a-zA-Z],\d\d\d\d\s</date>'
#         partern_posts = re.compile('<post>[\s\S]*?</post>', re.M)
#         result_dates = pattern_dates.findall(blogs)
#         result_posts = partern_posts.findall(blogs)
#
#         if(len(result_dates) == len(result_posts)):
#
#             print("匹配date结果：",result_dates[0])
#             print("匹配post结果：", result_posts[0])
#             print("匹配date结果：",result_dates[1])
#             print("匹配post结果：", result_posts[1])
#
#         # normalization posts
#         for num in range(len(result_posts)):
#             newpost = result_posts[num]
#             for i in range(len(words)-1):
#                 newpost = re.sub(words[i][0],words[i][1], newpost)
#             print('[normalization posts] : ',newpost)
#
#
#     except UnicodeDecodeError as err:
#         print("[CRITICAL] except Error in ")


print("------------- Testing End -------------")
# ################################## Testing Code ##################################################################################################

meta_data_file.close()
log_file.close()