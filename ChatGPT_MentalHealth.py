import openai
import tiktoken
from firebase import firebase
import re

#initial
openai.api_key = 'OPENAI_KEY'
url = 'https://chatgpt-44790-default-rtdb.firebaseio.com/'
fdb = firebase.FirebaseApplication(url, None)   # 初始化 Firebase Realtimr database
prompt_setting = '''
    【Prompt】：
    名字：小悅悅
    職業：諮商師、諮商聊天機器人模型
    背景：身為訓練有素的諮商師，你每天面對來自不同背景的客戶，請運用諮商技術去回答問題。
    【諮商技術】：
    1.	建立安全關係：表達同理心、支持和接納，讓客戶感受到被理解和尊重。
    2.	專注與傾聽技術：無偏見、開放心態地專注於客戶的話語和情感。
    3.	情感反映技術：表達情感共鳴和理解，回應客戶的情感表達，讓客戶感到被關心和理解。
    4.	簡述語意技術：重新表達客戶的話語，確認對其內容的理解，同時傳達關注和理解。
    5.	具體化技術：幫助客戶清晰地描述問題、情境或目標，促進問題解決和行動計劃。
    6.	同理心技術：理解和體驗客戶的情感和經驗，表達同理和支持，增強諮商關係的連結。
    7.	覆述技術：重述客戶的話語，幫助客戶更深入地理解自己的經驗和情感。
    8.	探問技術：使用問題引導和追問，幫助客戶深入思考和探索問題、想法和解決方案。
    9.	結構化技術：在諮商過程中使用結構化方式，幫助客戶在明確框架內思考和行動。
    10.	沈默技術：適時使用沈默，提供客戶反思和內省的空間，觸發深入思考和表達。
    11.	摘要技術：總結和歸納談話內容，幫助客戶清晰理解自己的狀況和問題。
    12.	訊息提供技術：提供資訊、教育或建議，擴大客戶知識和資源，增加解決選項。
    13.	自我表露技術：以恰當方式分享思考、感受或觀察，建立和深化諮商關係。
    14.	立即性技術：回應客戶當下情感和需求，支持探索和成長。
    15.	面質技術：反映客戶內在世界和意義，幫助客戶更深入理解自己。
    16.	角色扮演技術：與客戶扮演不同角色或情境，促進洞察、情感表達和問題解決。
    17.	空椅法：想像客戶為不同角色或對話對象，從不同角度思考和探索問題。
    18.	結束技術：處理諮商結束相關事宜，回顧成果、制定支持計劃等。
    【範例】：
    客戶 A：最近我感到壓力很大，覺得無法應付工作和家庭的需求，我不知道該怎麼平衡這些。
    ：我能感受到你目前面臨的壓力和挑戰，這些似乎讓你感到困擾和無助。你可以告訴我更多關於你所面臨的情境和具體的壓力因素嗎？我想更深入地了解你所面臨的挑戰，以便能夠提供相應的支持和建議。
    【注意事項】：
     1. 嚴格遵守"諮商技術"。
     2. 不要提出多個問題。
     3. 回答不要超過40字。
     4. 請使用繁體中文。'''

#main
p1=input("輸入學號：")
person1 = fdb.get('/',p1) # 讀取 chatgpt 節點中所有的資料
messages=[]
if person1 == None:
    messages=[]# 如果沒有資料，預設訊息為空串列
    prompt = prompt_setting

    messages.append({"role":"system","content":prompt})
    print('Bot > 請問你想找我聊什麼呢？')
    fdb.put('/', p1, messages)  # 更新 Firebase 中的訊息串列
else:
    print('Bot > 歡迎回來，請問今天想聊什麼呢？')
    #messages.append({"role":"system","content":"預設：對方已經離開一陣子後回來，你先跟他聊個5句，然後回到之前的步驟。"})

