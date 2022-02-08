from flask import Flask,render_template, request, session
import random
from datetime import timedelta
import os
import datetime
import pytz
import time
from binascii import unhexlify
from symbolchain.core.CryptoTypes import PrivateKey
from symbolchain.core.symbol.KeyPair import KeyPair
from symbolchain.core.facade.SymbolFacade import SymbolFacade
from binascii import hexlify
import json
import http.client


app = Flask(__name__)

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)

########↓数当てカード↓####################################################################################
Card01=[1, 2, 3, 4, 5, 6, 7, 8]
Card02=[1, 9, 10, 11, 12, 13, 14, 15]
Card03=[1, 16, 17, 18, 19, 20, 20, 22]
Card04=[1, 23, 24, 25, 26, 27, 28, 29]
Card05=[1, 30, 31, 32, 33, 34, 35, 36]
Card06=[1, 37, 38, 39, 40, 41, 42, 43]
Card07=[1, 44, 45, 46, 47, 48, 49, 50]
Card08=[1, 51, 52, 53, 54, 55, 56, 57]
Card09=[2, 9, 16, 23, 30, 37, 44, 51]
Card10=[2, 10, 17, 24, 31, 38, 45, 52]
Card11=[2, 11, 18, 25, 32, 39, 46, 53]
Card12=[2, 12, 19, 26, 33, 40, 47, 54]
Card13=[2, 13, 20, 27, 34, 41, 48, 55]
Card14=[2, 14, 20, 28, 35, 42, 49, 56]
Card15=[2, 15, 22, 29, 36, 43, 50, 57]
Card16=[3, 9, 17, 25, 33, 41, 49, 57]
Card17=[3, 10, 18, 26, 34, 42, 50, 51]
Card18=[3, 11, 19, 27, 35, 43, 44, 52]
Card19=[3, 12, 20, 28, 36, 37, 45, 53]
Card20=[3, 13, 20, 29, 30, 38, 46, 54]
Card21=[3, 14, 22, 23, 31, 39, 47, 55]
Card22=[3, 15, 16, 24, 32, 40, 48, 56]
Card23=[4, 9, 18, 27, 36, 38, 47, 56]
Card24=[4, 10, 19, 28, 30, 39, 48, 57]
Card25=[4, 11, 20, 29, 31, 40, 49, 51]
Card26=[4, 12, 20, 23, 32, 41, 50, 52]
Card27=[4, 13, 22, 24, 33, 42, 44, 53]
Card28=[4, 14, 16, 25, 34, 43, 45, 54]
Card29=[4, 15, 17, 26, 35, 37, 46, 55]
Card30=[5, 9, 19, 29, 32, 42, 45, 55]
Card31=[5, 10, 20, 23, 33, 43, 46, 56]
Card32=[5, 11, 20, 24, 34, 37, 47, 57]
Card33=[5, 12, 22, 25, 35, 38, 48, 51]
Card34=[5, 13, 16, 26, 36, 39, 49, 52]
Card35=[5, 14, 17, 27, 30, 40, 50, 53]
Card36=[5, 15, 18, 28, 31, 41, 44, 54]
Card37=[6, 9, 20, 24, 35, 39, 50, 54]
Card38=[6, 10, 20, 25, 36, 40, 44, 55]
Card39=[6, 11, 22, 26, 30, 41, 45, 56]
Card40=[6, 12, 16, 27, 31, 42, 46, 57]
Card41=[6, 13, 17, 28, 32, 43, 47, 51]
Card42=[6, 14, 18, 29, 33, 37, 48, 52]
Card43=[6, 15, 19, 23, 34, 38, 49, 53]
Card44=[7, 9, 20, 26, 31, 43, 48, 53]
Card45=[7, 10, 22, 27, 32, 37, 49, 54]
Card46=[7, 11, 16, 28, 33, 38, 50, 55]
Card47=[7, 12, 17, 29, 34, 39, 44, 56]
Card48=[7, 13, 18, 23, 35, 40, 45, 57]
Card49=[7, 14, 19, 24, 36, 41, 46, 51]
Card50=[7, 15, 20, 25, 30, 42, 47, 52]
Card51=[8, 9, 22, 28, 34, 40, 46, 52]
Card52=[8, 10, 16, 29, 35, 41, 47, 53]
Card53=[8, 11, 17, 23, 36, 42, 48, 54]
Card54=[8, 12, 18, 24, 30, 43, 49, 55]
Card55=[8, 13, 19, 25, 31, 37, 50, 56]
Card56=[8, 14, 20, 26, 32, 38, 44, 57]
Card57=[8, 15, 20, 27, 33, 39, 45, 51]

