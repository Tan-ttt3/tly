from http.client import GONE
import re
from turtle import goto
from pyparsing import GoToColumn
import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud, Line
from pyecharts.globals import SymbolType
from pyecharts.charts import Line
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 获取页面内容并解析词语
def get_words(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # 设置编码防止乱码
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

# 定义分词函数
def word_segmentation(text):
    # words = jieba.cut(text)
    # 使用jieba进行中文分词，排除标点符号和其他没有意义的中文字
    words = [word for word in jieba.lcut(text) if word.isalnum() and len(word) > 1]
    return list(words)

# 定义绘制词云函数
def draw_word_cloud(words_count):
    wc = (
        WordCloud()
        .add("", words_count, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="词云图"))
    )
    return wc

# 定义过滤低频词函数
def filter_low_frequency(words_count, min_frequency):
    filtered_words_count = dict()
    for word, count in words_count.items():
        if count >= min_frequency:
            filtered_words_count[word] = count
    return filtered_words_count

# 主应用
def main():
    # 页面标题
    st.title("交互式文本分析Web应用")

    # 文章URL输入框
    url = st.text_input("请输入文章URL")

 #Chart Types
    chart_types = ["折线图", "柱状图",  "散点图", "面积图", "直方图"]
    chart_type = st.selectbox("选择图表类型", chart_types)

    # 抓取文本内容
    if st.button("抓取文本内容"):
        text_content = get_words(url)
        st.text("文本内容：")
        st.text_area("内容展示", text_content, height=300)
        
        words = word_segmentation(text_content)
        words_count = Counter(words)
        word_list = [[word, count] for word, count in words_count.items()]
        wc = draw_word_cloud(word_list)
        st.text("词频排名前20：")
      
        
        # Common data for top 20 words
        sorted_words_count = sorted(words_count.items(), key=lambda x: x[1], reverse=True)
        top_20_words = dict(sorted_words_count[:20])
        x_data = list(top_20_words.keys())
        y_data = list(top_20_words.values())
        data = pd.DataFrame({"词频": y_data}, index=x_data)
        
        # Chart generation based on selected type
        if chart_type == "折线图":
            st.text("词频折线图：")
            st.line_chart(data)
        elif chart_type == "柱状图":
            st.text("词频柱状图：")
            st.bar_chart(data)
        elif chart_type == "散点图":
            st.text("词频散点图：")
            st.scatter_chart(data)
        elif chart_type == "面积图":
            st.text("词频面积图：")
            st.area_chart(data)
        elif chart_type == "直方图":
            st.text("词频直方图：")
            st.bar_chart(data, use_container_width=True)
       
        
if __name__ == "__main__":
    main()

 