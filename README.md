# practice-text2web
An application of GPT-3.5 to generate HTML from a text description

## libraries
os, OpenAI in Python

## 사용 내역
**Chat Completions API**

model: gpt-3.5-turbo

client.chat.completions.create의 "messages" argument에서 
- {"role": "system", "content": '사전 지시 작성'}
- {"role": "user", "content": '사용자 입력 제공'}

"temperature" argument에서
- 선택적 옵션으로 생성될 출력의 일관성 계수 조절 (결정적 또는 무작위적, 기본값: 0.7)

## 사용 방법
main 경로에서 

`>>>` python generate_website.py

`>>>` Enter text to describe your webpage: (사용자 입력)

사용자 입력 예시:
I want to make an apparel shopping mall. I need a homepage that contains the title of the shop 'The Brilliant', a fancy sentence under the title, an editable place for a full screen background image, an upper side horizontal menu consists of about us, mens, womens, FAQ, customer service, contact under the fancy sentence, the best seller items' horizontal placeholders for image and hyperlink, the brand-new items' placeholders for image and hyperlink parrellel to the bestsellers, search feature allowing users to find item.

사용 환경에 따라 py file의 OpenAI API 키 값을 선언해준다.