#カードリスト
Card_lists = [Card01,Card02,Card03,Card04,Card05,Card06,Card07,Card08,Card09,Card10,
              Card11,Card12,Card13,Card14,Card15,Card16,Card17,Card18,Card19,Card20,
              Card21,Card22,Card23,Card24,Card25,Card26,Card27,Card28,Card29,Card30,
              Card31,Card32,Card33,Card34,Card35,Card36,Card37,Card38,Card39,Card40,
              Card41,Card42,Card43,Card44,Card45,Card46,Card47,Card48,Card49,Card50,
              Card51,Card52,Card53,Card54,Card55,Card56,Card57]


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        session.clear()
        return render_template("8NEM_index.html")
    except:
        return render_template("8NEM_index.html")



@app.route("/card", methods=["GET", "POST"])
def card():
   if request.method == "POST":
      #現在時刻を取得
      start0 = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
      #現在時刻をstrに変換
      start = start0.strftime('%Y/%m/%d %H:%M:%S')
      #想定用現在時刻を取得
      start1 = time.time()
      #現在時刻をセッションに格納
      session["start"] = start
      #測定用現在時刻をセッションに格納
      session["start1"] = start1
      start = session["start"]
      address = request.form.get('address')
      session["user"] = address
      address = session["user"]
      questions = 1
      session["questions"] = questions
      questions = session["questions"]
      point = 0
      session["point"] = point
      point = session["point"]

      #カードを2枚ランダムで抽出
      Card_choice = random.sample(Card_lists, 2)
      #リストの共通項を見つけ出す
      Card_choice_shuffle01 = random.sample(Card_choice[0], len(Card_choice[0]))
      #print(Card_choice_shuffle01)
      Card_choice_shuffle02 = random.sample(Card_choice[1], len(Card_choice[1]))
      #print(Card_choice_shuffle02)
      Overlapping = list(set(Card_choice_shuffle01) & set(Card_choice_shuffle02))
      session["overlapping"] = Overlapping

      #画面に表示する数字
      Value01 = Card_choice_shuffle02[0]
      Value02 = Card_choice_shuffle02[1]
      Value03 = Card_choice_shuffle02[2]
      Value04 = Card_choice_shuffle02[3]
      Value05 = Card_choice_shuffle02[4]
      Value06 = Card_choice_shuffle02[5]
      Value07 = Card_choice_shuffle02[6]
      Value08 = Card_choice_shuffle02[7]

      #1枚目のカードの画像
      img11 = str(Card_choice_shuffle01[0]) + ".png"
      img12 = str(Card_choice_shuffle01[1]) + ".png"
      img13 = str(Card_choice_shuffle01[2]) + ".png"
      img14 = str(Card_choice_shuffle01[3]) + ".png"
      img15 = str(Card_choice_shuffle01[4]) + ".png"
      img16 = str(Card_choice_shuffle01[5]) + ".png"
      img17 = str(Card_choice_shuffle01[6]) + ".png"
      img18 = str(Card_choice_shuffle01[7]) + ".png"

      #2枚目のカードの画像
      img21 = str(Card_choice_shuffle02[0]) + ".png"
      img22 = str(Card_choice_shuffle02[1]) + ".png"
      img23 = str(Card_choice_shuffle02[2]) + ".png"
      img24 = str(Card_choice_shuffle02[3]) + ".png"
      img25 = str(Card_choice_shuffle02[4]) + ".png"
      img26 = str(Card_choice_shuffle02[5]) + ".png"
      img27 = str(Card_choice_shuffle02[6]) + ".png"
      img28 = str(Card_choice_shuffle02[7]) + ".png"

      return render_template("8NEM_card.html",
                              Card01 = Card_choice_shuffle01, Card02 = Card_choice_shuffle02,
                              Overlapping = Overlapping[0],
                              Value01=Value01, Value02=Value02, Value03=Value03, Value04=Value04,
                              Value05=Value05, Value06=Value06, Value07=Value07, Value08=Value08,
                              address=address,
                              questions=questions,
                              point=point,
                              start=start,
                              img11=img11, img12=img12, img13=img13, img14=img14,
                              img15=img15, img16=img16, img17=img17, img18=img18,
                              img21=img21, img22=img22, img23=img23, img24=img24,
                              img25=img25, img26=img26, img27=img27, img28=img28
                              )
   elif "user" in session:
      address = session["user"]
      questions = session["questions"]
      session["questions"] = questions + 1
      questions = session["questions"]
      point = session["point"]
      start = session["start"]
      #カードを2枚ランダムで抽出
      Card_choice = random.sample(Card_lists, 2)
      #リストの共通項を見つけ出す
      Card_choice_shuffle01 = random.sample(Card_choice[0], len(Card_choice[0]))
      #print(Card_choice_shuffle01)
      Card_choice_shuffle02 = random.sample(Card_choice[1], len(Card_choice[1]))
      #print(Card_choice_shuffle02)
      Overlapping = list(set(Card_choice_shuffle01) & set(Card_choice_shuffle02))
      session["overlapping"] = Overlapping
      #画面に表示する数字
      Value01 = Card_choice_shuffle02[0]
      Value02 = Card_choice_shuffle02[1]
      Value03 = Card_choice_shuffle02[2]
      Value04 = Card_choice_shuffle02[3]
      Value05 = Card_choice_shuffle02[4]
      Value06 = Card_choice_shuffle02[5]
      Value07 = Card_choice_shuffle02[6]
      Value08 = Card_choice_shuffle02[7]
      #1枚目のカードの画像
      img11 = str(Card_choice_shuffle01[0]) + ".png"
      img12 = str(Card_choice_shuffle01[1]) + ".png"
      img13 = str(Card_choice_shuffle01[2]) + ".png"
      img14 = str(Card_choice_shuffle01[3]) + ".png"
      img15 = str(Card_choice_shuffle01[4]) + ".png"
      img16 = str(Card_choice_shuffle01[5]) + ".png"
      img17 = str(Card_choice_shuffle01[6]) + ".png"
      img18 = str(Card_choice_shuffle01[7]) + ".png"
      #2枚目のカードの画像
      img21 = str(Card_choice_shuffle02[0]) + ".png"
      img22 = str(Card_choice_shuffle02[1]) + ".png"
      img23 = str(Card_choice_shuffle02[2]) + ".png"
      img24 = str(Card_choice_shuffle02[3]) + ".png"
      img25 = str(Card_choice_shuffle02[4]) + ".png"
      img26 = str(Card_choice_shuffle02[5]) + ".png"
      img27 = str(Card_choice_shuffle02[6]) + ".png"
      img28 = str(Card_choice_shuffle02[7]) + ".png"
      return render_template("8NEM_card.html",
                              Card01 = Card_choice_shuffle01, Card02 = Card_choice_shuffle02,
                              Overlapping = Overlapping[0],
                              Value01=Value01, Value02=Value02, Value03=Value03, Value04=Value04,
                              Value05=Value05, Value06=Value06, Value07=Value07, Value08=Value08,
                              address=address,
                              questions=questions,
                              point=point,
                              start=start,
                              img11=img11, img12=img12, img13=img13, img14=img14,
                              img15=img15, img16=img16, img17=img17, img18=img18,
                              img21=img21, img22=img22, img23=img23, img24=img24,
                              img25=img25, img26=img26, img27=img27, img28=img28
                              )

