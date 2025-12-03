def call(sentance):
    vovels=['a','e','i','o','u']
    vov=[]
    cons=[]
    data={}
    sentance=sentance.replace(" ","")
    for i in sentance:
        if i ==vovels:
            vov.append(i)
            data['vovels']=vov
    return data
data=input('enter sentance')
stm=call(data)
print(stm)
