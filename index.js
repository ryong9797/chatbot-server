const express = require("express");
const app = express();

app.use(express.json());

app.post("/api/price", (req, res) => {
  const response = {
    "version": "2.0",
    "template": {
      "outputs": [
        {
          "simpleText": {
            "text": "현재 대파 가격은 3,000원입니다."
          }
        }
      ]
    }
  };
  res.json(response);
});

app.listen(3000, () => console.log("서버가 시작되었습니다!"));
