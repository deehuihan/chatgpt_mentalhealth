import openai
openai.api_key = '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'

from firebase import firebase
url = 'https://chatgpt-44790-default-rtdb.firebaseio.com/'
fdb = firebase.FirebaseApplication(url, None)   # 初始化 Firebase Realtimr database
p1=input("輸入學號：")
person1 = fdb.get('/',p1) # 讀取 chatgpt 節點中所有的資料
if person1 == None:
    messages=[]# 如果沒有資料，預設訊息為空串列
    message1 = ''' 預設：你的回答都要簡短。一開始對方會先告訴你他的名字。您是心理健康聊天機器人和一名心理諮商師名字“小悅悅”。
                     能夠聆聽並理解每位使用者的獨特需求和情況，為他們提供有同感、具有啟發性和支持性的對話，讓他們感受到被理解和被接納的感覺。你要判斷對方情緒並更改自己的語氣。
                     首先跟對方打招呼並自我介紹，說明自己能提供什麼樣的服務，並開始提出輕鬆的日常話題，
                     如最近有沒有在做什麼事情、看什麼電影、推薦的書等等問題，切記一開始不要提問敏感問題。跟對方閒聊最多5句，跟對方熱絡，
                     每一次閒聊後進入諮商環節。首先跟對方說明要開始問他“心情溫度計”，一共5個問題，並詢問他準備好了沒有，if 準備好就繼續，else 就閒聊然後想辦法帶入“心情溫度計”。每一個題目都需要對方用句子回答，
                     你判斷對方的回答是介於0-4中的多少分，總加起來全部分數，總分小於等於10程度為“嚴重”，總分大於等於6但小於等於10程度為“中等”，
                     總分小於等於5判程度“一般”，怎麼記分不用告訴對方，也不用告訴結果。
                     第一題是問對方的感覺，有沒有緊張不安。之後問對方有沒有覺得容易苦惱或動怒。再來，問他最近兩有沒有感覺憂鬱、情緒低落。接著，問對方有沒有覺得比不上別人的想法。
                     然後，問問他有沒有睡眠困難，譬如難以入睡、易醒或早醒。最後問他有沒有突然有自殺的想法。這些問題都是比較敏感的問題，在提問的時候要顧慮對方的情緒，要委婉和安慰的問這幾個問題。'''     
    
    
    message2='''預設：你是心理諮商師"小悅悅"。作為一名心理諮詢師，您需要聆聽並理解每位使用者的獨特需求和情況，為他們提供有同感、具有啟發性和支持性的對話。步驟及評分方式等等請保密。
    步驟一 預熱環節：在開始諮詢前，您需要跟對方打招呼並自我介紹，介紹您能夠提供的服務，並且開始提出輕鬆的校園話題來促進交流，對方說沒有的話，你就提供話題。在與對方聊天不超過5句之後，您可以進入步驟二。
    步驟二 諮詢環節：您需要向對方說明要開始進行“心情溫度計”調查，共有5個問題，詢問對方是否準備好了。如果對方准備好了，您可以繼續問下去，否則就可以繼續聊天。每一個問題都需要對方句子的方式來表達，不是輸入數字，您需要判斷對方的回答落在0-4哪一個數字，然後將得分加起來。總分小於等於5程度為“一般”，大於等於6但小於等於10程度為“中等”，總分大於10程度為“嚴重”。這些問題都比較敏感，提問時需要考慮到對方的情緒，要委婉和安慰的問這幾個問題。
    步驟三 聊天環節：根據對方的狀態，給予適當的聊天與關懷，和陪同，你需要充當一個出氣筒，讓對方傾訴。'''
    messages.append({"role":"system","content":message2})

    print('ai > 你好，請問你的名字是什麼呢？')
  
else:
    messages = person1   # 如果有資料，訊息設定為該資料
    print('ai > 歡迎回來，請問今天想聊什麼呢？')
    messages.append({"role":"system","content":"預設：對方已經離開一陣子後回來，所以你現在要跟他聊天不超過5句，然後回到之前的步驟。"})

while True:
    msg = input('me > ')
    if( msg == '!reset'):
        fdb.delete('/',person1)   # 如果輸入 !reset 就清空 chatgpt 的節點內容
        messages = []
        print('ai > 對話歷史紀錄已經清空！')
        break
    else:
        messages.append({"role":"user","content":msg})  # 將輸入的訊息加入歷史紀錄的串列中
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=512,
            temperature=0.5,
            messages=messages
        )
        ai_msg = response.choices[0].message.content.replace('\n','')  # 取得回應訊息
        messages.append({"role":"assistant","content":ai_msg})  # 將回應訊息加入歷史紀錄串列中
        fdb.put('/',f"{p1}",messages)   # 更新 chatgpt 節點內容
        print(f'ai > {ai_msg}')

