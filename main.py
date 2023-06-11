from flask import Flask, render_template
import pymysql.cursors
import json
import math

app = Flask(__name__)

conn = pymysql.connect(host='183.99.87.90',
                            user='root',
                            password='swhacademy!',
                            db='Munchan',
                            charset='utf8')



def sum(lists):
    result = 0
    for i in lists:
        result = result + i[1]

    return result



with conn.cursor() as cursor:

    sql = 'SELECT id, company, title, editedTime, origin FROM newsContents WHERE dt = "20230106";'
    cursor.execute(sql)
    all_news = cursor.fetchall()

    sql = 'SELECT word, polarity FROM dictionary;'
    cursor.execute(sql)
    all_emotion = cursor.fetchall()

    all_datas = list()

    for news in all_news:
        content = list(set(news[4].split()))
        emotions = list()

        for word in content:
            for emotion in all_emotion:
                if word.replace('"', '') == emotion[0]:
                    emotions.append(emotion)


        if sum(emotions) > 0:
            all_datas.append([news[0], news[1],news[2], news[3], '긍정 [ %d ]' % sum(emotions)])
        elif sum(emotions) < 0:
            all_datas.append([news[0], news[1],news[2], news[3], '부정 [ %d ]' % sum(emotions)])
        elif sum(emotions) == 0:
            all_datas.append([news[0], news[1], news[2], news[3], '보통 [ %d ]' % sum(emotions)])

@app.route('/')
def main_page():
    return render_template('index.html', values=all_datas)

@app.route('/<pk_id>')
def news_info(pk_id):
    with conn.cursor() as cursor:
        data = []
        sql = 'SELECT title, origin FROM newsContents WHERE id = "%s";' % pk_id
        cursor.execute(sql)
        news = cursor.fetchone()

        print(news)

        sql = 'SELECT word, polarity FROM dictionary;'
        cursor.execute(sql)
        all_emotion = cursor.fetchall()

        emotions = list()
        labels = []
        dataSet = []
        if bool(news) != False:
            content = news[1].split()

            for word in content:
                for emotion in all_emotion:
                    if word.replace('"', '') == emotion[0]:
                        labels.append(emotion[0])
                        dataSet.append(emotion[-1])

                        if emotion[1] > 0:
                            emotions.append([emotion[0], '긍정 [ %d ]' % emotion[1]])
                        elif emotion[1] < 0:
                            emotions.append([emotion[0], '부정 [ %d ]' % emotion[1]])
                        elif emotion[1] == 0:
                            emotions.append([emotion[0], '보통 [ %d ]' % emotion[1]])

            data = [news[0], emotions, labels, dataSet]

            return render_template('news_lists.html', values=data)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")