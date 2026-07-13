from flask import Flask, request, jsonify
import requests
import os
import urllib.parse  # 한글 인코딩을 위해 추가

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        item = req.get('action', {}).get('parameters', {}).get('item', {}).get('value')
        
        if not item:
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": "조회할 품목을 선택하지 않았습니다."}}]
                }
            })
            
        # ⚠️ 한글 품목명을 URL 안전 문자열로 인코딩합니다 (예: 배추 -> %EB%B0%B0%EC%B3%94)
        encoded_item = urllib.parse.quote(item)
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/data_{encoded_item}.json"
        
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            price = data.get('kpi', {}).get('가격')
            
            if not price:
                price = str(data)
                
            response_text = f"조회하신 {item}의 가격 정보는 다음과 같습니다:\n{price}"
        else:
            # 404 등 파일 로드 실패 시 디버깅을 위해 에러 코드를 상세히 출력하도록 개선
            response_text = f"'{item}' 가격 데이터를 찾을 수 없습니다. (URL 오류 코드: {res.status_code})"
            
    except Exception as e:
        response_text = f"가격 조회 중 오류가 발생했습니다: {str(e)}"

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": response_text}}]
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