@app.route("/answer", methods=["GET", "POST"])
def answer():
    try:
        questions = session["questions"]
        answer = request.form.get('radio')
        img99 = str(answer) + ".png"
        session["answer"] = answer
        correct = session["overlapping"]
        point = session["point"]
        link01 = "card"
        link02 = "result"

        if questions < 8:
            if correct[0] == int(answer):
                seikai = "NEMonsterを倒した！"
                session["point"] = point + 1
                point = session["point"]
                if  "user" in session:
                    return render_template("8NEM_answer.html", answer = answer, seikai = seikai, point=point, link=link01, img99=img99)

            else:
                session["point"] = point
                point = session["point"]
                if  "user" in session:
                    matigai = "NEMonsterに攻撃された！"
                    return render_template("8NEM_answer.html", answer = answer, seikai = matigai, point=point, link=link01, img99=img99)
        else:
            if correct[0] == int(answer):
                seikai = "NEMonsterを倒した！"
                session["point"] = point + 1
                point = session["point"]
                message = "ゲーム終了"
                end0 = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                end = end0.strftime('%Y/%m/%d %H:%M:%S')
                session["end"] = end
                end1 = time.time()
                session["end1"] = end1
                return render_template("8NEM_answer.html", message=message, link=link02, end=end, img99=img99, answer = answer, seikai = seikai, point=point)

            else:
                session["point"] = point
                matigai = "NEMonsterに攻撃された！"
                message = "ゲーム終了"
                end0 = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                end = end0.strftime('%Y/%m/%d %H:%M:%S')
                session["end"] = end
                end1 = time.time()
                session["end1"] = end1
                return render_template("8NEM_answer.html", message=message, link=link02, end=end, img99=img99, answer = answer, seikai = matigai, point=point)

    except:
        message = "ゲーム終了"
        end0 = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        end = end0.strftime('%Y/%m/%d %H:%M:%S')
        session["end"] = end
        end1 = time.time()
        session["end1"] = end1
        return render_template("8NEM_answer.html", message=message, link=link02, end=end)


