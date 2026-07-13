"""
카카오톡 챗봇과 실시간 연동하여 농산물 가격 정보를 제공하는 Flask 서버입니다.
"""
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오 챗봇 파라미터에서 item(농산물 명) 값을 가져옵니다.
        item = req.get('action', {}).get('parameters', {}).get('item', {}).get('value')
        
        if not item:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [
                        {"simpleText": {"text": "조회할 품목을 인식하지 못했습니다."}}
                    ]
                }
            })
            
        # 깃허브에 올리신 농산물 JSON 파일 주소
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{item}.json"
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            
            # JSON 데이터 내 kpi -> 가격 데이터 추출 시도
            price = data.get('kpi', {}).get('가격')
            
            # 만약 가격 정보가 없으면 데이터 전체를 보여주도록 설정
            if not price:
                price = str(data)
                
            response_text = f"조회하신 {item}의 가격 정보는 다음과 같습니다:\n{price}"
        else:
            response_text = f"'{item}'에 대한 가격 데이터를 찾을 수 없습니다. (오류 코드: {res.status_code})"
            
    except Exception as e:
        response_text = f"가격 조회 중 오류가 발생했습니다: {str(e)}"

    # 카카오 챗봇 규격에 맞춰 JSON 형태로 응답 반환
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": response_text
                    }
                }
            ]
        }
    })

if __name__ == '__main__':
    # Render.com 등의 클라우드 환경에서는 PORT 환경변수를 바인딩해주어야 헬스체크가 성공합니다.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
