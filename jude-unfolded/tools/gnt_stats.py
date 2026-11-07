import sys,glob,os,collections
d=sys.argv[1]
books={}
for f in sorted(glob.glob(os.path.join(d,'[6-8][0-9]-*.txt'))):
    name=os.path.basename(f).split('-')[1].replace('.txt','')
    rows=[l.split() for l in open(f,encoding='utf-8') if l.strip()]
    books[name]=rows
total=collections.Counter(); perbook=collections.defaultdict(collections.Counter)
for b,rows in books.items():
    for r in rows:
        total[r[6]]+=1; perbook[b][r[6]]+=1
jude=books['Jud']
print('Jude tokens:',len(jude),' distinct lemmas:',len(perbook['Jud']))
print('Total NT tokens:',sum(total.values()))
hap=[l for l in perbook['Jud'] if total[l]==perbook['Jud'][l]]
print('\nLemmas in Jude found nowhere else in SBLGNT NT (%d):'%len(hap))
order=[]
for r in jude:
    if r[6] in hap and r[6] not in order: order.append(r[6])
for l in order:
    v=[int(r[0][4:6]) for r in jude if r[6]==l]
    print(f'  {l}  vv.{sorted(set(v))}  x{perbook["Jud"][l]}')
only2=[l for l in perbook['Jud'] if total[l]==perbook['Jud'][l]+perbook['2Pe'][l] and perbook['2Pe'][l]>0]
print('\nLemmas occurring only in Jude and 2 Peter (%d):'%len(only2))
for l in only2: print('  ',l, 'Jude',perbook['Jud'][l],'2Pe',perbook['2Pe'][l])
for key in ['τηρέω','οὗτος','ἀσεβής','ἀσέβεια','ἀσεβέω','ἀγαπητός','ἀγάπη','ἔλεος','ἐλεάω','κρίσις','κρίμα','ἅπαξ','πᾶς','κύριος','Ἰησοῦς','Χριστός','θεός','πνεῦμα','σάρξ','ζόφος','φυλάσσω','πίστις','ἅγιος','ἐπιθυμία','πορεύομαι','βλασφημέω','αἰών','αἰώνιος','ἑαυτοῦ','ὑμεῖς','δόξα','σῴζω','ἀπόλλυμι']:
    vs=sorted(set(int(r[0][4:6]) for r in jude if r[6]==key))
    print(f'{key}: Jude x{perbook["Jud"][key]} vv.{vs}  NT x{total[key]}')
