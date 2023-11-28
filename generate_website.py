import os
from openai import OpenAI

# OpenAI API 키 값을 시스템 환경변수에서 불러온다. 
# 참조: (Step 2: Setup your API key Setup your API key for all projects (recommended), https://platform.openai.com/docs/quickstart?context=python)
# 시스템 환경변수가 설정되어 있지 않으면 아래 값을 지우고 키 값을 직접 선언해도 된다.
api_key = os.environ.get("OPENAI_API_KEY")

# OpenAI client 초기화
client = OpenAI(api_key=api_key)


def extract_code(response):
    # 출력된 내용 중 필요로 하는 코드가 '# START CODE'와 '# END CODE' 사이에 있다는 가정하에 이를 추출한다.
    start_marker = '# START CODE'
    end_marker = '# END CODE'

    # 코드에서 시작 위치와 종료 위치 파악
    start_pos = response.find(start_marker)
    end_pos = response.find(end_marker)

    # 필요한 부분만 추출
    if start_pos != -1 and end_pos != -1:
        code = response[start_pos + len(start_marker):end_pos].strip()
        return code
    else:
        return None
    

def generate_webpage_content(user_input):
    # GPT를 이용하여 사용자 입력에 따른 HTML 내용 생성
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 모델 버전 설정
        messages=[
            {"role": "system", "content": 
             '''
             You are a HTML website maker.
             
             INSTRUCTION:
             - make a real one, not an example.
             - enclose the code between delimiters "# START CODE" and "# END CODE".
             '''
            }, # 좋은 결과를 도출하기 위하여 미리 어느정도의 지시를 내린다.
            {"role": "user", "content": user_input}
        ],
#         max_tokens=10000, # 필요하다면 출력 토큰 길이를 제한한다.
        temperature = 0.5, # 일관성과 결정적 <---> 다양성과 창의적 수준의 조절 계수. 기본값: 0.7, 범위: 0 to 2
    )

    # 생성된 response 에서 담고 있는 값들 중 필요한 내용만 선택한다
    generated_html = response.choices[0].message.content
    generated_html = extract_code(generated_html)
    assert generated_html is not None # extract_code의 오류 확인
    return generated_html

    
def save_to_file(content, filedir):
    # 생성된 파일을 저장할 공간을 확인하고 내부에 파일이 있다면 전부 지워버린다.
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    for f in os.listdir(filedir):
        os.remove(os.path.join(filedir, f))
    
    # 생성된 내용물을 사전 정의된 이름으로 특정 경로에 저장한다.
    filepath = os.path.join(filedir, "generated_webpage.html")
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

        
        
        
if __name__ == "__main__":
    # 사용자로부터 생성할 웹페이지에 대한 설명을 입력 받는다.
    user_input = str(input("Enter text to describe your webpage: "))

    # 웹페이지 생성
    generated_content = generate_webpage_content(user_input)

    # 이 파일이 위치하는 directory에 결과값을 저장하기 위한 path를 지정한다.
    file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
    
    # 지정된 directory에 생성된 내용을 저장한다.
    save_to_file(generated_content, filedir=file_dir)

    print(f"Webpage content generated and saved to '{file_dir}'")