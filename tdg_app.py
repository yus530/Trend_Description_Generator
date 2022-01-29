from flask import *
app = Flask(__name__)
import nltk
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
import csv
import random
import time
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# with open('../csv/test_data3.csv') as f1:
#     reader = csv.reader(f1)
#     data = [row for row in reader]

with open('./csv/dict_vn.csv') as f2:
    reader = csv.reader(f2)
    dict_vn = [row for row in reader]

with open('./csv/dict_advj.csv') as f3:
    reader = csv.reader(f3)
    dict_advj = [row for row in reader]

#nltkを用いた方のisPlural()のテスト用ファイル
# with open('./csv/isPlural_accuracy_test.csv') as f4:
#     reader = csv.reader(f4)
#     isp_accuracy_test = [row for row in reader]

#https://www.worldsys.org/europe/
#[male,female]の順に分けられている
with open('./csv/person_name.csv') as f5:
    reader = csv.reader(f5)
    name_list = [row for row in reader]


#判定をタグでできるか考える
def is_plural(noun): #ref=https://try2explore.com/questions/jp/11463316
    lemma = wnl.lemmatize(noun, 'n')
    isp = True if noun != lemma else False
    return lemma
    # return isp


def change_to_possessive(name):
    cp=""
    for i in range(len(name_list)):
      if name==name_list[i][0]:
        cp="his"
        return cp 
      if name==name_list[i][1]: 
        cp="her"
        return cp
    cp="their" if is_plural(name.lower())==True else "its"
    return cp

def make_subject_list(subject):
    subject_list=[]
    after_of_list=[]
    s=subject
    s0=s[0].lower()+s[1:]
    s1=s2=s3=s4=s5=s6=sx=""
    noun=pronoun=""
    target_pprp=[" in "," from "," on "," to "," for "," In "," From "," On "," To "," For "," IN "," FROM "," ON "," TO "," FOR "," who "," which "," whose "," that "," Who "," Which "," Whose "," That "," WHO "," WHICH "," WHOSE "," THAT "]
    target_of=[" of "," Of "," OF "]
    target_possessive="'s "

    for i in target_of:
      if i in s0:
          idx = s0.find(i)
          s1= s0[:idx]#ofの前の部分を取得
          idx += 4
          s2 = s0[idx:]#ofの後の部分を取得
          break
      else: s2=s0


    #s2を短くしていく
    for i in target_pprp:
      if i in s2:
          idx = s2.find(i)
          s3= s2[:idx]#inとかの前の部分を取得
          break
      else: s3=s2

    if target_possessive in s3:#Boby's dog のようなときにhis dog に変えたい。change_to_possessive()を使う
      idx = s3.find(target_possessive)
      # print("idx:"+str(idx))
      noun = s3[:idx]#'sの前の名詞を取得
      idx += 2
      s4 = change_to_possessive(noun)+s3[idx:] 
    else: s4=s3
    for i in reversed(range(len(s4))):
      if s4[i]==" ": break
      sx+=s4[i]
    noun=sx[::-1]
    s5 = "they" if is_plural(noun)==True else "it" 

    after_of_list.append(s2)
    if s3 not in after_of_list: after_of_list.append(s3)
    if s4 not in after_of_list: after_of_list.append(s4)

    if s1!="":
      if s5=="they":
        s5="them"
        after_of_list.append(s5)
      for i in range(len(after_of_list)):
        s6=(s1+" of " + after_of_list[i])
        subject_list.append(s6)
      subject_list.append("it")
    else:
      after_of_list.append(s5)

    return subject_list if s1!="" else after_of_list


def get_subject_list(subject_list,data_len): #同じ主語を何回使用するかを決める
    choiced_subject_list=[]
    #1つの主語当たり2回まで使用可能。順番に使用していき、もし全部使い切ったら、また最初から。
    idx=0
    for i in range(data_len):
      if idx==len(subject_list): idx=0
      choice=random.choices([1,2],weights=[7.5,2.5],k=1)
      for j in range(choice[0]):
        choiced_subject_list.append(subject_list[idx])
      idx+=1  
    if len(choiced_subject_list)>data_len:
      x=len(choiced_subject_list)-data_len
      for i in range(x):
        choiced_subject_list.pop()

    return choiced_subject_list


def get_diff_average(diff_list):
    x=0
    for i in range(len(diff_list)):
      if i!=0:
        x+=float(abs(diff_list[i]))
    return x/(len(diff_list))


def get_diff_list(data):
    diff_list=[]
    for i in range(len(data)-1):
      if i!=0:
        diff_list.append(float(data[i+1][1])-float(data[i][1]))
    return diff_list


def get_vn_advj(diff,diff_average):
    #evaluation criteria:　diff diff_averageから評価基準を作成
    eva_crit_list=[0,diff_average*0.5,diff_average,diff_average*1.5,diff_average*2] #[0-25-50-75-100]
    # print("Evaluation Criteria:")
    # print(eva_crit_list)
    abs_diff=abs(diff)
    advj=["",""]
    for i in range(len(eva_crit_list)-1):
      if abs_diff==0: 
        break 
      if abs_diff>=eva_crit_list[4]: 
        advj=dict_advj[3] 
        break
      if abs_diff>=eva_crit_list[i] and abs_diff<eva_crit_list[i+1]:
        advj=dict_advj[i]
        break
    if diff==0: return dict_vn[0],advj
    elif diff>0:
      return dict_vn[random.choice([1,2,3])],advj
    else:
      return dict_vn[random.choice([4,5,6])],advj


