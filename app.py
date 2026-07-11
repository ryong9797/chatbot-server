from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/price', methods=['POST'])
def get_price():
    req = request.get_json()
    try:
        # 카카오 파라미터 가져오기
        params = req.get('action', {}).get('parameters', {})
        item = params.get('item', {}).get('value')
        
        # 깃허브 파일명 규칙: data_감귤.json, data_감자.json ...
        filename = f"data_{item}.json"
        url = f"https://raw.githubusercontent.com/ryong9797/chatbot-server/main/{filename}"
        
        res = requests.get(url)
        
        if res.status_code == 200:
            data = res.json()
            # 파일 구조에 맞게 '가격' 추출 (데이터에 한글로 '가격'이라고 적혀있음)
            price = data.get('kpi', {}).get('가격', '정보 없음')
            return jsonify({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": f"{item}의 가격은 {price}원입니다."}}]
                }
            })
        else:
            # 실패 시 파일명을 보여주게 하여 무엇이 문제인지 확인
            return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"{filename} 파일을 찾을 수 없습니다. (상태코드: {res.status_code})"}}]}})
    except Exception as e:
        return jsonify({"version": "2.0", "template": {"outputs": [{"simpleText": {"text": f"오류: {str(e)}"}}]}})

if __name__ == '__main__':
    app.run()
