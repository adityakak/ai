import random
from math import log
import time
import sys

alphabetToNumber = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11,
                    'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22,
                    'X': 23, 'Y': 24, 'Z': 25}
numberToAlphabet = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
                    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
                    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
ngramFreq = {}
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
NGRAM_SIZE = 4
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .2


def encode(org, cipher):
    for loc, character in enumerate(org):
        if character.isalpha():
            cipherSearch = alphabetToNumber[character.upper()]
            org = org[:loc] + cipher[cipherSearch] + org[loc + 1:]
    return org


def decode(org, cipher):
    for loc, character in enumerate(org):
        if character.isalpha():
            alphabetLocation = cipher.index(character.upper())
            org = org[:loc] + numberToAlphabet[alphabetLocation] + org[loc + 1:]
    return org


def ngramFitness(encoded, cipher, n):
    decoded = decode(encoded, cipher)
    ngram = [decoded[x:x + n] for x in range(len(decoded)) if x + n < len(decoded) and decoded[x:x + n].isalpha()]
    total = 0
    for grams in ngram:
        try:
            freq = ngramFreq[grams]
            total += log(freq, 2)
        except KeyError:
            continue
    return total


def hillClimbing(encoded):
    randomStart = list(alphabetToNumber.keys())
    random.shuffle(randomStart)
    decoded = decode(encoded, randomStart)
    currentMaxScore = ngramFitness(decoded, '', 4)
    bestCipher = randomStart.copy()
    while True:
        swap1, swap2 = random.randint(0, 25), random.randint(0, 25)
        while swap1 == swap2:
            swap2 = random.randint(0, 25)
        randomStart[swap1], randomStart[swap2] = randomStart[swap2], randomStart[swap1]
        decoded = decode(encoded, randomStart)
        score = ngramFitness(decoded, '', 4)
        if score > currentMaxScore:
            currentMaxScore = score
            bestCipher = randomStart.copy()
        randomStart = bestCipher.copy()
        print(decode(encoded, bestCipher), currentMaxScore)


def breed(parent1, parent2):
    child = '%%%%%%%%%%%%%%%%%%%%%%%%%%'
    dominate, nonDominate = (parent1, parent2) if random.randint(0, 1) == 0 else (parent2, parent1)
    cross = random.sample(list(numberToAlphabet.keys()), CROSSOVER_LOCATIONS)
    placed = set()
    for item in cross:
        placed.add(dominate[0][item])
        child = child[:item] + dominate[0][item] + child[item + 1:]
    for item in nonDominate[0]:
        if item not in placed:
            placed.add(item)
            nextIndex = child.index('%')
            child = child[:nextIndex] + item + child[nextIndex + 1:]
    return child