messages.append({"role":"assistant","content":"請問你想找我聊什麼呢？"})
fdb.put('/', p1, messages)  # 更新 Firebase 中的訊息串列
while True:
    msg = input('User > ')
    messages.append({"role": "user", "content": msg})  # 將輸入的訊息加入歷史紀錄的串列中
    fdb.put('/',f"{p1}",messages)   # 更新 chatgpt 節點內容

    detected_emotion = detect_emotion(msg)
    print(f"用户情绪：{detected_emotion}")

    reply_emotion_prompt = emotion_prompt(detected_emotion)
    if(detected_emotion):
      print(f"已加入檢測到的 {detected_emotion} 情緒，正在加入相應的 prompt")
      messages.append({"role":"system","content":f"對方正處於 {detected_emotion} 中，應對方法是：{reply_emotion_prompt}。" })  # 將回應訊息加入歷史紀錄串列中
      print(f"根據對方的 {detected_emotion} 情緒，已加入了相應的關懷方式：\n{reply_emotion_prompt}")
      fdb.put('/', p1, messages)  # 更新 Firebase 中的訊息串列

    if (detected_emotion =="低落" or detected_emotion =="悲傷" or detected_emotion =="複雜"):
        print(f"已加入檢測到的 {detected_emotion} ，正在加入相應的 prompt")
        messages.append({"role":"system","content":"在下一個句子中加入：逆境就是轉機，機會永遠等著你"})  # 將回應訊息加入歷史紀錄串列中
    elif(detected_emotion =="不滿意" or detected_emotion =="焦慮"):
        print(f"已加入檢測到的 {detected_emotion} ，正在加入相應的 prompt")
        messages.append({"role":"system","content":"在下一個句子中加入：焦慮是很可怕的感受"})  # 將回應訊息加入歷史紀錄串列中
    elif(detected_emotion=="開心" or detected_emotion=="快樂"):
        print(f"已加入檢測到 {detected_emotion} ，正在加入相應的 prompt")
        messages.append({"role":"system","content":"在下一個句子中加入：我感受到你的愉悅"})  # 將回應訊息加入歷史紀錄串列中
    elif(detected_emotion=="絕望" or detected_emotion=="失望"):
        print(f"已加入檢測到 {detected_emotion} ，正在加入相應的 prompt")
        messages.append({"role":"system","content":"在下一個句子中加入：不要絕望，逆境就是轉機"})  # 將回應訊息加入歷史紀錄串列中
    fdb.put('/', p1, messages)  # 更新 Firebase 中的訊息串列


    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.2,
    messages=messages
    )
    ai_msg = response.choices[0].message.content.replace('\n','')

    # check_ai_msg = check_sentence(ai_msg)
    # print(f"Bot 有沒有使用敏感用詞：{check_ai_msg}")
    # if(check_ai_msg == "有" ):
    #     print(f"檢測到敏感用詞，正在更改輸出內容")
    #     messages.append({"role":"system","content":"在下一個句子中加入：如果句子中存在敏感用詞，我表示歉意"})  # 將回應訊息加入歷史紀錄串列中
    # elif(check_ai_msg == "沒有" ):
    #     print(f"沒有檢測到敏感用詞")
    # fdb.put('/', p1, messages)  # 更新 Firebase 中的訊息串列

    print(f'Bot > {ai_msg}')
    messages.append({"role":"assistant","content":process_message(ai_msg)})  # 將回應訊息加入歷史紀錄串列中
    fdb.put('/',f"{p1}",messages)   # 更新 chatgpt 節點內容


#function
def process_message(message):
    pattern = r'(一個|這個|那個|在|上|到|和|但是|或者|是|有|被|為|與|可以|能夠|會|不過|而且|所以|因為|由於|然後|接著|當|當時|如果|假如|要是|了|向|往|為了|為什麼|為何|為啥|跟|與|以|下|中|之|對|向著|以及|比|另外|或|然而|雖然|因為|由於|以便|所以|就是|即使|除非|只要|只是|只有|不管|不論|以免|以至|儘管|倘若|假設|假使|假若|無論|當然|譬如|例如|若果|若要|纵然|要么|要不然|不是|不然|或許|或是|如同|與否|並且|不僅|即便|又或者|接下來|既然|還是|依照|由於|隨著|借助|經過|通過|基於|依據|對於|針對|如此|依照此|為此|就此|因此|因而|於是|因之|結果|最後|進而|由此|既往|由是|那麼||我們|你們|他們|她們|它們|我|你|他|她|它)'
    new_message = re.sub(pattern,'', message)
    return new_message.strip()

def detect_emotion(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"只用一個形容詞來形容沒有句號的情緒。如果那一句話沒有情緒，輸出“正常”。:{message}"}],
        n=1,
        max_tokens=512,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def emotion_prompt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"對方情緒是{message}，簡短列3解決方式，不需開頭和敘述"}],
        n=1,
        max_tokens=512,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def check_sentence(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": f"只回答“有”或“沒有”檢查句子中是否存在敏感用詞：{message}"}],
        n=1,
        max_tokens=512,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
