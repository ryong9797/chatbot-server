"""
카카오톡 챗봇과 실시간 연동하여 농산물 가격 정보를 제공하는 Flask 서버입니다.
"""
from flask import Flask, request, jsonify
import requests
import os
import urllib.parse

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오 챗봇 파라미터에서 item(농산물 명) 값을 안전하게 추출합니다.
        action = req.get('action', {})
        detail_params = action.get('detailParams', {})
        params = action.get('params', {})
        
        item = None
        # 1. detailParams에서 우선적으로 value 추출
        if 'item' in detail_params:
            item = detail_params.get('item', {}).get('value')
        # 2. 없을 경우 params에서 추출
        elif 'item' in params:
            item = params.get('item')
        
        # 품목 정보가 없을 때의 처리
        if not item:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": "조회할 품목을 선택하지 않았습니다."}}]
                }
            })
            
        # ⚠️ 만약 파라미터에 "배추 가격"처럼 "가격"이 포함되어 들어온 경우 "가격"을 제거해 "배추"로 만듭니다.
        item = item.replace("가격", "").strip()
            
        # 깃허브에 올리신 농산물 JSON 파일 주소 (한글 파일명 인코딩)
        encoded_item = urllib.parse.quote(item)
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{encoded_item}.json"
        
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
            response_text = f"'{item}' 가격 데이터를 찾을 수 없습니다. (오류 코드: {res.status_code})"
            
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
