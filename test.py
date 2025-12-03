def call(sentance):
    vovels=['a','e','i','o','u']
    vov=[]
    cons=[]
    for i in sentance:
        if i in vovels:
            vov.append(i)
        else:
            cons.append(i)
    return [vov,cons]        
data=call('kireeti')
print(data)
            