@app.route("/result", methods=["GET", "POST"])
def result():
    r_address = session["user"]
    point = session["point"]
    start = session["start"]
    end = session["end"]
    start1 = session["start1"]
    end1 = session["end1"]
    time = ('{:.1f}'.format(end1 - start1))

    #この下からSymbol送金プログラムを記載
    if len(r_address) == 39 and r_address[0] == "N":
        facade = SymbolFacade('mainnet')
        b = unhexlify("秘密鍵")
        prikey = PrivateKey(b)
        keypair = KeyPair(prikey)
        pubkey = keypair.public_key
        address = facade.network.public_key_to_address(pubkey)
        print(address)
        recipient_address = SymbolFacade.Address(r_address)
        print(recipient_address)

        deadline = (int((datetime.datetime.today() + datetime.timedelta(hours=2)).timestamp()) - 1615853185) * 1000
        tx = facade.transaction_factory.create({
          'type': 'transfer',
          'signer_public_key': pubkey,
          'fee': 30000,
          'deadline': deadline,
          'recipient_address': recipient_address,
          'mosaics': [(0x7E7A62B9AECA3121, int(point * 100))],
          'message': bytes(1) + "".encode('utf8')
        })
        #print(tx)
        signature = facade.sign_transaction(keypair, tx)
        tx.signature = signature.bytes

        payload = {"payload": hexlify(tx.serialize()).decode('utf8').upper()}
        jsonPayload = json.dumps(payload)
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection("symbol-harvesting.tokyo",3000)
        conn.request("PUT", "/transactions", jsonPayload,headers)

        response = conn.getresponse()
        print(response.status, response.reason)

        hash = facade.hash_transaction(tx)
        print('https://symbol-harvesting.tokyo:3000/transactionStatus/' + str(hash))

    else:
        pass

    return render_template("8NEM_result.html",name=r_address, point=point, start=start, end=end, time=time)


if __name__ == "__main__":
    app.run(debug=True)