def genetic(encoded):
    initialCiphers = []
    added = set()
    while len(initialCiphers) < POPULATION_SIZE:
        randomStart = list(alphabetToNumber.keys())
        random.shuffle(randomStart)
        stringForm = ''.join(randomStart)
        if stringForm not in added:
            added.add(stringForm)
            initialCiphers.append(stringForm)
    for iteration in range(POPULATION_SIZE):
        initialCiphers = [(x, ngramFitness(encoded, x, NGRAM_SIZE)) for x in initialCiphers]
        initialCiphers.sort(reverse=True, key=lambda x: x[1])
        # print('Generation %d Best Score: %s' % (iteration, initialCiphers[0][1]))
        print('Generation %d Decoded: %s' % (iteration, decode(encoded, initialCiphers[0][0])))
        print()
        nextGen = [initialCiphers[x][0] for x in range(0, NUM_CLONES)]
        createdChildren = {initialCiphers[x][0] for x in range(0, NUM_CLONES)}
        tourneyParticipants = random.sample(initialCiphers, 2 * TOURNAMENT_SIZE)
        tourney1 = sorted(tourneyParticipants[:len(tourneyParticipants) // 2], key=lambda x: x[1], reverse=True)
        tourney2 = sorted(tourneyParticipants[len(tourneyParticipants) // 2:], key=lambda x: x[1], reverse=True)
        parent1 = parent2 = None
        while len(nextGen) < POPULATION_SIZE:
            for i in tourney1:
                if random.random() < TOURNAMENT_WIN_PROBABILITY:
                    parent1 = i
                    break
            for i in tourney2:
                if random.random() < TOURNAMENT_WIN_PROBABILITY:
                    parent2 = i
                    break
            child = breed(parent1, parent2)
            if random.random() < MUTATION_RATE:
                swap1, swap2 = random.randint(0, 25), random.randint(0, 25)
                while swap1 == swap2:
                    swap2 = random.randint(0, 25)
                temp = child[swap1]
                child = child[:swap1] + child[swap2] + child[swap1 + 1:]
                child = child[:swap2] + temp + child[swap2 + 1:]
            if child not in createdChildren:
                nextGen.append(child)
                createdChildren.add(child)
        initialCiphers = nextGen.copy()


def initializer():
    with open('ngrams.txt') as f:
        for line in f:
            ngram, freq = line.strip().split()
            ngramFreq[ngram] = int(freq)


initializer()
start = time.perf_counter()
genetic(sys.argv[1])
# Number 1
'''
genetic("""PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT
TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ
GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS
DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT
SVEFG. GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR
NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL
HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT
FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF. GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR
ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ
GUR NPGVIVGVRF JBEX (CYRNFR QBA'G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF
GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR
PBZZBAF NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY. SBE NA
RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE
PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR. GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF
CEBWRPG, FRR BHE CRBCYR CNTR. SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR. SBE ZBER
VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR.""")
'''

# Number 2
'''
genetic("""LTQCXT LRJJ HJRDECD, EZT CDJP SXTFRYTDE EC ZNKT LTTD RASTNHZTY VNF NDYXTV WCZDFCD. ZT VNF NHUBREETY LP N
FRDGJT KCET VZTD N LXNKT FTDNECX QXCA ONDFNF XTQBFTY EC PRTJY QXCA SXTFFBXT EC HCDKRHE EZT SXTFRYTDE.
ZNY WCZDFCD LTTD HCDKRHETY, EZT FSTNOTX CQ EZT ZCBFT VCBJY ZNKT LTHCAT SXTFRYTDE FRDHT WCZDFCD ZNY DC
KRHTSXTFRYTDE. RDHXTYRLJP, RE VNF EZRF FNAT FSTNOTX VZC JTY EZT RASTNHZATDE RD EZT ZCBFT CQ
XTSXTFTDENERKTF. EZBF, ZNY EZT FTDNET HCDKRHETY EZT SXTFRYTDE, EZRF VCBJY ZNKT NACBDETY EC N SCJRERHNJ
HCBS.""")
'''

# Number 3
'''
genetic("""ZRTGO Y JPEYPGZA, RP'J IKPGO HIJJRMWG PI RSHEITG PUG JPEYPGZA MA SYDROZ EYOBIS XUYOZGJ, PGJPROZ PUG
EGJLWP IK PUIJG XUYOZGJ, YOB DGGHROZ IOWA PUG MGPPGE ILPXISGJ. PURJ RJ XYWWGB URWW XWRSMROZ. PURJ RJ
EGWYPRTGWA JRSHWG PI XIBG, MLP BIGJO'P CIED RO GTGEA JRPLYPRIO - RP XYO IKPGO ZGP XYLZUP RO Y WIXYW
SYFRSLS, Y JPEYPGZA PUYP RJ OIP RBGYW MLP KEIS CURXU YOA JROZWG XUYOZG RJ OIP YO RSHEITGSGOP IO RPJ ICO.
ZGOGPRX YWZIERPUSJ YEG Y HICGEKLW PIIW KIE RSHEITROZ IO PUG RBGY IK URWW XWRSMROZ PI IHPRSRVG Y JIWLPRIO
RO JRPLYPRIOJ CUGEG YWW IK PUG KIWWICROZ YEG PELG: Y JPEYPGZA XYO MG HEGXRJGWA QLYOPRKRGB MA Y JHGXRKRX
JGP IK TYERYMWGJ ZRTGO XGEPYRO OLSGERX TYWLGJ. PUG ILPXISG IK PUG JPEYPGZA XYO YWJI MG HEGXRJGWA
QLYOPRKRGB. PUGEG YEG ROPGEYXPRIOJ MGPCGGO PUG TYERYMWGJ PUYP SYDG JRSHWG URWW XWRSMROZ ROGKKRXRGOP IE
LOWRDGWA PI JLXXGGB.""")
'''
# Number 4
'''
genetic("""CWQ KHTTQKC TFAZJAB HS FGG HS CWQ ECFT YFTE PHRJQE TQGQFEQM EH SFT JE CWQ QPXJTQ ECTJZQE VFKZ, F AQY
WHXQ, CWQ GFEC OQMJ, TQCLTA HS CWQ OQMJ, THBLQ HAQ, EHGH, TQRQABQ HS CWQ EJCW, CWQ SHTKQ FYFZQAE, TJEQ
HS CWQ EZNYFGZQT, CWQ XWFACHP PQAFKQ, FCCFKZ HS CWQ KGHAQE. CWQ KHTTQKC TFAZJAB HS CWQ CWTQQ JAMJFAF
OHAQE PHRJQE JE CWQ GFEC KTLEFMQ, TFJMQTE HS CWQ GHEC FTZ, CQPXGQ HS MHHP. CWQTQ JE AH SHLTCW JAMJFAF
OHAQE PHRJQ, FAM FANHAQ YWH CQGGE NHL HCWQTYJEQ JE F GJFT. OLEC CQGG CWQP CH CLTA FTHLAM FAM YFGZ FYFN
VQSHTQ CWQN KFA VGQEE NHL YJCW FAN HCWQT JAKHTTQKC HXJAJHAE. FANYFN, EH EFNQCW PN STJQAM VJGG, YWH
WFXXQAQM CH VQ HAGJAQ YWJGQ J YFE PFZJAB CWJE FEEJBAPQAC, YWQA J FEZQM WJP 'YWFC YHLGM VQ F BHHM EQKTQC
PQEEFBQ SHT PN ECLMQACE CH MQKHMQ?' XGQFEQ CFZQ LX FAN KHPXGFJACE YJCW WJP.""")
'''
# Number 5
'''
genetic("""XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI. GR GQ BEQX ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL
KMQR SMKKML VMPYQ GL BLDJGQF: 'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER RBESFBP.'""")
'''
# Number 6
'''
genetic("""XTV B CHDQCL BHF GCVIVDGDHWPN ABVF ZABPPLHWL, ZTHGDFLV MBJDHW B PTHW BHF XCPPN VLBFBYPL GLVDLG TX UTVFG
HLRLV CGDHW B GDHWPL LEBMIPL TX TCV ULPP-PTRLF LHWPDGA WPNIA UADZA TZZCVG GLZTHF IPBZL DH TRLVBPP
XVLQCLHZN. DX D BM WLHCDHL, D UDPP GBN MBHN, MBHN GLZTHFG ABRL IBGGLF UADPL D ABRL YLLH ALVL ITHFLVDHW
MBJDHW GCZA B UTVJ. FDGZTRLVDHW NTC ZVBZJLF MN YVBDHZADPF, ALVL, DH B GMBPPLV HCMYLV TX GLZTHFG UTCPF
WDRL ML HT GCVIVDGL.""")
'''
# Number 7
'''
genetic("""NU XTZEIMYTNEVZ INUHU YM, ZML SPYVI NXILNFFZ XNFF IVPU N API VNTD. NU PI ILTWU MLI, P XNW YM N FMWY JNZ
JPIVMLI LUPWY NWZ MC IVNI YFZEV IVNI ITNDPIPMWNFFZ CMFFMJU 'D' NI NFF. PUW'I IVNI ULTETPUPWY? P CMLWD
IVPU ULTETPUPWY, NWZJNZ! NW NLIVMT JVM NFUM CMLWD IVPU ULTETPUPWY, FMWY NYM, NXILNFFZ FMUI SNWZ SMWIVU
JTPIPWY N AMMH - N CLFF CPXIPMWNF UIMTZ - JPIVMLI IVNI YFZEV NI NFF. NSNRPWY, TPYVI?""")
'''
# Number 8
'''
genetic("""RHNJJCBXVCXJYQJNEJNDYDCELTHNBFTVTHNJJREFCLBEECANOTREFDNEBXTHJTNXTXECPCBAPZNSSPXTNYTXFVZCNXTSXRKRJTGTYECJ
RKTRDFSNHTRANGRDTNKNFEFZTTECQSNSTXCDVZRHZFEXNRGZEJRDTFEXRNDGJTFFUBNXTFSTDENGCDFZTINGCDFNDYCEZTXQRGBXTFRD
FETNYCQXTANRDRDGQRITYRDEZTRXSJNHTFACKTQXTTJPNLCBECDCXRDEZTFBXQNHTLBEVREZCBEEZTSCVTXCQXRFRDGNLCKTCXFRDORD
GLTJCVREKTXPABHZJROTFZNYCVFCDJPZNXYVREZJBARDCBFTYGTFNDYPCBVRJJEZTDZNKTNSXTEEPHCXXTHEDCERCDCQAPHCBDEXPNDY
HCBDEXPATDNJNFNQTVPTNXFNGCRFZCBJYZNKTFNRYAPBDRKTXFTLBEDCVAPARDYZNFLTTDCSTDTYECZRGZTXKRTVFCQEZRDGF""")
'''
# Number 9
'''
genetic("""W CTZV VYQXDVD MCWJ IVJJTHV, TYD VYQXDVD WM BVAA, FXK WM QXYMTWYJ MCV JVQKVM XF MCV PYWZVKJV! YX
KVTAAS, WM DXVJ! SXP DXY'M NVAWVZV IV? BCS BXPAD SXP YXM NVAWVZV MCTM MCWJ RVKFVQMAS QKXIPAVYM JVQKVM
MVGM QXYMTWYJ MCV NV TAA, VYD TAA, HKTYDVJM JVQKVM XF TAA MCV QXJIXJ? YXB W FVVA DWJKVJRVQMVD! CTZV
SXP DWJQXZVKVD SXPK XBY NVMMVK PAMWITMV MKPMC XF VZVKSMCWYH? W DWDY'M MCWYL JX. JX BCS TKV SXP HVMMWYH
TAA PRRWMS TM IV? CXYVJMAS. YX XYV CTJ TYS ITYYVKJ MCVJV DTSJ. ...BCTM'J MCTM? SXP BTYM IV MX MVAA
SXP MCV JVQKVM? YXM TFMVK MCWJ LWYD XF DWJKVJRVQM! HXXDYVJJ HKTQWXPJ IV. NTQL BCVY W BTJ T SXPMC W
BTJ YXM JX QTAAXPJ. BCVY JXIVXYV BVAA KVJRVQMVD TYD WIRXKMTYM MXAD IV MCTM MCVS CTD JXIVMCWYH BXKMC
MVAAWYH IV, W OPJM AWJMVYVD! W DWDY'M DXPNM MCVI! JX KPDV, CXYVJMAS. OPJM PYTQQVRMTNAV.
""")
'''
# Number 10
'''
genetic("""ZFNNANWJWYBZLKEHBZTNSKDDGJWYLWSBFNSSJWYFNKBGLKOCNKSJEBDWZFNGKLJKJNQFJPFJBXHBZTNRDKNZFNPDEJWYDRPDEGCNZNWJ
YFZZFLZTCNBBNBZFNNLKZFSLKONWBLCCKJANKBPHGBZFNGNLOBLWSRDCSBZFNRJWLCBFDKNJWLWSWDTDSUWDTDSUOWDQBQFLZBYDJWYZ
DFLGGNWZDLWUTDSUTNBJSNBZFNRDKCDKWKLYBDRYKDQJWYDCSJZFJWODRSNLWEDKJLKZUJNANWZFJWODRDCSSNLWEDKJLKZUZFNRLZFN
KQNWNANKRDHWSJZFJWODRSNLWEDKJLKZU""")
'''
# print('Time for 500 Generations: %d' % (time.perf_counter() - start))