def get_fbt_list(data,diff_list): #from,by,to
    idx=2
    diff_list_index=0
    fbt_list=[]
    for i in data:
      if idx==(len(data)): break
      choice=random.choices([0,1,2],weights=[4,4,2],k=1)
      if choice[0]==0:
        fbt_list.append("from " + data[idx-1][0] +  " by " + str(abs(diff_list[diff_list_index]))) # from by
      elif choice[0]==1:
        fbt_list.append("from " + data[idx-1][0] + " to " + data[idx][0])  # from to
      else:
        fbt_list.append("from " + data[idx-1][0] +  " by " + str(abs(diff_list[diff_list_index]))+ " to " + data[idx][0])
      idx += 1
      diff_list_index+=1
    return fbt_list

def get_highest_lowest(data):
    highest_idx=lowest_idx=0
    sentence_high=sentence_low=""
    value_list=[]
    idx=0
    for i in range(len(data)):
      if i!=0:
          value_list.append(data[i][1])
    highest_idx=value_list.index(max(value_list))
    lowest_idx=value_list.index(min(value_list))

    sentence_high+=data[highest_idx+1][0]+" has the highest value."
    sentence_low+=data[lowest_idx+1][0]+" has the lowest value."
    highest=[highest_idx+1,sentence_high]
    lowest=[lowest_idx+1,sentence_low]
    return highest,lowest

def make_sentence(data):
    sentence_list = []
    data_len=len(data)-1 #データの名前の分を引く
    # できる主語(文章)の数はdata_lenからさらに-1した数。subject_listの要素数=diiff_listの要素数=文章の数
    subject_list=get_subject_list(make_subject_list(data[0][0]),data_len-1)
    
    diff_list=get_diff_list(data)
    diff_average=get_diff_average(diff_list)
    fbt_list=get_fbt_list(data,diff_list)
    #0,1を重みをつけて選択。　s+v->70%,there is->30%
    #https://docs.python.org/ja/3/library/random.html#functions-for-sequences
    sentence_type=random.choices([0,1],weights=[6,4],k=(data_len-1)) # 0:s+v 1:There is ~ 
    fbt_position=random.choices([0,1],weights=[8,2],k=(data_len-1)) # 0: ~ fbt 1: fbt, ~
    highest,lowest=get_highest_lowest(data)
    sentence_type[0]=0 #最初の一文だけはS+Vの形
    fbt_position[0]=0 #最初の一文だけはfbtは文の後ろに設置

    for i in range(data_len-1):
      s=""
      vn,advj=get_vn_advj(diff_list[i],diff_average)
      if sentence_type[i]==0:
        s+=(subject_list[i]+" "+vn[0]+" "+advj[0])
      else:
        s+="there is"
        if "a little" not in advj[1]: # a littleがない場合
          if advj[1]!="": #形容詞がある場合
            s+=(" a " + advj[1]+" "+vn[1])
          else: #形容詞が無くて名詞がaeiouで始まる場合
            if vn[1][0]=="a" or vn[1][0]=="e" or vn[1][0]=="i" or vn[1][0]=="o" or vn[1][0]=="u":
              s+=(" an " + advj[1]+" "+vn[1])
        else:
          s+=(" "+advj[1]+" "+vn[1])
        if vn[1]=="no change": s+=(" "+vn[1])


      sentence=""
      if fbt_position[i]==0:
          sentence=(s[0].upper()+s[1:] + " " + fbt_list[i] + ".")
      else:
        sentence=(fbt_list[i][0].upper()+fbt_list[i][1:] + ", " + s +".")
      sentence_list.append(sentence)
       
    sentence_list.insert(highest[0],highest[1])
    sentence_list.insert(lowest[0],lowest[1])

    return sentence_list


@app.route('/')
def init():
    return render_template('layout.html')

@app.route('/tdg_input',methods=['GET','POST'])
def input():
    #return "input test"
    return render_template('tdg_input.html')


@app.route('/tdg_output', methods=["POST"])
def output():
    #input_values=request.form.get("value")
    error_message="Error: "

    input_name=request.form.get("name")
    input_item_list=request.form.getlist("item")
    input_value_list=request.form.getlist("value")
    num=len(input_item_list)+1
    data=[["" for i in range(2)] for i in range(num)]
    #https://teratail.com/questions/103349
    # https://www.headboost.jp/python-list-how-to-convert-a-value/
    if input_name=="":
      error_message+="There was not Name of data. Please Back and Input again."
      return render_template('tdg_output.html', data=data, graph=data, name=input_name, result=error_message)
    data[0][0]=input_name
    for i in range(num):
        if i!=0:
          if input_item_list[i-1]!="":
            data[i][0]=input_item_list[i-1]
            if input_value_list[i-1]!='':
              data[i][1]=input_value_list[i-1]
            else:
              data[i][1]=0
        print(data[i])
    # print(data)
    # print(input_name)
    # print(input_item_list)
    # print(input_value_list)
    # print(st1)
   

    # print("")
    # print(data)
    s=make_sentence(data)
    result=""
    for i in s: 
      print("  "+i)
      result+=(i+" ")
    data.pop(0)
    #return "show test"
    return render_template('tdg_output.html', data=data, graph=data, name=input_name, result=result)
    #return 'input_text: %s' % input_text

if __name__ == "_main_":
    app.run(debug=True)

# print("")
# print(data)
# s=make_sentence(data)
# for i in s: print("  "+i)
