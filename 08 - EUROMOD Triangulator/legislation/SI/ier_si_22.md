

 


 
 
 
MIKROSIMULACIJSKI MODEL 
DAVKOV IN SOCIALNIH 
TRANSFERJEV SLOMOD 
 
 
 
Barbara Kalar 
Nataša Kump 
Marko Ogorevc 
Klemen Koman 
Damjan Kavaš 
 
 
 
 
 
Ljubljana, 2023 
 


2 
EkonomIERa  
03-2023 
MIKROSIMULACIJSKI MODEL DAVKOV IN SOCIALNIH TRANSFERJEV 
SLOMOD 
Barbara Kalar, Nataša Kump, Marko Ogorevc, Klemen Koman, Damjan Kavaš 
© 2023 Inštitut za ekonomska raziskovanja, Ljubljana 
Vse pravice pridržane. Nobenega dela tega gradiva se brez predhodnega 
privoljenja lastnikov avtorskih pravic ne sme reproducirati, shranjevati ali 
prepisovati v katerikoli obliki oziroma na katerikoli način, bodisi elektronsko, 
mehansko, s fotokopiranjem, snemanjem ali kako drugače. 
 
Izdal in založil: Inštitut za ekonomska raziskovanja, Ljubljana 
Oblikovanje naslovnice: Solos d.o.o., Ljubljana 
Tisk: Solos d.o.o., Ljubljana 
Naklada: 100 izvodov 
Knjižna zbirka: EkonomIERa, ISSN 2630-2896 
Urednik: dr. Boris Majcen 
Področje: Socialna vključenost in pokojnine 
 
Monografija je nastala v okviru operacije »Nadgradnja analitičnih modelov na 
področju pokojninskega sistema« (št. pogodbe C2611-18-783107 med IER in 
MDDSZ). Naložbo sofinancirata Republika Slovenija in Evropska unija iz 
Evropskega socialnega sklada. 
 
CIP - Kataložni zapis o publikaciji 
Narodna in univerzitetna knjižnica, Ljubljana 
 
336.22:519.862(497.4) 
364-646.2:519.862(497.4) 
 
    MIKROSIMULACIJSKI model davkov in socialnih transferjev SLOmod / 
Barbara Kalar ... [et al.]. - Ljubljana : Inštitut za ekonomska 
raziskovanja, 2023. - (EkonomIERa, ISSN 2630-2896) 
 
ISBN 978-961-6906-73-9 
COBISS.SI-ID 145512707 
 


 
i 
KAZALO VSEBINE 
PREDGOVOR ....................................................................................................... 1 
1 
UVOD........................................................................................................... 3 
2 
KRATEK PREGLED DAVČNEGA SISTEMA IN SISTEMA SOCIALNIH 
TRANSFERJEV V SLOVENIJI ....................................................................... 5 
3 
METODOLOŠKA POJASNILA ..................................................................... 9 
3.1 
Priprava podatkov .................................................................................................... 10 
3.1.1 
Socioekonomski in demografski podatki ............................................. 15 
3.1.2 
Dohodki, nadomestila, transferji .............................................................. 22 
3.1.3 
Število mesecev prejemanja dohodka, nadomestila, transferja ... 33 
3.1.4 
Premoženje ....................................................................................................... 35 
4 
UPORABA MIKROSIMULACIJSKEGA MODELA SLOMOD ...................... 37 
5 
VALIDACIJA MODELA SLOMOD ............................................................. 43 
5.1 
Dohodek, dohodnina in socialni prispevki ..................................................... 43 
5.2 
Socialni transferji in nadomestila ....................................................................... 46 
6 
SIMULACIJE SCENARIJEV ........................................................................ 57 
6.1 
Scenarij 1: Minimalni dohodek ............................................................................ 58 
6.2 
Scenarij 2: Univerzalni otroški dodatek............................................................ 65 
6.3 
Scenarij 3: Enotna dohodninska stopnja ......................................................... 72 
6.4 
Scenarij 4: Neupoštevanje premoženja po ZUPJS ....................................... 79 
6.5 
Porazdelitev po dohodkovnih razredih ........................................................... 85 
7 
ZAKLJUČEK ............................................................................................... 95 
LITERATURA IN VIRI ........................................................................................ 99 
PRILOGE .......................................................................................................... 101 
KAZALO SLIK .................................................................................................. 117 
KAZALO TABEL ............................................................................................... 119 
 


ii 
EkonomIERa  
03-2023 
SEZNAM UPORABLJENIH KRATIC 
EU-SILC 
European Union Statistics on Income and Living Conditions 
IS CSD 
Informacijski sistem centrov za socialno delo 
ISER 
Institute for Social and Economic Research  
JPRS 
Javni sklad Republike Slovenije 
JRC 
Joint Research Centre (Skupno raziskovalno središče) 
JŠRIP 
Javni štipendijski, razvojni, invalidski in preživninski sklad Republike 
Slovenije 
MDDSZ 
Ministrstvo za delo, družino socialne zadeve in enake možnosti  
MIZŠ 
Ministrstvo za izobraževanje, znanost in šport 
MSM 
Mikrosimulacijski model 
RBO 
Register brezposelnih oseb 
SRDAP 
Statistični register delovno aktivnega prebivalstva 
SURS 
Statistični urad Republike Slovenije 
SZ-1 
Stanovanjski zakon 
ZDoh 
Zakon o dohodnini 
ZPIZ 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije 
ZPIZ-2 
Zakon o pokojninskem in invalidskem zavarovanju 
ZRSZ 
Zavod Republike Slovenije za zaposlovanje  
ZSDP 
Zakon o starševskem varstvu in družinskih prejemkih 
ZSVarPre 
Zakon o socialno varstvenih prejemkih 
ZUJF 
Zakon o uravnoteženju javnih financ 


 
1 
PREDGOVOR 
Slovenija se podobno kot ostale razvite države sooča s številnimi izzivi, kot so 
demografske spremembe, zeleni prehod, digitalni prehod, pandemije (npr. covid-
19), tehnološke spremembe, deglobalizacija, naraščajoči javnofinančni izdatki, 
kriza zdravstvenega sistema, prehranska varnost, nestabilne gospodarske in 
politične razmere. Zato je pomembno, da se država Slovenija ustrezno odzove na 
opredeljene izzive, saj bo le tako dosegla cilje, ki si jih je zastavila v Strategiji 
razvoja Slovenije, predvsem doseganje osrednjega cilja Strategije, ki je doseči 
kakovostno življenje za vse.  
 
Negativne demografske napovedi pomenijo tveganja za javnofinančno vzdržnost 
pokojninskega sistema in višino pokojnin, za področje dolgotrajne oskrbe ter z 
vidika trga dela, za katerega sta značilna nizka delovna aktivnost starejših in pozen 
vstop mladih na trg dela. Pravočasen in ustrezen odziv zahteva sprejetje ustreznih 
strukturnih reform, ki so ključne za srednje in dolgoročno stabilnost javnih financ 
ter predvsem odgovarjajo na demografske izzive v Sloveniji. Pri tem pa ne smemo 
pozabiti na vpliv ostalih izzivov oziroma trendov, ki bodo imeli pomemben vpliv 
na sisteme socialne varnosti in na trg dela. Kot odgovor na izzive Slovenija 
pripravlja ključne strukturne reforme, kot so pokojninska in zdravstvena reforma 
ter reforma dolgotrajne oskrbe. Omenjene reforme so že leta vključene v 
nacionalne reformne programe, vključene pa so tudi v Načrt za okrevanje in 
odpornost. Starajoče se prebivalstvo pomeni velik pritisk tudi na trg dela in s tem 
na politiko zaposlovanja, podobno velja tudi za izobraževalni sistem. Nujnost 
sprejetja strukturnih reform poleg Evropske komisije izpostavlja tudi Organizacija 
za gospodarsko sodelovanje in razvoj. 
 
Priprava in izvedba strukturnih reform pa zahteva pripravo ustreznih strokovnih 
in analitičnih podlag, kar terja redno raziskovalno delo na razvoju in vzdrževanju 
tako baz podatkov kot tudi modelskih orodij, s čimer je mogoče oceniti posledice 
ukrepov ekonomske politike. Republika Slovenija in Evropska unija iz Evropskega 
socialnega sklada zato sofinancirata operacijo Nadgradnja analitičnih modelov na 
področju pokojninskega sistema, v okviru katere poteka razvoj in nadgradnja 
mikrosimulacijskih orodij, ki omogočajo hitro in učinkovito odzivnost na strateške 
in tudi tekoče potrebe nosilcev ekonomske politike na pomembnih področjih 
delovanja slovenske vlade: davčnega sistema in prispevkov za socialno varnost, 


2 
EkonomIERa  
03-2023 
pokojninskega sistema, socialnih transferjev in trga dela. Kot bistven rezultat 
operacije so bili realizirani trije mikrosimulacijski modeli: mikrosimulacijski model 
trga dela, mikrosimulacijski model davkov in socialnih transferjev ter dinamični 
pokojninski mikrosimulacijski model. Z namenom prikaza razvoja in osnov 
delovanja posameznega modela ter njegove praktične uporabe smo za vsak 
model pripravili samostojno strokovno monografijo; v pričujoči monografiji 
prikazujemo razvoj in uporabno vrednost mikrosimulacijskega modela davkov in 
socialnih transferjev SLOmod. 
 
 
 


 
3 
1 
UVOD 
Mikrosimulacijski model davkov in socialnih transferjev predstavlja enega od 
temeljnih orodij, potrebnih ne samo za oceno posledic morebitnih reform in v 
okviru njih sprememb na področju socialnih transferjev, temveč tudi za tekočo 
uporabo ocen posledic posameznih popravkov določenega socialnega transferja 
ali davka. Vsaka načrtovana sprememba davčnega sistema ali sistema socialne 
varnosti namreč zahteva primeren pristop k vrednotenju učinkov teh sprememb. 
Sprašujemo se, kdo bo na slabšem in kdo na boljšem ter kakšni bodo neto učinki 
predvidenih sprememb na proračun. Mikrosimulacijski model tako zajema 
celoten socioekonomski spekter prebivalstva, saj simulira učinke sprememb na 
vse posameznike v reprezentativnem vzorcu v določenem trenutku. Simulira 
neposredne davke, socialne prispevke in transferje z neposredno prevedbo 
zakonodaje v kodo modela. 
Univerza v Essexu je prva razvila statični mikrosimulacijski model EUROMOD, ki 
na primerljiv način omogoča izračune politik davkov in socialnih transferjev za 
posamezne države EU kot tudi na ravni celotne EU. Od leta 2021 dalje je razvoj in 
upravljanje modela prevzelo Skupno raziskovalno središče (JRC) Evropske 
komisije v sodelovanju z Eurostatom in predstavniki nacionalnih skupin 
strokovnjakov. Ključne prednosti modela EUROMOD so usklajeni vhodni 
mikropodatki (EU-SILC, podatkih o dohodkih in življenjskih pogojih) in simulacije 
politik za vse vključene države na predpisan način. Programsko orodje oziroma 
platforma EUROMOD je zelo fleksibilna in omogoča prilagajanje modela drugim 
virom podatkov. V posameznih državah obstaja velik interes uporabe 
administrativnih podatkov na platformi EUROMOD, saj se na tak način pri 
modeliranju politik davkov in socialnih transferjev lahko uporabi podatke, ki v EU-
SILC niso na razpolago, hkrati pa se simulacije izvajajo na veliko večjih vzorcih. 
Tako nekatere države članice (npr. Grčija, Belgija, Litva, Slovaška in Romunija) že 
poskušajo prilagoditi model EUROMOD tudi za uporabo na administrativnih 
podatkih (EUROMOD, 2023). V Grčiji so na primer oblikovali dve dodatni vhodni 
bazi podatkov na podlagi podrobnejših dohodninskih podatkov, BELMOD pa je 
primer belgijskega mikrosimulacijskega modela, s katerim želijo razširiti model 
EUROMOD, da bo lahko deloval tako na EU-SILC kot administrativnih podatkih. 
Slednje poskušajo doseči z vgradnjo obstoječega mikrosimulacijskega modela 
MIMOSIS, ki temelji na administrativnih podatkih, v EUROMOD. 


4 
EkonomIERa  
03-2023 
V 
okviru 
pričujočega 
dela 
predstavljamo 
izgradnjo 
in 
uporabnost 
mikrosimulacijskega modela davkov in socialnih transferjev SLOmod, ki je 
prilagojen slovenskemu sistemu. SLOmod temelji na platformi EUROMOD in 
uporabi administrativnih podatkov. Pretekli modeli davkov in socialnih transferjev 
so bili pripravljeni s programskim orodjem Stata, uporabniku pa je bil na voljo 
uporabniški vmesnik. SLOmod predstavlja nov korak v razvoju mikrosimulacijskih 
modelov davkov in socialnih transferjev, saj ima platforma EUROMOD na voljo 
uporabniški vmesnik, obsežen meni pomoči in več orodij, ki uporabniku 
omogočajo izpis agregatnih rezultatov. Programska platforma EUROMOD je 
odprtokodna 
in 
dostopna 
na 
spletni 
strani 
JRC 
(https://euromod-
web.jrc.ec.europa.eu/sites/default/files/inline-files/EUROMOD_installer_64bit 
_v3.5.8.zip). 
Vhodna baza mikropodatkov je oblikovana na podlagi vzorca slovenske 
populacije, oblikovanega s povezovanjem baz podatkov iz različnih virov in 
omogoča simuliranje statičnih učinkov ukrepov na področju davkov in socialnih 
transferjev 
na 
ravni 
posameznika 
oziroma 
gospodinjstva. 
Prednost 
mikrosimulacijskega modela je tudi v tem, da lahko ocenimo posledice uvedene 
spremembe pri posamezni politiki na ostale politike. Na primer, ob uvedbi 
spremembe dohodninske stopnje lahko poleg vpliva na dohodnino ocenimo tudi 
neposredni vpliv uvedene spremembe na število prejemnikov in višino 
posameznih socialnih transferjev. Podobno bi lahko ob uvedbi spremembe 
otroškega dodatka ocenili spremembe tudi pri številu upravičencev in prejetih 
zneskih pravic, na katere vpliva višina prejetega otroškega dodatka (npr. denarna 
socialna pomoč, državna štipendija, subvencija plačila vrtca in druge).  
V naslednjem poglavju podajamo kratek opis davčnega sistema in sistema 
socialnih transferjev v Sloveniji. V tretjem poglavju sledijo metodološka pojasnila, 
kjer opisujemo podatke, na katerih temelji SLOmod, omejitve podatkov in 
predpostavke, ki smo jih sprejeli v fazi priprave podatkov. V četrtem poglavju 
predstavimo model SLOmod. Sledi validacija modela SLOmod, kjer na podlagi 
primerjave rezultatov simulacij z zunanjimi statistikami preverjamo uspešnost 
modela SLOmod za izračun davkov in socialnih transferjev. V šestem poglavju na 
podlagi različnih simulacij prikažemo, kakšne spremembe politik je mogoče 
analizirati v modelu. V zadnjem poglavju na kratko povzamemo delo in opišemo 
tudi načrte razširitve oziroma nadgradnje modela.  
 


 
5 
2 
KRATEK PREGLED DAVČNEGA SISTEMA IN 
SISTEMA SOCIALNIH TRANSFERJEV V SLOVENIJI  
Slovenija si kot socialna država prizadeva za zagotavljanje socialne varnosti in 
enakosti svojih prebivalcev tudi z izvajanjem davčne in socialne politike. Kako ima 
država oblikovan sistem davkov in sistem socialnih prispevkov, igra pomembno 
vlogo pri doseganju ciljev socialne države. V nadaljevanju na kratko povzemamo 
lastnosti davčnega in socialnega sistema v Sloveniji.   
Obveznost plačila dohodnine v Sloveniji temelji na letnem dohodku, med letom 
pa se plačuje akontacija dohodnine. V letno davčno osnovo se vštevajo: dohodek 
iz zaposlitve, dohodek iz dejavnosti (če se davčna osnova ugotavlja na podlagi 
dejanskih prihodkov in odhodkov), dohodek iz osnovne kmetijske in gozdarske 
dejavnosti, dohodek iz prenosa premoženjske pravice in drugi dohodki. Dohodek 
iz dejavnosti (če se davčna osnova ugotavlja z upoštevanjem normiranih 
odhodkov), dohodek iz kapitala (obresti, dividende, dobiček iz kapitala) ter 
dohodek iz oddajanja premoženj v najem pa so dohodki, ki se ne vštevajo v letno 
davčno osnovo in od katerih se dohodnina plačuje cedularno, kar pomeni, da je 
plačani davek dokončen.   
Večina socialnih transferjev je odvisna od neto letnega dohodka. Izjeme so 
denarna socialna pomoč, varstveni dodatek in subvencija najemnine, pri katerih 
se za upravičenost do pravice upošteva trimesečni dohodek pred mesecem 
vložitve vloge za uveljavljanje pravic iz javnih sredstev. Socialni transferji se 
izplačujejo mesečno, izjemi sta dodatek za veliko družino, ki se izplačuje enkrat 
letno, in pomoč ob rojstvu otroka, ki se izplačuje le ob rojstvu otroka.  
Davčne lestvice, višine olajšav, meje dohodkovnih razredov za socialne transferje 
in zneski socialnih transferjev se usklajujejo, a ni enotnega režima. Zneski 
družinskih transferjev in osnovni znesek minimalnega dohodka, ki je osnova za 
določitev minimalnega dohodka pri presojanju upravičenosti do denarne socialne 
pomoči, varstvenega dodatka in subvencije najemnine, se uskladijo enkrat letno 
(marca) z indeksom cen življenjskih potrebščin v preteklem letu. Meje dohodkov 
za ugotavljanje upravičenosti do letnih pravic (otroški dodatek, državna 
štipendija, znižano plačilo vrtca in subvencionirana šolska prehrana) se zvišujejo 
enkrat letno (januarja) skladno z indeksom cen življenjskih potrebščin v prejšnjem 
letu (od leta 2018 dalje). Skladno z zakonom, ki ureja pokojnine (ZPIZ-2), je 


6 
EkonomIERa  
03-2023 
določeno, da se redna uskladitev pokojnin izvede enkrat letno (februarja) na 
podlagi rasti povprečne mesečne bruto plače in povprečne rasti cen življenjskih 
potrebščin v skladu z naslednjo formulo: višina pokojnin se uskladi za 60 % rasti 
povprečne bruto plače v preteklem letu v primerjavi s povprečno bruto plačo leto 
pred tem in 40 % povprečne rasti cen življenjskih potrebščin v preteklem letu v 
primerjavi z letom poprej. Zneski neto letnih davčnih osnov in davčne olajšave se 
vsako leto najkasneje decembra uskladijo na podlagi koeficienta, določenega s 
strani ministra za finance. Koeficient se (od leta 2022 dalje) določi najmanj v višini 
50 % rasti povprečnih mesečnih plač zaposlenih v Sloveniji za mesec junij 
tekočega leta v primerjavi z mesecem junijem prejšnjega leta, če je rast pozitivna. 
Poleg vseh naštetih razlik prihaja do spremenjenega načina usklajevanja tudi 
zaradi izrednih uskladitev in sprememb zakonov. 
Večji vpliv na davčno politiko in socialne transferje so imeli tudi začasno uvedeni 
ukrepi in interventni zakoni v času zadnjih globalnih kriz, finančne krize v letih 
2008–2009 in pandemije covid-19 v letih 2020–2021. Maja 2012 je bil sprejet 
Zakon o uravnoteženju financ (ZUJF) za zagotovitev vzdržnih javnih financ in za 
zmanjšanje izdatkov proračuna. Zakon je zaostril pogoje upravičenosti do 
posameznih pravic in tudi zneske transferjev. Nekateri ukrepi so bili trajni, drugi 
začasni. Ukrepi, ki so urejali družinske transferje (starševsko nadomestilo, otroški 
dodatek, pomoč ob rojstvu otroka, dodatek za veliko družino, starševski dodatek 
in državna štipendija), so skladno z zakonom veljali do vključno leta, ki sledi letu, 
v katerem gospodarska rast preseže 2,5 odstotka bruto domačega proizvoda 
in/ali rast stopnje delovne aktivnosti v starostni skupini od 20 do 64 let preseže 
1,3 odstotne točke. Tako so bili nekateri ukrepi, ki urejajo družinske transferje, 
delno odpravljeni v letih 2016 in 2018 (za otroški dodatek), večina pa jih je bila 
odpravljena šele januarja 2019 (za starševsko nadomestilo, očetovski dopust, 
dodatek za veliko družino in državno štipendijo). 
S pojavom pandemije covid-19 so bili v začetku leta 2020 sprejeti ukrepi za 
ublažitev posledic krize. Skupno je bilo sprejetih deset protikoronskih paketov 
ukrepov v letih 2020 in 2021, ki so bila predvsem usmerjena v ukrepe za urejanje 
trga dela in ohranitev delovnih mest, pomoč podjetjem in ukrepe za pomoč 
različnim skupinam prebivalstva, predvsem ranljivim skupinam (upokojencem, 
prejemnikom denarne socialne pomoči, varstvenega dodatka in invalidskega 
nadomestila ter študentom). Slednje je bilo izvedeno z nadomestili plač, 
subvencioniranjem krajšega delovnega časa, enkratnimi solidarnostnimi izplačili 


 
7 
ranljivim skupinam in z dodatki oziroma povečanimi zneski nekaterih pravic, kot 
so dodatek za veliko družino, dodatek za nego otroka, pomoč ob rojstvu otroka, 
otroški dodatek. 
 
 
 


8 
EkonomIERa  
03-2023 
 
 


 
9 
3 
METODOLOŠKA POJASNILA 
Osnova za mikrosimulacijski model socialnih transferjev so podatki iz več virov, ki 
se nanašajo na leto 2017 in ki jih je anonimiziral SURS. Podatki obsegajo: 
- 
identifikator osebe, identifikatorja gospodinjstva in družine, v katerega 
oziroma katero posameznik sodi, ter identifikatorje matere, očeta, 
zakonca; 
- 
demografske podatke o posameznikih: spol, starost, izobrazba, status 
aktivnosti, državljanstvo, občina prebivališča, zakonski stan; 
- 
podatke o lastništvu nepremičnine oziroma vrsti najema stanovanja 
(register nepremičnin in registrski popis najemnih stanovanj); 
- 
podatke o lastništvu, znamki, oznaki in datumu prve registracije vozil; 
- 
podatke, ki omogočajo identifikacijo študentov, ter podrobnejše podatke 
o štipendistih (na podlagi obrazcev ŠOL-ŠTIP in ŠOL-DIPL-TER, ki jih zbira 
SURS); 
- 
podatke iz Statističnega registra delovno aktivnega prebivalstva (SRDAP); 
- 
podatke Zavoda za pokojninsko in invalidsko zavarovanje Slovenije (ZPIZ) 
o zavarovancih (podatki o obdobjih zavarovanja in plačah); 
- 
podatke ZPIZ o upokojencih (podatki o upokojitvenem postopku in o 
osnovah za izračun pokojninske osnove); 
- 
podatke Zavoda Republike Slovenije za zaposlovanje (ZRSZ) o prijavah 
brezposelnih oseb (RBO) in denarnemu nadomestilu za brezposelnost; 
- 
podatke o dohodnini za leto 2017; 
- 
podatke o obračunu davčnih odtegljajev za dohodke iz delovnega 
razmerja, mesečni REK obrazci za leto 2017; 
- 
podatke o transferjih, ki jih izplačuje ZPIZ (nakazila uživalcem pravic pri 
ZPIZ); 
- 
podatke o socialnih transferjih iz informacijskega sistema centrov za 
socialno delo (IS CSD, ki ga sestavljata dva povezana sistema ISCSD in 
ISCSD2), ki jih izplačuje Ministrstvo za delo, družino, socialne zadeve in 
enake možnosti (MDDSZ), ter podatke o dohodkih in premoženju, ki jih 
vodi MDDSZ (skupno 14 baz podatkov iz IS CSD). 
Na podlagi povezovanja baz podatkov, potrebnih za opredelitev gospodinjstva, 
posameznih vrst dohodka, določenih oblik premoženja in socialnih transferjev, 
smo oblikovali vhodno bazo podatkov 388.908 posameznikov, ki živijo v 171.785 


10 
EkonomIERa  
03-2023 
gospodinjstvih, kar predstavlja 18,8 % slovenske populacije leta 2017. 
Reprezentativni vzorec slovenske populacije je pripravil SURS. Povezovanje baz 
podatkov, pripravo in oblikovanje končne baze podatkov, ki je osnova za izvajanje 
simulacij v mikrosimulacijskem modelu, smo izvedli z uporabo programskega 
paketa Stata. Mikrosimulacijski model davkov in socialni transferjev temelji na 
platformi EUROMOD in smo ga poimenovali SLOmod. 
V tem poročilu se sklicujemo na tri vrste podatkov:  
- 
mikropodatke iz povezanih baz, ki so podatki iz zgoraj navedenih baz 
podatkov in lastnih preračunov, na podlagi katerih ustvarimo vhodno 
bazo (za vzorčno populacijo); vhodna baza je osnova za simulacije v 
mikrosimulacijskem modelu; 
- 
podatke iz zunanjih virov, kot so: SURS, ZRSZ, ZPIZ, ministrstva ipd.; 
- 
rezultate simulacij, ki so pridobljeni na podlagi izračunov oziroma 
simulacij mikrosimulacijskega modela davkov in socialnih transferjev 
SLOmod. 
Kljub razpolaganju z zelo dobrimi in podrobnimi podatki smo se pri oblikovanju 
končne baze podatkov in izgradnji mikrosimulacijskega modela srečevali z 
določenimi omejitvami. V nadaljevanju podrobneje opisujemo, s katerimi 
omejitvami smo se srečevali, kako jih (poskušali) rešili, in predpostavke, ki smo jih 
sprejeli v fazah priprave podatkov in izgradnje mikrosimulacijskega modela 
SLOmod.  
3.1 Priprava podatkov 
Prva omejitev, s katero smo se srečali, je sestava oziroma tip gospodinjstva1. Kot 
tip gospodinjstva se pojavlja ne le veliko vrst gospodinjstev, ki so v obliki 
razširjenih družin (npr. stari starši, starši in otroci oziroma starši in odrasli otroci s 
svojimi družinami), ampak tudi kot skupinska in posebna gospodinjstva, ki lahko 
štejejo tudi do več sto članov (npr. študentski domovi, domovi za starejše občane, 
varne hiše in materinski domovi). Poleg tega je veliko enostarševskih družin 
(starša otrok sta prijavljena na različnih naslovih), celo družin oziroma 
gospodinjstev, ko otroci niso v rejništvu, a tudi ne živijo s starši, in enočlanskih 
 
1 Po definiciji SURS-a je tip gospodinjstva značilnost gospodinjstva glede na to, ali v njem živijo osebe 
v družinskih ali nedružinskih skupnostih. Glede na tip gospodinjstva SURS loči: zasebno, skupinsko in 
posebno gospodinjstvo. 


 
11 
gospodinjstev, ko sta partnerja prijavljena na različnih naslovih. Zato smo 
oblikovali pravila, s pomočjo katerih smo znotraj gospodinjstev oblikovali ožje 
družine 
ter 
predvsem 
povezali 
»razdrte« 
(enostarševske) 
družine 
in 
gospodinjstva2.  
Pomembne podatke o družinah in gospodinjstvih smo pridobili in na novo 
oblikovali z združevanjem baz: registrski popis prebivalstva (popis prebivalstva), 
centralni register prebivalstva (CRP), vloge prosilcev za pravice iz javnih sredstev 
(IS CSD baze - vloge) in osebe, ki so zajete pri pridobivanju pravic iz javnih 
sredstev (IS CSD baze - osebe). Medtem ko smo iz prvih dveh, popisa prebivalstva 
in CRP, pridobili podatke o družinah, gospodinjstvih, identifikatorje mame, očeta 
in zakonca, smo iz drugih dveh, IS CSD bazah o vlogah in osebah, pridobili 
podatke o odločbah (vlogah) za pravice iz javnih sredstev in osebah, ki se vežejo 
na posamezno odločbo. Najprej smo na podlagi podatka o položaju v družini (iz 
popisa prebivalstva) določili tudi identifikator partnerja oziroma partnerice ter 
tako razširili osnovni podatek o identifikatorju zakonca iz CRP. Slednje je 
prispevalo k temu, da smo lahko v naslednjih korakih oblikovali boljše 
predpostavke za oblikovanje ožjih družin in povezovanje »razdrtih« družin. S 
podatki o osebah, ki so skupaj pisane na odločbi za uveljavljanje pravic iz javnih 
sredstev, pa smo lahko oblikovali družine in gospodinjstva, ki v popisu 
prebivalstva niso registrirane kot ena družina oziroma gospodinjstvo (npr. starša 
otrok, ki imata registrirano stalno prebivališče na različnih naslovih, ali odrasli 
otroci s partnerjem oziroma partnerico, ki so še vedno registrirani na svojem 
prejšnjem stalnem naslovu). Osnovne predpostavke pri oblikovanju ožjih družin 
in povezovanju »razdrtih« družin so: 
- 
osebe, mlajše od 26 let, iz skupinskih/posebnih gospodinjstev pridružimo 
družini in gospodinjstvu mame, medtem ko preostale osebe iz 
skupinskih/posebnih 
gospodinjstev 
smatramo 
kot 
samostojno, 
enočlansko gospodinjstvo oziroma enočlansko družino; 
- 
mame, ki niso v skupinskem ali posebnem gospodinjstvu in ki živijo v 
drugem gospodinjstvu kot njeni otroci (mlajši od 18 let, ki ne živijo v 
skupinskem ali posebnem gospodinjstvu) brez partnerja ali s partnerjem, 
ki je oče otroka oziroma otrok, pridružimo družini in gospodinjstvu otrok; 
 
2 Zavedamo se, da smo na tak način v družine povezali preveč družin, a je napaka manjša, kot če tega 
ne bi storili. Na to kaže primerjava sestave gospodinjstev/družin po registrskih podatkih in na podlagi 
mikropodatkov. 


12 
EkonomIERa  
03-2023 
- 
v primerih, ko otroci, mlajši od 18 let, živijo brez mame, a s svojim očetom, 
ki ima novo partnerico, mam otrok ne prestavljamo v družino in 
gospodinjstvo otrok; 
- 
v primerih, ko otroci, mlajši od 18 let in različnih mam, živijo z očetom, ki 
nima partnerice, združimo kot družino in gospodinjstvo otroke, očeta in 
mamo najmlajšega otroka, če ta nima drugega partnerja (predvidevamo, 
da ima oče otroke iz dveh (ali več) razmerij in živi z žensko, s katero imata 
skupaj mlajše oziroma najmlajšega otroka); 
- 
očete dojenčkov (otroci, mlajši od 1 leta), ki z dojenčkom niso registrirani 
skupaj kot družina in gospodinjstvo, pa tudi niso del skupinskega ali 
posebnega gospodinjstva ter v svoji družini in gospodinjstvu nimajo 
otrok niti partnerice, pridružimo družini in gospodinjstvu dojenčka, če 
dojenček ni iz skupinskega ali posebnega gospodinjstva ter njegova 
mama nima drugega partnerja; 
- 
očete, če v svoji družini in gospodinjstvu nimajo otrok, pridružimo družini 
in gospodinjstvu otrok (mlajši od 18 let ali stari do 26 let, ki se šolajo), s 
katerimi so skupaj na vlogi za uveljavljanje pravic iz javnih sredstev; 
- 
otroke, mlajše od 18 let, ki živijo brez mame in očeta ter niso v rejništvu, 
pridružimo družini in gospodinjstvu mame; 
- 
otrok iz rejništva ne prestavljamo; 
- 
v primerih, ko sta moški in ženska partnerja, a ne živita skupaj in 
partnerice ne živijo v skupinskem ali posebnem gospodinjstvu, partnerji 
pa živijo sami, te pridružimo družini in gospodinjstvu partnerice; 
- 
osebe, ki živijo same, a imajo parterja oziroma partnerico, ki prav tako živi 
sam oziroma sama, združimo v eno družino in gospodinjstvo; 
- 
osebe, ki so same oddale vlogo za uveljavljanje pravice do denarne 
socialne pomoči ali varstvenega dodatka, smatramo kot samostojno 
družino in gospodinjstvo. 
Pojavljali so se tudi primeri, ko osebe niso imele pripisanih identifikatorjev družine 
ali staršev v podatkih (popis prebivalstva in CRP). V prvem primeru smo za osebe, 
ki niso imele pripisanega identifikatorja družine v podatkih, ustvarili nov, svojstven 
identifikator družine. Nato smo v gospodinjstvih tudi poiskali sorojence po mami, 
mlajše od 26 let, in jim v primeru, da v podatkih niso imeli pripisanega 
identifikatorja družine, pripisali identifikator družine sorojenca (iz podatkov, če ga 
je imel, oziroma novo ustvarjenega, če v podatkih ni imel pripisanega 


 
13 
identifikatorja družine). V drugem primeru, ko so bili neznani identifikatorji 
staršev, pa smo na podlagi podatka o razmerju do referenčne osebe3 in/ali 
podatka o položaju v družini4 (popis prebivalstva) določili, za kakšno sorodstveno 
razmerje gre med osebami v gospodinjstvu. Na podlagi tega smo lahko določili 
otroke in starše ter otrokom pripisali identifikatorje staršev.  
Naknadno smo po oblikovanju vzorca izločili še: 
- 
otroke, ki živijo sami (starši niso bili zajeti v vzorec); 
- 
gospodinjstva brez polnoletnega člana. 
Ker je tip gospodinjstva oziroma družine zelo pomemben podatek pri simuliranju 
upravičenosti do socialnih transferjev, ocenjujemo, da je kljub sprejetju nekaj 
arbitrarnih odločitev napaka manjša, kot bi bila, če bi gospodinjstva in družine 
obravnavali, kot so določena le na podlagi registrskih podatkov. Da gre za vidne 
razlike med simuliranim in uradnim številom gospodinjstev in družin nakazujejo 
tudi podatki prikazani v tabeli 1. Pri tem je treba opozoriti, da se uradni opredelitvi 
gospodinjstva in družine z otroki nekoliko razlikujeta od opredelitev, ki smo ju 
sprejeli pri obravnavi podatkov.  
Po uradni opredelitvi SURS so gospodinjstva ločena na zasebna, skupinska in 
posebna 
gospodinjstva. 
Zasebna 
gospodinjstva 
sestavljajo 
enočlanska, 
veččlanska družinska in veččlanska nedružinska zasebna gospodinjstva (SURS, 
2022a). Po naši opredelitvi pa sodijo v gospodinjstva tako zasebna kot tudi 
skupinska in posebna gospodinjstva, pri čemer za slednja dva tipa sprejmemo še 
nekatere predpostavke, opisane v začetku tega poglavja (osebe, mlajše od 26 let, 
iz skupinskih/posebnih gospodinjstev prestavimo v gospodinjstva in družine 
staršev, preostale osebe iz skupinskih/posebnih gospodinjstev pa smatramo kot 
samostojno, enočlansko gospodinjstvo oziroma enočlansko družino). Pri tem je 
še treba opozoriti na to, da smo pred premikanjem oseb iz skupinskih/posebnih 
gospodinjstev na podlagi starosti oseb poskušali določiti, za kakšno obliko 
skupinskega/posebnega gospodinjstva gre. Slednje smo presojali glede na to, ali 
v skupinskem/posebnem gospodinjstvu, kjer prebiva več kot 20 oseb, 
prevladujejo mladi ali starejši.  
 
3 (00) referenčna oseba gospodinjstva, (01) mož/žena, (02) zunajzakonski partner/zunajzakonska 
partnerica, (03) sin/hči, (05) oče/mati itd. 
4 (01) starš/zakonec, (02) otrok v zakonski skupnosti, (03) zunajzakonski partner, (04) otrok v 
zunajzakonski skupnosti itd. 


14 
EkonomIERa  
03-2023 
Tako smo za osebe predpostavili, da živijo: 
- 
v študentskem domu (oziroma ustanovi, kjer prevladujejo mladi, mlajši 
od 27 let); 
- 
v domu za starostnike (oziroma ustanovi, kjer prevladujejo starejši, stari 
več kot 60 let); 
- 
drugje. 
Tabela 1: Gospodinjstva in družine glede na simulirane in zunanje podatke, 
leti 2017/18 
 
Simulirani rezultati 
Zunanji podatki 
Gospodinjstva 
912.178 
825.195 od tega 
zasebna: 824.618 
skupinska: 497 
posebna: 80 
Povprečna velikost gospodinjstva 
2,26 
2,5** 
Enočlansko gospodinjstvo  
368.227 
269.898 
Družine z otroki 
269.445* 
427.540*** 
Povprečno št. otrok v družini z otroki 
1,62 
1,56 
Opombe: * Otroci, mlajši od 18 let oziroma mlajši od 26 let, če se šolajo in nimajo svoje družine 
oziroma ne živijo v zunajzakonski skupnosti; ** Upoštevajo se zasebna gospodinjstva. *** Starost otrok 
ni omejena, vendar le-ti nimajo svoje družine oziroma ne živijo v zunajzakonski skupnosti. 
Vir: SURS in lastni izračuni. 
Naslednja omejitev, s katero smo se srečali, so različne vrednosti istega podatka. 
Pri združevanju večjega števila baz podatkov pridobimo iste podatke, predvsem 
o socialno-ekonomskem položaju oseb, ki se lahko med bazami razlikujejo. Tako 
smo podatke o socialno-ekonomskem statusu posameznika vsaki osebi pripisali 
na osnovi prioritetnega vrstnega reda in hierarhije vseh uporabljenih virov 
podatkov. Pri določitvi vzorca smo prednostno upoštevali osebe iz popisa 
prebivalstva (oseb iz drugih baz, ki se niso združile s popisom prebivalstva, nismo 
upoštevali), medtem ko smo pri urejanju podatkov sledili hierarhiji virov. Na 
primer, status (mesečne) aktivnosti smo posameznikom pripisali na podlagi 
podatkov o delovni aktivnosti (SRDAP), katerim sledijo podatki o brezposelnih 
(RBO), podatki ZPIZ o upokojencih ter podatki o študentih. Za prejemnike 
socialnih transferjev smo ohranili podatke za posameznika, ki se vežejo na 
njegovo zadnjo odobreno vlogo. Namreč, posameznik oziroma družina lahko 
med letom odda več vlog za pravice. Podatki, ki se vežejo na vlogo, kot so število 
(vzdrževanih) članov, položaj v družini, izobrazba, aktivnost, dohodki, premoženje 


 
15 
itd., pa se lahko med vlogami razlikujejo, saj se le-ti lahko posamezniku med 
letom spremenijo.  
Dodatni razlog za razhajanja v vrednosti istega podatka med bazami je tudi v tem, 
da se baze nanašajo na različne datume oziroma obdobja: na primer, popis 
prebivalstva se nanaša na dan 1. 1. 2018, CRP na dan 1. 2. 2018, podatki iz SRDAP 
in RBO so na mesečni ravni, podatki o statusu študentov se nanašajo na študijski 
leti 2016/17 in 2017/18, podatki o prejemnikih socialnih transferjev se nanašajo 
na podatke iz odločb za pravice v letu 2017 ipd. V nadaljevanju tako podajamo 
podrobnejši opisi urejanja nekaterih pomembnejših podatkov.   
3.1.1 
Socioekonomski in demografski podatki 
Podatke o socioekonomskem položaju (status aktivnosti) posameznika smo 
pridobili iz popisa prebivalstva, ki je za posameznika veljal na dan 1. 1. 2018. Z 
združevanjem različnih baz (SRDAP, RBO, podatki ZPIZ o upokojitvenem 
postopku, podatki o študentih) smo lahko prišli do podrobnejšega podatka o 
socialno-ekonomskem položaju posameznika, ki se nanaša na posamezen mesec 
v letu 2017. Posameznikom smo za vsak mesec v letu 2017 pripisali mesečno 
aktivnost po naslednjem vrstnem redu: zaposlen, brezposeln, upokojenec, 
študent/dijak/učenec ali druga neaktivna oseba, glede na to, ali je bila oseba 
zavedena v posamezni bazi. Vrstni red določanja statusa aktivnosti od zaposlene 
do neaktivne osebe smo oblikovali, ker lahko prihaja do neskladij med bazami 
(npr. oseba je bila lahko isti mesec registrirana kot zaposlena in brezposelna, do 
česar najverjetneje prihaja, ker se status osebe spremeni sredi meseca; podatek o 
statusu študenta imamo za posamezno šolsko leto, ki pa se lahko spremeni med 
letom – študent zaključi študij in se zaposli, postane brezposelna oseba/iskalec 
zaposlitve ali neaktivna oseba). Status brezposelne osebe tako pripišemo 
posamezniku kot mesečno aktivnost, če oseba za isti mesec še ni imela 
določenega statusa zaposlene osebe (ni bila zavedena v bazi SRDAP). Status 
študenta oziroma študenta/dijaka/učenca pripišemo osebam za posamezni 
mesec, če so imele status študenta v letu 20175 in v posameznem mesecu niso 
bile zavedene v bazah SRDAP, RBO ali ZPIS bazi o upokojitvenem postopku. 
Dodatno smo zaposlenim določili status aktivnosti glede na obliko (zaposlen, 
 
5 Status študenta v mesecih januar–september smo pripisali osebam, ki so imele status študenta v 
študijskem letu 2016/2017, in status študenta v mesecih oktober–december tistim, ki so imele status 
študenta v študijskem letu 2017/2018. 


16 
EkonomIERa  
03-2023 
samozaposlen ali kmet) in delovni čas ((samo)zaposlitev za polni ali krajši delovni 
čas). Brezposelne smo ločili na prejemnike denarnega nadomestila in tiste, ki ga 
ne prejemajo, v okviru statusa študenta/dijaka/učenca pa smo upoštevali: a) vse 
učence in dijake, stare do 15 let, ki so bili v izobraževanju, b) mladostnike do 
vključno 18. leta, ki niso bili zaposleni ali v evidenci brezposelnih oseb ter c) mlade 
od 18. leta dalje, če so bili evidentirani v bazi s podatki o študentih in ne v bazah 
SRDAP ali RBO. Status druge neaktivne osebe smo pripisali posameznikom za 
mesece, ko niso bili registrirani v nobeni izmed omenjenih baz in jim tako nismo 
mogli pripisati nobenega aktivnega statusa.  
Status mesečne aktivnosti smo poskušali še dodatno izboljšati z upoštevanjem 
dohodkov, ki jih je posameznik prejel v letu 2017. Tako smo osebam, katerim smo 
pripisali status neaktivne osebe, a so prejemale pokojnino in dohodek iz 
zaposlitve oziroma samozaposlitve, ki je bil višji od pokojnine, popravili mesečne 
aktivnosti v status zaposlen za krajši delovni čas oziroma samozaposlen za krajši 
delovni čas. Osebam, katerim smo pripisali status neaktivne osebe skozi celo leto, 
a je oseba prejemala dohodek iz zaposlitve iz tujine ali pa dohodek iz zaposlitve 
doma in tujine, smo popravili vse mesečne statuse aktivnosti v zaposlen za polni 
delovni čas. Preden smo spremenil mesečni status aktivnosti, smo v primeru 
prejemanja dohodka iz zaposlitve doma in tujine upoštevali še dodatni pogoj, da 
mora biti oseba v popisu prebivalstva registrirana kot zaposlena oseba. Treba je 
še omeniti, da statusa upokojenca nismo pripisali mlajšim od 60 let, ki prejemajo 
družinsko pokojnino. 
Na podlagi novo oblikovanih podatkov o mesečnih aktivnosti smo oblikovali 
podatek o ekonomskem statusu (les)6 posameznika v 3. obdobjih v letu 2017: 
januar (les01), junij (les06) in december (les12). Tako smo posameznike razporedili 
trikrat (za mesec januar, junij in december) v devet skupin glede na status 
mesečne aktivnosti v posameznem mesecu (januarju, juniju in decembru):  
0. otroci v vrtcu in mlajši – vsi otroci, ki so vključeni v predšolsko vzgojo, in 
vsi otroci, ki so mlajši od 6 let in za njih nimamo podatka niti o tem, ali so 
vključeni v vrtec, niti, ali so v domačem varstvu, medtem ko smo 6-letnim 
otrokom pripisali ta status le za mesec januar (les01=0) in junij (les06=0), 
če smo na podlagi veljavnih vlog (ne zadnje, a še vedno veljavne v letu 
 
6 V oklepajih so napisana imena spremenljivk, ki so uporabljena v vhodni bazi podatkov, pripravljenih 
za uporabo modela EUROMOD, ki je podrobneje opisan v naslednjem poglavju 0.  


 
17 
2017) za uveljavljanje pravic iz javnih sredstev lahko določili, da se je za 
tega šestletnika odločalo tudi o znižanem plačilu vrtca7;  
1. kmetje – osebe z mesečnim statusom aktivnosti kmet; 
2. samozaposleni – osebe z mesečnim statusom aktivnosti samozaposlen za 
polni ali krajši delovni čas; 
3. zaposleni – osebe z mesečnim statusom aktivnosti zaposlen za polni ali 
krajši delovni čas; 
4. upokojenci – osebe z mesečnim statusom aktivnosti upokojenec; 
5. brezposelni – osebe z mesečnim statusom aktivnosti brezposelni ne 
glede na to, ali je prejemnik denarnega nadomestila oziroma pomoči na 
ZRSZ ali ne; 
6. študenti/dijaki/učenci – osebe z mesečnim statusom aktivnosti 
študenta/dijaka/učenca; 
7. neaktivni – osebe z mesečnim statusom aktivnosti druga neaktivna oseba; 
8. bolni in invalidni – osebe, stare 29–59 let, ki prejemajo pokojnino in 
katerih mesečni status aktivnosti ni (samo)zaposlen za polni ali krajši 
delovni čas, ali brezposelni, ne glede na to, ali je prejemnik denarnega 
nadomestila oziroma pomoči na ZRSZ ali ne, ter osebe, katerih status 
mesečne aktivnosti je upokojenec in prejemajo invalidsko pokojnino. 
V spodnji tabeli 2 prikazujemo porazdelitev oseb glede na ekonomski status. Pri 
tem moramo biti previdni pri primerjavi, saj vsi ekonomski statusi niso popolnoma 
primerljivi med simuliranimi rezultati in zunanjimi podatki. 
 
 
 
7 Kot je pojasnjeno v začetku tega poglavja, smo za upravičence pravic iz javnih sredstev ohranili 
podatke za posameznika, ki se vežejo na njegovo zadnjo oziroma najnovejšo odobreno vlogo v letu 
2017. 


18 
EkonomIERa  
03-2023 
Tabela 2: Porazdelitev oseb glede na ekonomski status, leto 2017 
 
Simulirani rezultati 
Zunanji podatki 
  
Januar (les01) 
Junij (les06)* 
December (les12) 
2017 
Ekonomski status 
Število 
Delež 
Število 
Delež 
Število 
Delež 
Število 
Ekonomski 
status 
Otroci v vrtcu in mlajši 
148.956 
7,21 
148.956 
7,21 
133.037 
6,44 
149.180 
Otroci, stari 0–
6 let** 
Kmetje 
11.995 
0,58 
11.857 
0,57 
11.863 
0,57 
851.848 
Zaposleni*** 
Samozaposleni 
70.273 
3,4 
70.411 
3,41 
71.154 
3,45 
Zaposleni 
739.078 
35,79 
747.329 
36,19 
751.806 
36,41 
Upokojenci 
429.165 
20,78 
432.011 
20,92 
435.123 
21,07 
534.336 
Upokojenci*** 
Brezposelni 
93.037 
4,51 
81.795 
3,96 
80.696 
3,91 
101.816 
Brezposelni*** 
Študenti/dijaki/ učenci 299.033 
14,48 
297.349 
14,4 
300.307 
14,54 
331.611 Študenti/dijaki/ 
učenci# 
Neaktivni 
188.707 
9,14 
188.547 
9,13 
190.725 
9,24 
111.329 
Drugi 
neaktivni*** 
Bolni in invalidni 
84.859 
4,11 
86.845 
4,21 
90.392 
4,38 
n.p. 
n.p. 
Opombe: * Pri analizi smo v primeru upoštevanja letnega ekonomskega status (in ne v začetku, sredini 
ali kuncu leta), upoštevali status v sredini leta (les=les06). ** Podatek se nanaša na drugo polovico leta 
(2017H2). *** Podatek se nanaša na osebe, stare 15+ let. # Podatek se nanaša na 2017/18. 
Vir: SURS in lastni izračuni. 
Tudi podatek o trenutni izobrazbi (dec) smo na podlagi združevanja podatkov 
iz različnih baz določili sami. Iz popisa prebivalstva smo upoštevali podatek o 
izobrazbi (najvišje dosežena izobrazba) in statusu aktivnosti, iz IS CSD baz pa smo 
upoštevali status šolajočega (vključenost v izobraževanje). Podatek o trenutni 
izobrazbi smo pripisali le mlajšim od 14 let, dijakom in študentom. Ker imamo 
podatek o statusu šolajočih le za osebe iz IS CSD baz, smo predpostavili, da so: 
- 
vsi otroci, mlajši od 6 let, ki nimajo podatka o vključenosti v vrtec, doma 
(večinoma gre za dojenčke in predšolske otroke, za katere podatki v IS 
CSD bazah potrjujejo, da niso vključeni v vrtec); 
- 
vsi otroci, ki imajo podatek o vključenosti v vrtec, vključeni v vrtec oziroma 
predšolsko izobraževanje; 
- 
vsi otroci, stari od 5 do vključno14 let, ki še niso dokončali osnovne šole, 
ter 15-letniki, za katere imamo podatek, da so v osnovni šoli, vključeni v 
osnovno šolo oz. primarno izobraževanje; 
- 
14-letniki in starejši, za katere imamo podatek, da so v srednji šoli ali 
imajo status aktivnosti učenca/dijaka, vključeni v srednjo šolo oziroma 
sekundarno izobraževanje; 


 
19 
- 
vsi, za katere imamo podatek, da so v višji oziroma visoki šoli, ali so 
starejši od 18 let in imajo status aktivnosti študenta, trenutno vključeni v 
višješolsko, visokošolsko oziroma terciarno izobraževanje. 
Podatek o trenutni izobrazbi smo uskladili še s podatkom o statusu mesečne 
aktivnosti posameznika ter ekonomskem statusu (les). Najprej smo za osebo, 
kateri je bil pripisan status mesečne aktivnosti študenta/dijaka/učenca vsaj en 
mesec v letu 2017, predpostavljali, da se oseba trenutno izobražuje, in obratno, v 
primeru, 
da 
osebi 
nismo 
pripisali 
statusa 
mesečne 
aktivnosti 
študenta/dijaka/učenca v nobenem mesecu leta 2017, smo za vse te osebe 
predpostavljali, da se trenutno ne izobražujejo. Tako smo novo določenim 
šolajočim, 16 do 18-letnikom pripisali vključenost v sekundarno izobrazbo, 19-
letnikom in starejšim pa vključenost v terciarno izobrazbo. Nazadnje smo podatek 
o trenutni izobrazbi uskladili še glede na ekonomski status osebe. Vsem osebam, 
ki niso imele ekonomskega statusa študenta/dijaka/učenca (les=6) ali otroka v 
vrtcu in mlajši (les=0), smo pripisali, da se trenutno ne izobražujejo.  
Primerjava simuliranih rezultatov in zunanjih podatkov SURS (tabela 3) kaže, da 
smo se približali uradnim podatkom, z izjemo podatka o številu študentov. Razlog 
za podcenjenost števila študentov lahko izhaja ravno iz odločitve, opisane na 
koncu prejšnjega odstavka, saj smo končni status osebe o trenutni vključenosti v 
izobraževanje (dec) oblikovali tudi na podlagi upoštevanja ekonomskega statusa 
(les). To pomeni, da je bila na primer oseba na začetku leta 2017 lahko študent, 
vendar v mesecu juniju, ko gledamo ekonomski status osebe, ni imela več statusa 
študenta/dijaka/učenca ali pa ga še ni imela in je zato ne štejemo kot osebo, 
vključeno v izobraževanje (npr. oseba je zaključila s študijem v prvi polovici leta 
2017 ali pa je pridobila status študenta šele z vpisom v študijski program z novim 
študijskem letom 2017/18).   


20 
EkonomIERa  
03-2023 
Tabela 3: Vključeni v formalno izobraževanje, leto 2017  
 
Simulirani 
rezultati 
Podatki SURS 
Vključeni v izobrazbo 
2017 
2016/17 
2017/18 
Otroci v vrtcu 
94.582 
86.284 
86.703 
Učenci 
182.266 
176.898 
181.301 
Dijaki 
73.421 
74.021 
73.776 
Študenti 
56.743 
79.547 
76.534 
Skupaj 
407.012 
416.750 
418.314 
Vir: SURS in lastni izračuni. 
V nadaljevanju opisujemo oblikovanje še nekaj pomembnejših spremenljivk, ki 
smo jih na podlagi obstoječih podatkov oblikovali sami in pripomorejo k 
natančnejši izvedbi simulacij davkov, socialnih transferjev in nadomestil.  
Na podlagi ZPIZ podatkov o zavarovancih, kjer imamo za posameznika zbrane 
datume vseh prijav v zavarovanja in datume vseh odjav iz zavarovanj, smo 
posameznikom izračunali dopolnjeno zavarovalno dobo. Podatek smo spremenili 
v mesece in ga oblikovali kot podatek o delovni dobi oziroma številu mesecev 
zaposlitve (liwwh). Podatek o številu mesecev zaposlitve uporabimo pri 
simuliranju denarnega nadomestila za brezposelnost.  
Pri simulaciji denarnega nadomestila za brezposelnost uporabimo še eno novo 
ustvarjeno spremenljivko, tj. osnova za izračun denarnega nadomestila za 
brezposelnost (yempv). To smo določili posameznikom, ki so prejemali denarno 
nadomestilo na enega od dveh načinov:  
- 
na podlagi podatkov ZPIZ o zavarovancih smo določili plačo iz leta 2016;  
- 
za posameznike, za katere v ZPIZ podatkih ni bilo podatka o plači za leto 
2016, smo yempv ocenili na podlagi višine denarnega nadomestila in 
podatka/predpostavke o trajanju prejemanja nadomestila.  
Prav tako smo posameznikom na podlagi podatka o plačnih zgodovinah (ZPIZ 
podatki o zavarovancih) pripisali podatek o plači na uro za leto 2017 (yivwg). Če 
za posameznika podatka o plači ni bilo, smo plačo na uro ocenili s Heckmanovo 
enačbo oziroma Heckmanovim modelom izbire, ločeno za moške in ženske. 
Heckmanov model vključuje dve ločeni enačbi: za plače in za izbiro. Enačba plače 
je odvisna od starosti, izobrazbe in števila mesecev v zaposlitvi (liwwh). Pri tem 


 
21 
smo v enačbo plače vključili le moške in ženske, stare med 18 in 65 leti, ki se ne 
izobražujejo in ne prejemajo dohodka iz samozaposlitve ali pokojnine. Dodatne 
spremenljivke v enačbi izbire so partner (ali oseba ima partnerja ali ne), število 
otrok po starostnih skupinah in dohodki drugih posameznikov, ki živijo v istem 
gospodinjstvu. Te spremenljivke pojasnjujejo izbiro, ali oseba dela ali ne, ne pa 
rezultata (višino plače). Podatek o plači na uro smo uporabili pri simulaciji 
materinskega in starševskega nadomestila ter očetovskega nadomestila.  
Dojenčkom (otroci, stari do enega leta) smo pripisali podatek o številu mesecev v 
letu 2017, ko še niso bili stari eno leto (dag00). Ta podatek nam služi, da lahko 
natančneje simuliramo starševski dodatek, saj tako upoštevamo mesece 
prejemanja starševskega dodatka v letu 2017 glede na starost dojenčka (meseci, 
ko otrok še ni star eno leto) namesto predpostavke, da oseba prejema starševski 
dodatek celo leto.   
Na podlagi podatka o generalnem statusu posameznika iz baze CRP, ki nam pove, 
ali je oseba živa ali je umrla, smo lahko identificirali posameznike, ki so v letu 2017 
izgubili ožjega družinskega člana (partnerja ali starša) (dfa=1). Podatek o smrti 
ožjega družinskega člana smo pripisali posameznikom, ki so bili ali 
partner/partnerica umrlega/umrle ali najstarejši otrok pokojne osebe v primeru, 
da umrla oseba ni imela partnerja/partnerice. Ta podatek uporabimo pri določitvi 
upravičencev do pravic pogrebnine in posmrtnine. Pri tem moramo opozoriti, kot 
je razvidno iz zapisanega, da smo kot upravičenca do pogrebnine ali posmrtnine 
določili le partnerja ali otroka, medtem ko so po zakonu ZSVarPre do obeh pravic 
upravičeni tudi starši, bratje ali sestre, nečaki ali nečakinje ter vnuki in vnukinje 
pokojne osebe.  
Za natančnejšo določitev upravičencev in prejemnikov pravice varstvenega 
dodatka smo posameznikom pripisali podatek o tem, ali imajo polnoletne otroke 
(dadch=1). Slednji so na podlagi družinske zakonodaje (veljavne leta 2017 in vse 
do danes, torej leta 2023) po svojih zmožnostih dolžni preživljati svoje starše, če 
si ti sami ne morejo zagotoviti preživetja. Osebe, ki imajo polnoletne otroke, za 
katere je ugotovljeno, da so zmožni preživljati svoje starše, niso upravičene do 
prejemanja varstvenega dodatka.  
Otroke (do 18 leta oziroma do 26 leta, če se šolajo) smo tudi označili po vrstnem 
redu oziroma po starosti od najstarejšega do najmlajšega (dch) za natančnejšo 
dodelitev pravice do znižanega plačila vrtca (VR). 


22 
EkonomIERa  
03-2023 
Na novo smo oblikovali podatek o številu mesecev, ko je otrok lahko vzdrževani 
član (tchmy). Spremenljivko smo oblikovali na podlagi skupnega števila mesecev 
v 
letu, 
ko 
ima 
posamezna 
oseba 
mesečni 
status 
aktivnosti 
študenta/dijaka/učenca. Ta podatek smo uporabili pri simulaciji olajšave za 
vzdrževane družinske člane in splošne olajšave pri dohodnini. 
3.1.2 
Dohodki, nadomestila, transferji 
Podatke o večini dohodkov smo pridobili iz dohodninskih podatkov: 
- 
dohodek iz zaposlitve (šifra dohodkov 1000), 
- 
dohodek iz dejavnosti (šifra dohodkov 2000), 
- 
dohodek iz osnovne kmetijske in osnovne gozdarske dejavnosti (šifra 
dohodkov 3000), 
- 
dohodek iz premoženja (šifra dohodkov 4000), 
- 
dohodek iz kapitala (šifra dohodkov 5000), 
- 
drugi dohodki (šifra dohodkov 6000). 
Nekatere dohodke, nadomestila in transferje smo na podlagi obstoječih baz 
podatkov oziroma njihovega združevanja ali razdruževanja podrobneje določili 
sami. Tako smo dohodek iz zaposlitve podrobneje razdelili na 6 tipov dohodkov 
(glej tabelo 4):  
- 
obdavčljivi dohodek iz zaposlitve (šifra dohodka 1101), 
- 
drugi obdavčljivi dohodki iz zaposlitve (šifre dohodkov 1102, 1104, 1105, 
1109 in 1110), 
- 
regres za letni dopust (šifra dohodka 1103), 
- 
pokojnina (šifra dohodka 1106), 
- 
invalidska nadomestila (šifra dohodka 1107), 
- 
nadomestila iz naslova obveznega zdravstvenega zavarovanja (bolniški 
dopust nad 30 dni, ki je del dohodka šifre 1108). 
Podatke o prejetih (yptmp) in plačanih preživninah (xmp) imamo le za osebe, 
ki so oddale vlogo za uveljavljanje pravic iz javnih sredstev in so zavedene v IS 
CSD. Na podlagi upoštevanja dveh oblik dohodkov iz IS CSD baz, in sicer 
preživnine, ki jo izplačuje CSD, in nadomestila preživnine, ki jo izplačuje Javni 
štipendijski, razvojni, invalidski in preživninski sklad RS (JŠRIP) (pred letom 2017 
imenovan Javni preživninski sklad Republike Slovenije (JPRS)), smo določili 
prejeto preživnino (yptmp).  


 
23 
Tudi podatek o nadomestilu za izgubljeni dohodek zaradi otroka, ki 
potrebuje posebno nego (bcrsvcc), smo pridobili iz IS CSD baz. Zato smo 
znesek tega nadomestila odšteli od dohodninskega podatka o drugih dohodkih 
iz zaposlitve (delno plačilo za izgubljeni dohodek je del dohodka šifre 1109). 
Podatke o pravicah iz javnih sredstev (starševskih nadomestilih in socialnih 
transferjih) smo pridobili iz baz IS CSD. Podatke o transferjih, ki jih izplačuje ZPIZ 
(invalidnina (bdixp), dodatek za pomoč in postrežbo (bdica), ter letni dodatek za 
upokojence (pls) smo pridobili iz ZPIZ-ovih baz podatkov. Za simulacijo nekaterih 
pravic iz javnih sredstev so bili potrebni določeni dodatni izračuni in 
predpostavke, da smo osebam lahko pripisali prave podatke na način, kot jih 
potrebujemo za simulacijo določene pravice. Pomembnejše izračune in sprejete 
predpostavke povzemamo v nadaljevanju.  
V bazi IS CSD so podatki o materinskem, očetovskem in starševskem nadomestilu 
ter o nadomestilu v času odmora za dojenje podani kot pravica z imenom 
starševsko nadomestilo. Znesek te pravice ni podan kot pravi znesek pravice, ki jo 
je upravičenec prejel, ampak osnova, na podlagi katere se je določila višina 
pravice za posameznika. V letu 2017 je materinsko nadomestilo znašalo 100 % 
osnove, medtem ko sta starševsko in očetovsko nadomestilo znašala 90 % 
osnove. Nadalje, očetje so v letu 2017 imeli tudi pravico do koriščenja 
neplačanega očetovskega dopusta. V tem primeru očetje niso prejemali 
očetovskega nadomestila, imeli pa so s strani države plačane prispevke za 
socialno varnost. Zaradi različnih vrst starševskih nadomestil in pripadajočih 
zneskov nadomestil smo na podlagi upoštevanja števila dni prejemanja 
nadomestila (prejemanje pravice se je lahko pričelo že v letu 2016, vendar z 
nadaljevanjem v letu 2017) in zneska osnove za določitev starševskega 
nadomestila sami oblikovali naslednje predpostavke in podrobneje opredelili 
vrsto starševskega nadomestila:  
- 
vsem, ne glede na spol, ki so neprekinjeno prejemali starševsko 
nadomestilo 
105 
dni, 
smo 
pripisali 
prejemanje 
materinskega 
nadomestila; 
- 
ženskam, ki so prejemale starševsko nadomestilo manj kot 105 dni, smo 
pripisali prejemanje starševskega nadomestila; 
- 
ženskam, ki so prejemale starševsko nadomestilo več kot 105 dni, smo 
od 106. dne dalje pripisali prejemanje starševskega nadomestila; 


24 
EkonomIERa  
03-2023 
- 
moškim, ki so dnevno prejemali starševsko nadomestilo in je bila osnova 
nadomestila enaka takratni minimalni plači, smo pripisali koriščenje 
očetovskega neplačanega dopusta; 
- 
ženskam, ki so prejemale starševsko nadomestilo in je bila osnova 
nadomestila enaka takratni minimalni plači, smo pripisali koriščenje 
odmora za dojenje med delovnim časom; 
- 
vsem, ki so prejemali starševsko nadomestilo in jim na podlagi zgornjih 
kriterijev še ni bila pripisana podrobnejša vrsta starševskega nadomestila, 
smo pripisali prejemanje starševskega nadomestila – v teh primerih gre 
za koriščenje eno od treh oblik pravic, in sicer starševskega dopusta, 
očetovskega plačanega dopusta ali prenesenega dopusta po dnevih 
oziroma v strnjenem nizu, za katere je nadomestilo znašalo 90 % osnove.  
Ob upoštevanju zgornjih predpostavk smo nadalje oblikovali: a) materinsko in 
starševsko nadomestilo (bmact) ter b) očetovsko nadomestilo (bcrbafh). K 
slednjemu, očetovskemu nadomestilu, štejemo starševsko nadomestilo, ki ga 
prejema moški do enega meseca (predpostavka, sprejeta na podlagi pravice, ki je 
veljala za očete v letu 2017, in sicer, da so očetje lahko koristili 25 dni plačanega 
dopusta). K materinskemu in starševskemu nadomestilu pa štejemo materinsko 
nadomestilo (ne glede na spol), starševsko nadomestilo, ki ga prejema ženska, 
starševsko nadomestilo, ki ga prejema moški nad enim mesecem, in nadomestilo 
za koriščenje prenesenega dopusta po dnevih (ne glede na spol). Pravici 
koriščenja očetovskega neplačanega dopusta in odmora za dojenje med 
delovnim časom zaradi pomanjkljivosti podatkov ne upoštevamo. 
Tudi pri koriščenju pravice plačila prispevkov zaradi dela s krajšim delovnim 
časom in v primeru skrbi za štiri ali več otrok je kot znesek pravice v podatkih 
podana osnova, na podlagi katere so se obračunali prispevki za socialno varnost. 
Natančneje, v primeru pravice do plačila prispevkov zaradi dela s krajšim delovnim 
časom osnova predstavlja sorazmerni del (upoštevajoč ure koriščenja pravice) 
bruto minimalne plače, od katere so se izračunali prispevki. Na podlagi tega 
podatka smo posameznikom pripisali število ur koriščenja pravice do plačila 
prispevkov zaradi dela s krajšim delovnim časom in znesek obračunanih/plačanih 
prispevkov za socialno varnost. Prav tako smo znesek obračunanih/plačanih 
prispevkov za socialno varnost pripisali prejemnikom, ki so uveljavljali pravico do 
plačila prispevkov v primeru skrbi za štiri ali več otrok.  


 
25 
V podatkih iz IS CSD prihaja do prekrivanja pri koriščenju pravic iz zavarovanja 
starševskega varstva (starševsko nadomestilo, plačilo prispevkov zaradi koriščenja 
krajšega delovnega časa in plačilo prispevkov zaradi varovanja štirih ali več otrok) 
in družinskih transferjev (delno plačilo za izgubljeni dohodek). V takih primerih 
smo sledili pravilu: povsod, kjer prihaja do prekrivanja pravic delnega plačila za 
izgubljeni dohodek/plačila prispevkov zaradi koriščenja krajšega delovnega 
časa/plačila prispevkov zaradi varovanja štirih ali več otrok in starševskih 
nadomestil, pravico delno plačilo za izgubljeni dohodek/plačilo prispevkov zaradi 
koriščenja krajšega delovnega časa/plačilo prispevkov zaradi varovanja štirih ali 
več otrok prekinemo za obdobje prejemanja starševskega nadomestila (dneve 
prejemanja delnega plačila za izgubljeni dohodek/plačila prispevkov zaradi 
koriščenja krajšega delovnega časa/plačila prispevkov zaradi varovanja štirih ali 
več otrok skrajšamo). Namreč, omenjene pravice se med seboj načeloma ne 
smejo prekrivati in v takih primerih pride do »zamrznitve« in prekinitve 
izplačevanja prve pravice za čas koriščenja druge pravice.   
Pri simuliranju denarne socialne pomoči smo za izračun višine dohodka 
posameznika oziroma gospodinjstva upoštevali mesečne dohodke, če smo 
razpolagali s podatki. Tako smo za del dohodkov iz zaposlitve razpolagali z 
dejanskimi dohodki v posameznem mesecu leta 2017, medtem ko smo za vse 
ostale dohodke predpostavljali, da so vsak mesec znašali 1/12 letnega dohodka. 
Podatke o mesečnih dohodkih smo pridobili iz mesečnih REK obrazcev, pri čemer 
smo upoštevali posebej: a) obdavčljivi dohodek iz zaposlitve (yemtx), b) drugi 
obdavčljivi dohodki iz zaposlitve (yemot) in c) regres (yemhl). Omenjene tri 
dohodke smo skupno poimenovali dohodki iz zaposlitve z nad-oznako yem (glej 
tabelo 4). Ker smo združevali dohodke iz dveh podatkovnih baz, in sicer letne 
dohodninske podatke in mesečne podatke iz REK obrazcev8, je prihajalo do 
nekaterih neskladij, zato smo za končno določitev mesečnih dohodkov iz 
zaposlitve oblikovali pravila posebej za obdavčljivi dohodek iz zaposlitve, druge 
obdavčljive dohodke iz zaposlitve in regres.  
V primeru obdavčljivega dohodka iz zaposlitve (plača) smo predpostavili, da so 
mesečni zneski o dohodkih iz REK obrazcev dejansko izplačani dohodki v 
naslednjem mesecu, npr. znesek dohodka iz REK obrazca za mesec januar je 
 
8 Podatkov o dohodkih iz IS CSD baz nismo upoštevali, saj so z izjemo tekočih dohodkov podani neto 
zneski dohodkov. 


26 
EkonomIERa  
03-2023 
dohodek, ki ga je oseba dejansko prejela v mesecu februarju. Z upoštevanjem 
takšne predpostavke nam je manjkal podatek o januarskem dohodku oziroma 
plači, zato smo na podlagi treh pravil in izračunov predpostavili januarsko plačo, 
ki je enaka:  
- 
razliki med vsoto mesečnih dohodkov in letnim dohodkom, če je bila 
vsota mesečnih dohodkov iz REK obrazcev za mesece januar–november 
nižja od letnega podatka o dohodku iz dohodninskih podatkov (vsoto 
mesečnih dohodkov iz REK obrazcev smo odšteli od letnega zneska 
dohodka iz dohodninskih podatkov); 
- 
letnemu dohodku, če za osebo ni bilo mesečnih podatkov iz REK 
obrazcev za mesece januar–november (predpostavili smo, da je podatek 
o letnem dohodku iz dohodninskih podatkov enak januarskemu 
dohodku); 
- 
0, če je bila vsota mesečnih dohodkov iz REK obrazcev za mesece januar–
november višja od letnega podatka o dohodku iz dohodninskih 
podatkov; v tem primeru smo vse mesečne (pozitivne) dohodke zmanjšali 
za povprečno vrednost presežka mesečnih dohodkov nad letnim 
dohodkom in tako uskladili mesečne dohodke z letnim dohodkom 
(znesek seštevka mesečnih dohodkov se ujema z zneskom letnega 
dohodka). 
Ker gre v primeru prejemanja drugih obdavčljivih dohodkov iz zaposlitve za 
neredne dohodke, ne moremo dovolj natančno predpostaviti, katerem mesecu je 
oseba prejela ta dohodek. Zato smo upoštevali vse mesečne podatke iz REK 
obrazcev, tudi za mesec december, in predpostavili sledeče:  
- 
če se mesečni dohodki iz REK obrazcev za mesece januar–december niso 
ujemali z letnim zneskom dohodka iz dohodninskih podatkov, smo 
mesečne dohodke znižali oziroma povečali za povprečni znesek 
neujemanja (znesek seštevka mesečnih drugih dohodkov iz zaposlitve se 
ujema z letnim zneskom te vrste dohodka); 
- 
če je bil za osebo znan le podatek o drugih obdavčljivih dohodkih iz 
zaposlitve na letni ravni iz dohodninskih podatkov (mesečni podatki o teh 
dohodkih iz REK obrazcev za osebo niso bili znani), smo letni znesek 
enakomerno porazdelili čez vseh 12 mesecev. 


 
27 
V primeru regresa smo prav tako upoštevali vse mesečne podatke iz REK 
obrazcev, tudi za mesec december, in predpostavili:  
- 
če se mesečni dohodki iz REK obrazcev za mesece januar–december niso 
ujemali z letnim zneskom dohodka iz dohodninskih podatkov, smo 
mesečne dohodke znižali oziroma povečali za povprečni znesek 
neujemanja (znesek seštevka mesečnih dohodkov regresa se ujema z 
zneskom letnega regresa); 
- 
če je bil za osebo znan le podatek o regresu na letni ravni iz dohodninskih 
podatkov (mesečni podatki o regresu iz REK obrazcev za osebo niso bili 
znani), smo predpostavili, da je oseba prejela regres v mesecu juniju (letni 
znesek regresa pripišemo mesecu juniju). 
V dohodninskih podatkih imamo podatek o pokojnini ne glede na vrsto 
pokojnine. Z združevanjem dohodninskih in ZPIZ-ovih podatkov iz evidenc 
upokojitvenega postopka smo pokojnine ločili na staroste pokojnine (poa00), 
invalidske pokojnine (pdi00) in vdovske oziroma družinske pokojnine (psu00).  
Mesečno vrednost dohodkov, nadomestil in transferjev, katerih vrednosti ne 
moremo določiti na mesečni ravni na podlagi uporabljenih baz podatkov, smo 
določili kot 1/12 dejanskega letnega dohodka. 
V naslednjih dveh tabelah (tabeli 4 in 5) so navedeni vsi dohodki, nadomestila in 
transferji, pri čemer navajamo oznako dohodka, nadomestila in socialnega 
transferja v mikro bazi ter vir podatkov.  
 


28 
EkonomIERa  
03-2023 
Tabela 4: Opredelitev dohodkov in nadomestil v mikropodatkih glede na opredelitev dohodkov po zakonu, ki ureja 
dohodnino (ZDoh) 
Mikropodatki 
Zunanji podatki 
Vrsta dohodka, 
nadomestila 
Oznaka 
Nad-vrsta 
dohodka, 
nadomestila 
Nad-
oznaka 
Vir podatka 
na letni 
ravni (baza 
podatkov) 
 
Vir 
podatka 
na 
mesečni 
ravni 
(baza 
podatkov) 
 
Nad-vrsta 
dohodka, 
nadomestila 
Oznaka 
Vrsta dohodka, nadomestila 
Obdavčljivi 
dohodek iz 
zaposlitve 
yemtx 
Dohodki iz 
zaposlitve 
yem 
Dohodninski 
podatki (na 
letni ravni) 
(SURS) 
Obračun 
davčnih 
odtegljajev 
za 
dohodke 
iz 
delovnega 
razmerja, 
REK 
obrazci 
(ZPIZ) 
Dohodek iz 
zaposlitve 
1101 
Plače, nadomestilo plače in povračila stroškov v zvezi z delom  
Drugi obdavčljivi 
dohodki iz 
zaposlitve 
yemot 
1102 
Bonitete 
1104 
Jubilejne nagrade, odpravnine ob upokojitvi in solidarnostne 
pomoči  
1105 
Premije za prostovoljno dodatno pokojninsko in invalidsko 
zavarovanje   
1109 
Drugi dohodki iz delovnega razmerja, razen delnega plačila za 
izgubljeni dohodek (bcrsvcc), kar obravnavamo kot samostojni 
transfer (glej tabelo 5) 
1110 
Dohodek za vodenje družbe (zavarovalna  
podlaga 040) 
Regres za letni 
dopust  
yemhl 
1103 
Regres za letni dopust 
Starostna pokojnina  
 
poa00 
 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
1106 
Pokojnine iz obveznega pokojninskega in invalidskega 
zavarovanja  
Invalidska 
pokojnina 
 
pdi00 
 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Družinska in 
vdovska pokojnina 
psu00 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 


 
29 
Mikropodatki 
Zunanji podatki 
Vrsta dohodka, 
nadomestila 
Oznaka 
Nad-vrsta 
dohodka, 
nadomestila 
Nad-
oznaka 
Vir podatka 
na letni 
ravni (baza 
podatkov) 
 
Vir 
podatka 
na 
mesečni 
ravni 
(baza 
podatkov) 
 
Nad-vrsta 
dohodka, 
nadomestila 
Oznaka 
Vrsta dohodka, nadomestila 
Nadomestila za 
delovne invalide 
bdirw 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
1107 
Nadomestila iz naslova obveznega pokojninskega in 
invalidskega zavarovanja  
Bolniška nad 30 dni bhl 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Del 
1108  
Nadomestila in drugi dohodki iz naslova obveznega socialnega 
zavarovanja – le dolgotrajna bolniška; vsa ostala nadomestila in 
dohodke (starševska nadomestila, plačilo prispevkov zaradi 
koriščenja krajšega delovnega časa, denarno nadomestilo za 
brezposelne…) smatramo kot samostojne transferje in 
nadomestila (glej tabelo 5)   
Dohodek 
študentov, 
upravičenih do 
posebne olajšave 
yst 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodek iz 
drugega 
pogodbenega 
razmerja 
1211 
Dohodki dijakov in študentov upravičenih do posebne olajšave 
Dohodek 
študentov, 
neupravičenih do 
posebne olajšave 
ystw 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
1212 
Dohodki dijakov in študentov, ki niso upravičeni do posebne 
olajšave 
Dohodek iz 
dodatne zaposlitve 
1 
yaj01 
Dohodki iz 
dodatne 
zaposlitve 
yaj 
Dohodninski 
podatki 
(SURS) 
/ 
1220 
Dohodki verskih delavcev 
Dohodek iz 
dodatne zaposlitve 
2 
yaj02 
1230 
Preostali dohodki iz drugega pogodbenega razmerja 


30 
EkonomIERa  
03-2023 
Mikropodatki 
Zunanji podatki 
Vrsta dohodka, 
nadomestila 
Oznaka 
Nad-vrsta 
dohodka, 
nadomestila 
Nad-
oznaka 
Vir podatka 
na letni 
ravni (baza 
podatkov) 
 
Vir 
podatka 
na 
mesečni 
ravni 
(baza 
podatkov) 
 
Nad-vrsta 
dohodka, 
nadomestila 
Oznaka 
Vrsta dohodka, nadomestila 
Dohodek iz 
samozaposlitve 
yse00 
Dohodki iz 
samozaposlitve 
yse 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodek iz 
dejavnosti 
2100 
Dobiček, ugotovljen na podlagi davčnega obračuna 
Dohodek iz 
samozaposlitve – 
normiranci 
ysen 
2200 
Dohodek zavezancev z upoštevanjem normiranih odhodkov 
Dohodek iz 
samozaposlitve – 
kmetijska dejavnost 
yseag 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodek iz 
osnove 
kmetijske in 
osnovne 
gozdarske 
dejavnosti 
3100 
Dohodek iz osnovne kmetijske in osnovne gozdarske dejavnosti 
Dohodek iz 
premoženja 
ypr 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodek iz 
premoženja 
4100 
Dohodek iz oddajanja premoženja v najem  
Avtorski honorar 
yro 
/ 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
4200 
Dohodek iz prenosa premoženjske pravice 
Kapitalski dohodek 
– obresti dosežene 
yiyitdp 
Dohodki iz 
kapitala 
yiy 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodek iz 
kapitala 
5300 
Obresti fizične osebe, dosežene na denarne depozite pri bankah 
in hranilnicah, ustanovljenih v skladu s predpisi v Sloveniji ter pri 
bankah in hranilnicah drugih držav članic EU  


 
31 
Mikropodatki 
Zunanji podatki 
Vrsta dohodka, 
nadomestila 
Oznaka 
Nad-vrsta 
dohodka, 
nadomestila 
Nad-
oznaka 
Vir podatka 
na letni 
ravni (baza 
podatkov) 
 
Vir 
podatka 
na 
mesečni 
ravni 
(baza 
podatkov) 
 
Nad-vrsta 
dohodka, 
nadomestila 
Oznaka 
Vrsta dohodka, nadomestila 
na denarne 
depozite 
 
Kapitalski dohodek 
- ostalo 
yiyot 
5200 
Dobiček iz kapitala, dosežen z odsvojitvijo kapitala, vrednostnih 
papirjev in deležev v gospodarskih družbah, zadrugah in drugih 
oblikah organiziranja ter investicijskih kuponov  
5201 
Dobiček iz kapitala, dosežen z odsvojitvijo nepremičnin  
5400 
Obresti  
5600 
Obresti na obveznice »SOS2E«, izplačane upravičencem  
5700 
Dividende  
5800 
Dividende in obresti, izplačane preko posrednika, ki ni dolžan 
izračunati in odtegniti davka  
5801 
Dividende, izplačane preko plačnika davka, ki ni dolžan 
izračunati in odtegniti davka 
5900 
Obresti, dosežene ob odsvojitvi diskontiranega dolžniškega 
vrednostnega papirja pred dospelostjo papirja ali pri odkupu 
diskontiranega dolžniškega vrednostnega papirja pred ali ob 
dospelosti papirja oziroma ob vnovčitvi diskontiranih dolžniških 
vrednostnih papirjev  
Drugi dohodki 
yot 
/ 
/ 
/ 
/ 
Drugi 
dohodki 
6100 
Darila  
6200 
Priznavalnine  
6300 
Preostali drugi dohodki 
6500 
Nadomestilo za uporabo lastnih sredstev prostovoljca 
6700 
Dohodki Fulbrightovega programa izmenjav 
Neobdavčljivi 
dohodek iz 
zaposlitve 
yemnt 
/ 
/ 
/ 
Obračun 
davčnih 
odtegljajev 
za 
dohodke 
/ 
/ 
Del plače za poslovno uspešnost v znesku, ki se ne všteva v 
davčno osnovo, in dohodek iz delovnega razmerja, ki se ne 
všteva v davčno osnovo 


32 
EkonomIERa  
03-2023 
Mikropodatki 
Zunanji podatki 
Vrsta dohodka, 
nadomestila 
Oznaka 
Nad-vrsta 
dohodka, 
nadomestila 
Nad-
oznaka 
Vir podatka 
na letni 
ravni (baza 
podatkov) 
 
Vir 
podatka 
na 
mesečni 
ravni 
(baza 
podatkov) 
 
Nad-vrsta 
dohodka, 
nadomestila 
Oznaka 
Vrsta dohodka, nadomestila 
iz 
delovnega 
razmerja, 
REK 
obrazci 
(ZPIZ) 
Dohodki iz tujine 
yemabtx*  / 
/ 
Dohodninski 
podatki 
(SURS) 
/ 
Dohodki iz 
tujine 
1101 
Plače, nadomestilo plače in povračila stroškov v zvezi z delom, 
ko imamo podatek o davku, plačanem v tujini 
Opombe: * Kategorična spremenljivka: 0 = domači dohodki, 1 = tuji dohodki, 2 = tuji in domači dohodki. 


 
33 
Tabela 5: Opredelitev transferjev in nadomestil v mikropodatkih  
Vrsta transferja, nadomestila 
SLOmod 
oznaka 
Vir podatka 
(baza podatkov) 
Denarno nadomestilo za brezposelne 
bunct 
Podatki: denarno 
nadomestilo za 
brezposelnost 
Materinsko in starševsko nadomestilo 
bmact 
IS CSD 
Očetovsko nadomestilo 
bcrbafh 
IS CSD 
Starševski dodatek 
bmanc 
IS CSD 
Otroški dodatek  
bchmt 
IS CSD2 
Pomoč ob rojstvu otroka 
bchba 
IS CSD 
Dodatek za veliko družino 
bchlg 
IS CSD2 
Denarna socialna pomoč 
bsa 
IS CSD2 
Varstveni dodatek 
bsapm 
IS CSD2 
Državna štipendija 
bedmt 
IS CSD2 
Subvencija malice 
bedrd01 
IS CSD2 
Subvencija kosila 
bedrd02 
IS CSD2 
Znižano plačilo vrtca 
bchedyc 
IS CSD2 
Subvencija najemnine 
bho 
IS CSD2 
Pogrebnina  
bsafu 
IS CSD2 
Posmrtnina  
bsawd 
IS CSD2 
Izredna denarna pomoč 
bsaec 
IS CSD2 
Dodatek za nego otroka 
bchcc 
IS CSD 
Delno plačilo za izgubljeni dohodek  
bcrsvcc 
IS CSD 
Plačilo prispevkov zaradi koriščenja 
krajšega delovnega časa 
bfapt 
IS CSD 
Plačilo prispevkov zaradi varovanja 
štirih ali več otrok 
bfabk 
IS CSD 
Prejete preživnine 
yptmp 
IS CSD2 
Plačane preživnine 
xmp 
IS CSD2 
Invalidnina  
bdixp 
Nakazila uživalcem pravic 
pri ZPIZ  
Dodatek za pomoč in postrežbo 
bdica 
Nakazila uživalcem pravic 
pri ZPIZ  
Letni dodatek za upokojence 
pls 
Nakazila uživalcem pravic 
pri ZPIZ  
 
3.1.3 
Število mesecev prejemanja dohodka, nadomestila, transferja 
Določitev števila mesecev prejemanja dohodka iz zaposlitve je zahtevala več 
operacij. Najprej smo za vsak mesec ugotavljali, ali je oseba prejela omenjeni 
dohodek ali ne. Slednje smo določili na podlagi upoštevanja obstoječih podatkov 
v naslednjemu vrstnem redu: 


34 
EkonomIERa  
03-2023 
- 
mesečni dohodki iz zaposlitve (yem) (za vsak mesec smo označili, ali je 
oseba prejela dohodek iz zaposlitve ali ne), 
- 
mesečni dohodki iz zaposlitve, pridobljeni iz IS CSD baz o dohodkih 
(mesec prejetega dohodka9 smo določili kot m-1, pri čemer m pomeni 
mesec oddane vloge za uveljavljanje pravic iz javnih sredstev; podatke 
smo upoštevali le za tiste osebe, ki so imele podatek o vsaj enem 
mesečnem10 dohodku v obdobju treh koledarskih mesecev pred 
mesecem vložitve vloge), 
- 
status mesečnih aktivnosti in letni dohodek iz zaposlitve (osebi smo 
pripisali, da je prejela  dohodek iz zaposlitve za tisti mesec, ko je imela 
status mesečne aktivnosti zaposlen za polni ali krajši delovni čas ob 
pogoju, da je imela tudi pozitivni letni dohodek iz zaposlitve (yem)). 
Za določitev končnega števila mesecev prejemanja dohodka iz zaposlitve v letu 
2017 (yemmy) smo sešteli mesece, ko je oseba prejemala ta dohodek.  
Za samozaposlene in brezposelne osebe smo število mesecev prejemanja 
dohodka (ysemy) oziroma nadomestila (bunmy) določili na podlagi števila 
mesecev, ko so imeli posamezniki izbran status mesečne aktivnosti, če so 
prejemali dotičen letni dohodek. Število mesecev prejemanja posamezne vrste 
pokojnine (poamy, pdimy in psumy) smo določili glede na podatek o vrsti 
pokojnine, ki jo je oseba prejela v posameznem mesecu. Enako kot pri določitvi 
končnega števila mesecev prejemanja dohodka iz zaposlitve smo tudi v teh 
primerih sešteli mesece prejemanja posameznega dohodka, nadomestila oziroma 
pokojnine in tako osebi pripisali skupno število mesecev njihovega prejemanja v 
letu 2017.  
Število mesecev koriščenja posamezne pravice iz javnih sredstev v letu 2017 smo 
določili na podlagi seštetega obdobja prejemanja posamezne pravice v letu 2017, 
ki je bila odobrena na podlagi oddanih vlog s strani posameznika, družine ali 
gospodinjstva v tem letu. Na primer, za osebo, ki je oddala 3 vloge za koriščenje 
 
9 Upoštevali smo dohodke, pridobljene iz dohodninskih podatkov (vir eDURS), in neobdavčljive 
dohodke: invalidnino (vir eZPIZ), dodatek za pomoč in postrežbo (vir eZPIZ), starševski dodatek (vir 
eISCSD) in dodatek za nego otroka (vir eISCSD). 
10 Mesečni zneski dohodkov za obdobje treh koledarskih mesecev pred mesecem vložitve vloge so 
pripisani osebam, ki so oddali vloge za presojanje upravičenosti do pravic po ZSVarPre. 


 
35 
pravice do denarne socialne pomoči, smo skupaj sešteli vse dneve prejemanja 
pravice v letu 2017, ki so bili odobreni z vsako vlogo posebej.    
V vhodno bazo vnesemo mesečni znesek prejemka, pri čemer ne upoštevamo 
dejanskega števila mesecev prejemanja, ampak letni znesek delimo z 12, kar je 
skladno s konvencijo modeliranja EUROMOD. Tudi v rezultatih so mesečni zneski 
prejemkov izpisani na enak način, tako da do letnih zneskov pridemo, če jih 
pomnožimo z 12. Dejansko število mesecev prejemanja se upošteva pri 
posameznih preračunih v kodi modela.  
3.1.4 
Premoženje  
Premoženje, ki smo ga upoštevali, smo razvrstili v štiri skupine:   
- 
nepremično premoženje (stanovanje/hiša), 
- 
osebno vozilo, 
- 
prihranki, 
- 
vrednostni papirji in lastniški deleži. 
Za vse osebe, ki so oddale vlogo za uveljavljanje pravic iz javnih sredstev, smo 
podatke o premoženju pridobili iz IS CSD baz, medtem ko smo ostalim osebam 
podatke o premoženju pripisali na naslednji način:  
- 
vrednost nepremičnine (amrmv) smo pridobili iz registra nepremičnin; 
- 
vrednost osebnega vozila smo pripisali na podlagi izračuna povprečne 
vrednosti vozila iz IS CSD baze glede na znamko, model in leto prve 
registracije vozila; pri določitvi končne vrednosti osebnega vozila (acamv) 
smo upoštevali skupno vrednost vseh vozil, ki jih oseba ima;  
- 
vrednost prihrankov (adp) smo izračunali na podlagi podatka o letnem 
dohodku iz naslova obresti fizične osebe, doseženih na denarne depozite 
(šifra dohodka 5300), in upoštevanja obrestne mere za vezane vloge do 
2 leti za leto 2017; 
- 
vrednost vrednostnih papirjev in lastniških deležev (ash) smo izračunali 
na podlagi podatka o letnem dohodku iz naslova obresti in dividend (šifre 
dohodkov 5400–5900) in upoštevanja mediane donosa, ki smo ga 
izračunali sami na podlagi kontrolnih dohodninskih podatkov (šifre 
dohodkov 5400–5900) ter premoženja iz naslova vrednostnih papirjev in 
lastniških deležev iz IS CSD baz (donos = dohodek / premoženje). 


36 
EkonomIERa  
03-2023 
 
 


 
37 
4 
UPORABA MIKROSIMULACIJSKEGA MODELA 
SLOMOD 
Za mikrosimulacijski model davkov in socialnih transferjev so zelo pomembni 
vhodni podatki, katerih pripravo smo opisali v prejšnjem poglavju, in sam 
mikrosimulacijski model, s katerim modeliramo pravila za izračun posameznih 
socialnih transferjev in nadomestil plač.   
Mikrosimulacijski model davkov in socialnih transferjev SLOmod temelji na 
platformi EUROMOD. Univerza v Essexu je prva razvila statični mikrosimulacijski 
model EUROMOD, ki na primerljiv način omogoča izračune politik davkov in 
socialnih transferjev za posamezne države EU kot tudi na ravni EU. Primerljivost 
med državami je omogočena s kodiranjem politik (davčnih in socialnih) v vseh 
državah na način, ki sledi EUROMOD konvenciji o modeliranju. Od leta 2021 dalje 
je razvoj in upravljanje modela prevzelo Skupno raziskovalno središče (JRC) 
Evropske komisije v sodelovanju z Eurostatom in predstavniki nacionalnih skupin 
strokovnjakov. Za večino držav vhodni podatki, ki so osnova za delovanje modela, 
temeljijo na podatkih o dohodkih in življenjskih pogojih, ki jih objavlja Eurostat 
(EU-SILC). Pri nekaterih državah so podatki EU-SILC dopolnjeni z nacionalno 
verzijo SILC, v kateri so za določene spremenljivke pridobljeni podrobnejši 
podatki (v EU-SILC so podatki o določenih spremenljivkah zbrani na zelo visoki 
agregatni ravni). V EU-SILC bazi se demografski podatki nanašajo na čas 
anketiranja (prava polovica referenčnega leta), podatki o dohodkih in davkih pa 
se za večino držav nanašajo na koledarsko leto pred referenčnim letom. Dohodki 
se posodabljajo z ustreznimi faktorji spremembe vse do leta, za katerega želimo 
izvesti simulacije (na primer, ker se vhodni podatki nanašajo na leto 2020, 
simulirajo pa se politike leta 2022, se plače (in tudi ostali dohodki ter transferji) 
povečajo z rastjo plač med leti 2020 in 2022). EUROMOD se letno posodablja z 
novimi podatki raziskave SILC, faktorji sprememb in implementacijo sprememb 
politik za vsako državo. V modelu so implementirana pravila politik oziroma 
veljavnost zakonov, ki veljajo na dan 30. junij za dano leto.  
Podlaga modela je namensko izdelana programska oprema, ki vključuje 
uporabniku prijazen vmesnik. Vmesnik omogoča tudi dopolnitev osnovnega 
modela z dodatnimi moduli (npr. prilagoditev trga dela (LMA), neto 
nadomestitvena stopnja (NRR)) in razširitvenimi funkcijami (npr. prilagoditev 
koriščenja transferja, prilagoditev davčnih predpisov/obveznosti, prilagoditev 


38 
EkonomIERa  
03-2023 
covid-19) za posebne namenske analize. Model tako omogoča analizo vplivov 
dejanskih ali predpostavljenih sprememb politik skozi leta na mikro ravni. Na ta 
način lahko vidimo, kako spremembe davčnih in socialnih politik vplivajo na 
dohodke 
in 
socialne 
transferje 
oziroma 
razpoložljivi 
dohodek 
posameznika/gospodinjstva. EUROMOD programska platforma vsebuje tudi 
orodja za izpis rezultatov, s katerimi je mogoče analizirati in primerjati učinke 
različnih politik oziroma scenarijev. Poleg izpisa vrednosti posameznih izbranih 
dohodkov, socialnih transferjev in davkov ter njihovih sprememb so prikazani tudi 
nekateri izračuni, kot so npr. porazdelitev dohodka po decilnih razredih, stopnja 
tveganja revščine, kazalniki dohodkovne neenakosti (Ginijev količnik, razmerje 
kvintilnih razredov (80/20)). Za analizo izhodnih podatkov se lahko poleg 
vgrajenih orodij uporabi tudi druga statistična programska oprema.   
Platforma EUROMOD in sam model sta javno dostopna na spletni strani 
EUROMOD. Na ta način se želi pridobiti čim večje število uporabnikov modela iz 
različnih institucionalnih okolij in prispevati k zmanjševanju vrzeli med 
akademskim raziskovanjem in oblikovanjem politik. Več informacij o modelu 
EUROMOD je dostopnih na spletni strani EUROMOD (https://euromod-
web.jrc.ec.europa.eu/) in v članku avtorjev Sutherland in Figari (2013).  
Kot je bilo že omenjeno, vhodni podatki modela EUROMOD temeljijo na podatkih 
EU-SILC, medtem ko simulacije v modelu SLOmod temeljijo na registrskih in 
administrativnih podatkih (glej listo uporabljenih baz podatkov na začetku 
poglavja 0). Ker nam administrativni podatki podajajo podrobnejše informacije 
kot EU-SILC podatki, smo lahko obstoječe politike iz modela EUROMOD 
izpopolnili ter vpeljali simulacije novih socialnih transferjev ter tudi subvencij (vse 
vključene socialne transferje, nadomestila plač, davke in subvencije v nadaljevanju 
imenujemo politike):  
- 
državna štipendija; 
- 
subvencija malice; 
- 
subvencija kosila; 
- 
znižano plačilo vrtca; 
- 
subvencija najemnine; 
- 
pogrebnina; 
- 
posmrtnina. 


 
39 
Pri tem smo sledili prej omenjeni EUROMOD konvenciji o modeliranju. Skozi 
monografijo so pri posameznih spremenljivkah in politikah v oklepajih zapisana 
imena politik in spremenljivk (okrajšave), ki jih uporabljamo v modelu in so 
skladne s konvencijo. Podrobneje so vhodne spremenljivke modela SLOmod 
predstavljene v prilogi 1.  
V modelu SLOmod je pomemben vrstni red implementacije politik z vidika 
izračunov parametrov/spremenljivk, ki vplivajo na izračun drugih, naslednjih 
politik. Na primer, dohodnino moramo izračunati pred izračunom otroškega 
dodatka, saj za določitev upravičenosti in višine otroškega dodatka potrebujemo 
neto dohodek. Najprej definiramo parametre (spremenljivke, konstante, liste 
dohodkov, enote opazovanja itd.), ki so pomembni pri simulacij politik, nato 
simuliramo dohodke in prispevke, na podlagi katerih simuliramo dohodnino, 
temu pa sledijo izračuni socialnih transferjev glede na vrstni red uveljavljanja 
pravic po ZUPJS. Vrstni red izvajanja posameznih politik v modelu SLOmod, ki 
omogočajo simulacijo davkov in socialnih transferjev, je sledeč:  
1. Privzete vrednosti za spremenljivke (SetDefault_si). 
2. Uskladitveni faktorji (Uprate_SI). 
3. Določitev konstant (ConstDef_si). 
4. Standardne liste dohodkov (IlsDef_SI). 
5. Liste dohodkov (IlDef_SI). 
6. Naključna dodelitev vrednosti spremenljivkam (random_si). 
7. Tranzicije trga dela (TransLMA_si). 
8. Enota opazovanja/simulacije (TUDef_SI). 
9. Nenegativni dohodek (neg_si). 
10. Premoženje (asset_si). 
11. Minimalna plača (yem_si). 
12. Hipotetična gospodinjstva (hhot_switch_SI). 
13. Denarno nadomestilo za brezposelne (bunct_si). 
14. Materinsko in starševsko nadomestilo (bmact_si). 
15. Očetovsko nadomestilo (bcrbafh_si). 
16. Starševski dodatek (bmanc_si). 
17. Davek na pogodbeno delo (posebni davek na določene prejemke) 
(tpa_si). 
18. Prispevki za socialno varnost – delodajalec (tscer_si). 
19. Prispevki za socialno varnost – zavarovanec (tscee_si). 


40 
EkonomIERa  
03-2023 
20. Prispevki za socialno varnost – samozaposleni (tscse_si). 
21. Pravica do plačila prispevkov iz naslova krajšega delovnega časa ali 
zapustitve trga dela (tscctfa_si). 
22. Dohodninska olajšava (tinta01_si). 
23. Posebna dohodninska olajšava za vzdrževane člane (tinta02_si). 
24. Dohodnina; dohodninska olajšava, lestvica za odmero dohodnine, 
zmanjšanje dohodnine za upokojence in dohodnina od dohodka iz 
kapitala in dohodka iz oddajanja premoženja v najem (tin_si). 
25. Otroški dodatek (bchmt_si). 
26. Pomoč ob rojstvu otroka (bchba_si). 
27. Dodatek za veliko družino (bchlg_si). 
28. Mesečni dohodki za izračun denarne socialne pomoči (ymy_si). 
29. Denarna socialna pomoč (bsa_si). 
30. Varstveni dodatek (bsapm_si). 
31. Državna štipendija (bedmt_si). 
32. Subvencija malice (bedrd01_si). 
33. Subvencija kosila (bedrd02_si). 
34. Znižano plačilo vrtca (bchedyc_si). 
35. Subvencija najemnine (bho_si). 
36. Pogrebnina (bsafu_si). 
37. Posmrtnina (bsafu_si). 
38. Prispevki za socialno varnost na nadomestila plač in socialne 
transferje (tscct_si). 
Nekatere izmed navedenih politik so zelo tehnične narave in so v modelu zato, 
da se posamezni davki in pravice lahko računajo. Na primer, v politiki 
»uskladitveni faktorji« določimo, s katerim faktorjem spreminjamo posamezno 
vrsto dohodka. V politiki »naključna dodelitev vrednosti spremenljivkam« 
določimo slučajna števila, ki se uporabljajo pri posameznih pravicah. Vse politike 
z namenom posameznega socialnega transferja ali davka pa sledijo zakonodaji s 
ciljem določiti upravičenost do določenega socialnega transferja ter njegov 
znesek oziroma obveznost do plačila dohodnine ali socialnih prispevkov. Vse 
politike v modelu zajemajo obdobje 2017–2022. Ker podatki temeljijo na 
dohodkih iz leta 2017, vse dohodke ustrezno povečujemo/zmanjšamo z 
uskladitvenimi faktorji. Z njimi skušamo vrednost dohodka, premoženja in ne 


 
41 
simuliranih socialnih transferjev prilagoditi spremembam med posameznimi leti, 
ki izhajajo iz uradnih podatkov.  
Liste dohodkov nam omogočajo, da vnaprej pripravimo seznam vseh dohodkov, 
ki so pomembni za določeno politiko, in ni treba navajati posameznih dohodkov 
pri vsaki politiki posebej. Podrobneje so liste dohodkov opredeljene v prilogi 2. 
Podobno lahko kot konstanto shranimo zneske, ki se pogosto pojavljajo v modelu 
(npr. znesek osnovnega minimalnega dohodka). V primeru spremenjenega 
zneska lahko uporabnik popravi znesek konstante zgolj enkrat in ne povsod v 
modelu, kjer se uporablja.   
Preden se v naslednjem poglavju posvetimo validaciji rezultatov simulacij, je 
potrebno omeniti še prednost uporabe platforme EUROMOD pri definiranju 
opazovane enote. Kljub temu da omejitev glede sestave oziroma tipa 
gospodinjstva delno obidemo že v fazi priprave podatkov z iskanjem povezanih 
oseb in preoblikovanjem obstoječih oziroma oblikovanjem novih gospodinjstev 
in družin (podrobneje opisano v poglavju 3.1), ima uporaba platforme EUROMOD 
veliko prednost. Vsi člani enega gospodinjstva tvorijo eno enoto opazovanja, 
vendar pa lahko znotraj gospodinjstva določimo tudi podskupino gospodinjstva, 
ki je pomembna za simuliranje določene politike s področja davkov ali socialnih 
transferjev. Na primer, za simuliranje upravičenosti do otroškega dodatka 
definiramo podskupino gospodinjstva oziroma družino, ki jo sestavljajo starši in 
otroci do 18. leta, za simuliranje starševskih nadomestil pa definiramo podskupino 
gospodinjstva oziroma družino, ki jo sestavljajo starši in otroci, ki so stari eno leto 
ali manj. Na tak način lahko gospodinjstvo razdelimo na več opazovanih enot 
različnih velikosti (npr. gospodinjstvo sestavlja 6 oseb: starša z dvema šolajočima 
otrokoma in stari starši otrok, medtem ko podskupino za otroški dodatek 
sestavljajo 4 člani: starša z dvema šolajočima otrokoma). Poleg tega (lahko) 
vsakemu članu gospodinjstva določimo položaj v gospodinjstvu (nosilec 
gospodinjstva/družine (oseba z najvišjim dohodkom), partner, vzdrževani otrok, 
starš samohranilec, ostale odrasle osebe).  
 
 
 


42 
EkonomIERa  
03-2023 
 
 


 
43 
5 
VALIDACIJA MODELA SLOMOD 
V tem poglavju na podlagi primerjave rezultatov simulacij (na podlagi vhodne 
baze podatkov in modeliranih politik) z zunanjimi statistikami preverjamo 
uspešnost modela SLOmod za izračun davkov in socialnih transferjev. Opisane so 
nekatere pomembnejše politike in morebitna odstopanja med simuliranimi in 
mikropodatki oziroma zunanjimi podatki. Podana so tudi pojasnila, zakaj prihaja 
do ugotovljenih odstopanj. Rezultate primerjamo tako z vidika zneska kot tudi 
števila prejemnikov/upravičencev. V tem poglavju podrobneje opisujemo zgolj 
rezultate za leto 2017, rezultati za ostala leta pa so v prilogi 3. 
5.1 Dohodek, dohodnina in socialni prispevki 
Dohodkov, z izjemo mesečnih dohodkov za izračun denarne socialne pomoči, ki 
so delno simulirani, ne simuliramo v modelu. Kljub temu pa nam primerjava ne 
simuliranih dohodkov iz vhodne baze podatkov z zunanjimi podatki poda oceno 
o kakovosti začetnih podatkov, ki je osnova za vse nadaljnje analize. Poleg tega 
prispeva tudi k razumevanju in pojasnjevanju posameznih komponent simuliranih 
vrednosti, če so le-te odvisne tudi od ne simuliranih. Dohodki iz vhodne baze se 
dobro ujamejo z agregatnimi vrednostmi zunanjih podatkov (MF, 2019) tako z 
vidika zneska kot števila prejemnikov. Nekoliko izstopa dohodek verskih delavcev 
(yaj01), ki je precenjen. Gre za dohodek, ki ga prejme le majhen delež prebivalstva 
in predstavlja majhen delež celotnega dohodka, zato je razlika toliko opaznejša. 
Pri pokojninah se z zneski približamo zunanji statistiki, z izjemo pri družinskih in 
vdovskih pokojninah. Slabši rezultati so tudi pri številu prejemnikov družinskih in 
vdovskih kot tudi invalidskih pokojnin. Vendar podatki o številu upravičencev niso 
najbolj primerljivi, saj zunanja statistika podaja število vseh prejemnikov 
posamezne pokojnine v letu 2017, medtem ko v modelu zajamemo zgolj 
rezidente in ne tudi prejemnike pokojnin v tujini. Dodatne razlike nastajajo tudi 
zaradi štetja prejemnikov družinskih pokojnin (več upravičencev do ene 
pokojnine).  
Primerjava simulirane vrednosti dohodnine z zunanjimi podatki (MF, 2019) v 
tabelah 6 in 7 nakaže na dobre rezultate. Tako s simuliranim zneskom kot številom 
zavezancev za dohodnino se zelo približamo zunanjim podatkom. Simulirana 
vrednost zneska je podcenjena za 2 %, medtem ko je simulirano število 
zavezancev podcenjeno le za 1 %. 


44 
EkonomIERa  
03-2023 
Tudi simulirane vrednosti prispevkov za socialno varnost zavarovanca 
((samo)zaposlenega) kot tudi delodajalca v primerjavi z zunanjo statistiko (MF, 
2022b) nakazujejo na dobre rezultate. Primerjamo lahko le zneske, saj zunanjih 
podatkov o številu zavezancev za plačilo prispevkov nismo pridobili.  
Tabela 6: Ne simulirani dohodki in simulirana dohodnina v primerjavi z 
zunanjimi podatki – zneski (v EUR), leto 2017  
Dohodki, dohodnina in socialni prispevki 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji 
podatki (zp) 
Razmerje 
SLOmod/zp 
   
2017 
2017 
2017 
Obdavčljivi dohodek iz zaposlitve (plača) 
(yemtx) 
14.303.637.492 
14.288.760.270 
1,00 
Dohodki iz zaposlitve (yem) 
15.217.830.588 
n.p. 
n.p. 
Dohodek iz samozaposlitve (yse00) 
434.812.500 
417.954.421 
1,04 
Dohodek iz samozaposlitve – kmetijska 
dejavnost (yseag) 
104.455.644 
100.160.164 
1,04 
Dohodek iz samozaposlitve – normiranci 
(ysen) 
215.738.736 
n.p. 
n.p. 
Avtorski honorar (yro) 
5.620.992 
9.661.880 
0,58 
Dohodek študentov, upravičenih do 
posebne olajšave (yst) 
228.130.260 
246.539.513 
0,93 
Dohodek študentov, neupravičenih do 
posebne olajšave (ystw) 
5.011.188 
5.026.656 
1,00 
Dohodek iz dodatne zaposlitve 1 (yaj01) 
458.916 
394.269 
1,16 
Dohodek iz dodatne zaposlitve 2 (yaj02) 
215.336.892 
213.690.460 
1,01 
Starostna pokojnina (poa00) 
3.469.651.476 
3.335.366.665 
1,04 
Invalidska pokojnina (pdi00) 
466.785.228 
475.683.437 
0,98 
Družinska in vdovska pokojnina (psu00) 
368.034.300 
478.291.321 
0,77 
Dohodnina (il_itbase0) 
1.903.829.748 
1.938.000.000 
0,98 
Prispevki za socialno varnost za 
zaposlene (ils_sicee) 
3.278.909.208 
3.224.555.585 
1,02 
Prispevki za socialno varnost za 
delodajalce (ils_sicer) 
2.407.267.596 
2.387.094.039 
1,01 
Prispevki za socialno varnost za 
samozaposlene (ils_sicse) 
337.635.840 
329.051.050 
1,03 
Vir: MF (2019, 2022b), ZPIZ (2018) in lastni izračuni.  
 
 


 
45 
Tabela 7: Ne simulirani dohodki in simulirana dohodnina v primerjavi z 
zunanjimi podatki – število, leto 2017 
Dohodki, dohodnina in socialni 
prispevki 
Legenda: Razlika v razmerju:  
SLOmod 
Zunanji podatki 
(zp) 
Razmerje 
SLOmod/zp 
   
2017 
2017 
2017 
Obdavčljivi dohodek iz zaposlitve 
(plača)  
814.788 
820.343 
0,99 
Dohodki iz zaposlitve  
845.644 
n.p. 
n.p. 
Dohodek iz samozaposlitve (yse00) 
55.973 
63.335 
0,88 
Dohodek iz samozaposlitve – kmetijska 
dejavnost (yseag) 
116.130 
110.645 
1,05 
Dohodek iz samozaposlitve – 
normiranci (ysen) 
43.011 
n.p. 
n.p. 
Avtorski honorar (yro) 
7.200 
7.228 
1,00 
Dohodek študentov, upravičenih do 
posebne olajšave (yst) 
88.157 
97.102 
0,91 
Dohodek študentov, neupravičenih do 
posebne olajšave (ystw) 
1.874 
1.917 
0,98 
Dohodek iz dodatne zaposlitve 1 
(yaj01) 
74 
68 
1,09 
Dohodek iz dodatne zaposlitve 2 
(yaj02) 
115.439 
114.274 
1,01 
Starostna pokojnina (poa00) 
403.518 
440.247 
0,92 
Invalidska pokojnina (pdi00) 
67.474 
81.955 
0,82 
Družinska in vdovska pokojnina 
(psu00) 
57.491 
91.182 
0,63 
Dohodnina (il_itbase0) 
1.529.811 
1.538.121 
0,99 
Prispevki za socialno varnost za 
zaposlene (ils_sicee) 
970.541 
n.p. 
n.p. 
Prispevki za socialno varnost za 
delodajalce (ils_sicer) 
970.541 
n.p. 
n.p. 
Prispevki za socialno varnost za 
samozaposlene (ils_sicse) 
107.002 
n.p. 
n.p. 
Vir: MF (2019, 2022b), ZPIZ (2018) in lastni izračuni.  
Prav tako tudi primerjava simuliranih in zunanjih podatkov (MF, 2019) o 
porazdelitvi davčnih zavezancev po davčnih razredih kaže, da smo blizu zunanjim 
podatkom. V tabeli 8 prikazujemo simulirane in zunanje podatke za leto 2017. 
 
 


46 
EkonomIERa  
03-2023 
Tabela 8: Primerjava porazdelitve simulirane dohodnine po davčnih razredih z 
zunanjimi podatki, 2017 
 
SLOmod 
Zunanji podatki 
Davčni 
razred 
Znesek 
(v EUR) 
Struktura 
(v %) 
Na 
zavezanca 
(v EUR) 
Znesek 
(v EUR) 
Struktura 
(v %) 
Na 
zavezanca 
(v EUR) 
1 
230.670.996 
12,12 
217 
210.220.890 
10,8 
200 
2 
844.846.260 
44,38 
2.231 
884.842.916 
45,7 
2.212 
3 
541.445.304 
28,44 
7.116 
545.716.930 
28,2 
6.981 
4 
128.943.636 
6,77 
17.635 
125.501.770 
6,5 
17.337 
5 
157.923.564 
8,30 
42.361 
171.731.813 
8,9 
44.364 
Skupaj 
1.903.829.760* 
100 
1.244 
1.938.014.319 
100 
1.260 
Opombe: * Do razlik med skupnim zneskom dohodnine, navedenim v tabeli 6, prihaja zaradi 
zaokroževanja. Davčni razred 1 vključuje osnovo do 8.021,34 EUR. Davčni razred 2 vključuje osnovo 
nad 8.021,34 EUR do 20.400 EUR. Davčni razred 3 vključuje  osnovo nad 20.400 EUR do 48.000 EUR. 
Davčni razred 4 vključuje osnovo nad 48.000 EUR do 70.907,20 EUR. Davčni razred 5 vključuje osnovo 
nad 70.907,20 EUR. 
Vir: MF (2019) in lastni izračuni.  
Tabela 9: Primerjava porazdelitve simuliranega števila davčnih zavezancev po 
davčnih razredih z zunanjimi podatki, 2017 
 
SLOmod 
Zunanji podatki 
Davčni razred 
Število 
Struktura (v %) 
Število 
Struktura (v %) 
1 
1.063.933 
69,55 
1.048.884 
68,2 
2 
378.752 
24,76 
399.957 
26,0 
3 
76.087 
4,97 
78.170 
5,1 
4 
7.312 
0,48 
7.239 
0,5 
5 
3.728 
0,24 
3.871 
0,3 
Skupaj 
1.529.812* 
100 
1.538.121 
100 
Opomba: * Do razlik med skupnim zneskom dohodnine, navedenim v tabeli 7, prihaja zaradi 
zaokroževanja.  
Vir: MF (2019) in lastni izračuni.  
5.2 Socialni transferji in nadomestila 
V tem poglavju primerjamo rezultate mikrosimulacijskega modela SLOmod z 
mikropodatki (IS CSD baze) in zunanjimi podatki po posameznih pravicah, kar 
prikazujeta tudi tabeli 10 in 11. 


 
47 
Skupni simulirani znesek politik materinskega in starševskega ter očetovskega 
nadomestila je v primerjavi z zunanjimi podatki (MDDSZ, 2022) sicer nekoliko 
podcenjen (10 %), a ko primerjamo politiki ločeno z mikropodatki (podatki IS 
CSD), se z materinskim in starševskim nadomestilom dobro približamo 
mikropodatkom (podcenjenost simuliranega nadomestila se zmanjša na 3 %). 
Nekoliko slabši rezultati so v primeru očetovskega nadomestila, ki je v primerjavi 
z mikropodatki dokaj precenjeno. To je lahko posledica tega, ker smo v fazi 
priprave podatkov sami izračunali vrednost posamezne vrste starševskega 
nadomestila, saj podatki ne navajajo zneska, ampak osnovo za izračun 
starševskega nadomestila, ki v podatkih tudi ni podrobneje opredeljen po vrsti 
nadomestila (podrobneje opisano v poglavju 3.1.2). Število prejemnikov 
materinskega in starševskega ter očetovskega nadomestila je sicer močno 
precenjeno, če simulirane podatke primerjamo z zunanjimi. Vendar je treba 
upoštevati, da zunanja statistika podaja povprečno število prejemnikov na mesec 
in ne vseh, ki so bili v letu 2017 prejemniki enega ali drugega nadomestila. Zelo 
pa se približamo mikropodatkom v primeru materinskega in starševskega 
nadomestila (simulirani podatki so podcenjeni za 2 %), medtem ko je očetovsko 
nadomestilo v primerjavi z mikropodatki podcenjeno za več kot 20 %. Razlog bi 
lahko izhajal v oblikovanju gospodinjstev oziroma družin. Namreč, kljub temu da 
smo v fazi priprave podatkov povezovali »razdrte« družine, se nekateri popravki 
zaradi uporabe vzorca niso obdržali. Na ta način smo lahko izgubili očete, ki po 
registrskih podatkih sicer niso del družine, a so prejemali očetovsko nadomestilo 
za svojega otroka.   
Medtem ko je simulirani znesek starševskega dodatka malenkostno (4 %) 
podcenjen v primerjavi z zunanjimi podatki (MDDSZ, 2022), je v primerjavi z 
mikropodatki IS CSD baz nekoliko precenjen (19 %). Ob tem je treba opozoriti, da 
je višja simulirana vrednost starševskega dodatka glede na zneske v IS CSD bazah 
pričakovana, saj v modelu upoštevamo bruto znesek dodatka (252,04 EUR), v IS 
CSD bazah pa je  zaveden neto znesek. V primerjavi z zunanjimi podatki je 
starševski dodatek – podobno kot starševski nadomestili – močno precenjen 
zaradi enakega razloga, saj so zunanji podatki podani za povprečno mesečno 
število prejemnikov v letu 2017, simulirani rezultati pa se nanašajo na vse 
posameznike, ki so leta 2017 prejeli starševski dodatek. 


48 
EkonomIERa  
03-2023 
Pomoč ob rojstvu otroka in dodatek za veliko družino sta dobro simulirana. Obe 
pravici se od zunanjih (MDDSZ, 2022) kot tudi mikropodatkov ne razlikujeta za 
več kot 10 %.  
Otroški dodatek je v primerjavi s podatki IS CSD baz in tudi zunanjimi podatki 
(MDDSZ, 2022) nekoliko precenjen tako z vidika zneska kot števila upravičencev. 
Razlogov za razhajanje med simuliranimi in podatki IS CSD baz oziroma zunanjimi 
podatki je lahko več: 
1. Kljub popravkom/prilagoditvi sestave oziroma tipa gospodinjstev tudi z 
upoštevanjem gospodinjstev/družin iz vlog za uveljavljenje pravic iz 
javnih sredstev (IS CSD baze) še vedno prihaja do razhajanj med 
dejanskimi in registrskimi gospodinjstvi (glej poglavje 3.1). 
2. Uporaba vzorca (za osebe, ki niso bile izbrane v vzorec, so spregledani 
tudi naši popravki glede oblikovanja gospodinjstev).  
3. Za simulacijo otroškega dodatka v letu 2017 upoštevamo dohodke iz leta 
2017, dejansko pa se upoštevajo dohodki iz leta 2016 ali celo 2015.  
4. Za vse upravičence predvidevamo prejemanje otroškega dodatka celo 
leto. 
5. Vrednost upoštevanega premoženja v modelu se lahko razlikuje od 
vrednosti premoženja iz uradnih evidenc zaradi diskrecijske pravice 
socialnega delavca.  
6. Zunanji podatki so podani za povprečno mesečno število upravičencev v 
letu 2017.  
V okviru starševskih in družinskih transferjev prikazujemo tudi rezultate za pravici 
do plačila prispevkov zaradi koriščenja krajšega delovnega časa in zaradi 
zapustitve trga dela zaradi varovanja štirih ali več otrok. Simulirane vrednosti obeh 
pravic prav tako nakazujejo na dobre rezultate simulacij. Tako simulirani zneski 
kot tudi število oseb, ki koristijo eno ali drugo pravico, se le malo razlikujejo od 
zunanjih podatkov in mikropodatkov. Izjema je zgolj primerjava simuliranega 
števila staršev, ki koristi posamezno pravico, z zunanjimi podatki. Vendar v tem 
primeru podatki niso najbolj primerljivi, saj zunanji podatki podajajo povprečno 
letno število upravičencev, medtem ko simulirani podatki podajajo število vseh 
oseb, ki so v letu 2017 koristile eno ali drugo pravico.   


 
49 
Tabela 10: Simulirani starševski in družinski transferji v primerjavi z zunanjimi 
in mikropodatki (IS CSD baze) – zneski (v EUR), leto 2017 
Starševski in družinski transferji 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji 
podatki 
(zp) 
Razmerje 
SLOmod/zp 
Mikro-
podatki (IS 
CSD baze)* 
Razmerje 
SLOmod/ 
baze 
   
2017 
2017 
2017 
2017 
2017 
Očetovsko nadomestilo (bcrbafh_s) 
12.115.536 
232.638.011 
0,90 
8.648.244 
1,40 
Materinsko in starševsko nadomestilo 
(bmact_s) 
196.463.472 
201.708.504 
0,97 
Starševski dodatek (bmanc_s) 
9.631.980 
10.028.244 
0,96 
8.067.648 
1,19 
Pomoč ob rojstvu otroka (bchba_s) 
4.714.008 
4.406.082 
1,07 
4.304.952 
1,10 
Dodatek za veliko družino (bchlg_s) 
9.823.752 
10.850.225 
0,91 
10.756.332 
0,91 
Otroški dodatek (bchmt_s) 
274.133.772 234.773.171 
1,17 232.939.596 
1,18 
Plačilo prispevkov iz naslova krajšega 
delovnega časa (tscctfa01_s in 
tscctfa02_s) 
18.109.668 
17.630.201 
1,03 
17.509.200 
1,03 
Plačilo prispevkov zaradi zapustitve trga 
dela (tscctfa03_s in tscctfa04_s) 
3.369.132 
3.535.507 
0,95 
3.470.088 
0,97 
Opomba: * Mikropodatki so podatki, pridobljeni na osnovi povezovanja uporabljenih baz podatkov in 
lastnih preračunov. 
Vir: MDDSZ (2022) in lastni izračuni.  
Tabela 11: Simulirani starševski in družinski transferji v primerjavi z zunanjimi in 
mikropodatki (IS CSD baze) – število, leto 2017 
Starševski in družinski transferji 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  
podatki 
(zp) 
Razmerje 
SLOmod/zp 
Mikro-
podatki (IS 
CSD baze)* 
Razmerje 
SLOmod/ 
baze 
   
2017 
2017 
2017 
2017 
2017 
Očetovsko nadomestilo (bcrbafh_s) 
13.291 
21.704 
2,07 
17.363 
0,77 
Materinsko in starševsko nadomestilo 
(bmact_s) 
31.552 
32.343 
0,98 
Starševski dodatek (bmanc_s) 
5.825 
3.589 
1,62 
6.517 
0,89 
Pomoč ob rojstvu otroka (bchba_s) 
16.541 
15.429 
1,07 
15.365 
1,08 
Dodatek za veliko družino (bchlg_s) 
23.959 
26.722 
0,90 
26.137 
0,92 
Otroški dodatek (bchmt_s) 
298.687 
258.469 
1,16 
270.500 
1,10 
Plačilo prispevkov iz naslova krajšega 
delovnega časa (tscctfa01_s in 
tscctfa02_s) 
20.884 
14.138 
1,48 
20.444 
1,02 
Plačilo prispevkov zaradi zapustitve trga 
dela (tscctfa03_s in tscctfa04_s) 
1.407 
1.207 
1,17 
1.433 
0,98 
Opomba: * Mikropodatki so podatki, pridobljeni na osnovi povezovanja uporabljenih baz podatkov in 
lastnih preračunov. 
Vir: MDDSZ (2022) in lastni izračuni.  


50 
EkonomIERa  
03-2023 
Simulirane vrednosti subvencije šolske prehrane za učence in dijake ter znižanega 
plačila vrtca lahko primerjamo le z vidika števila prejemnikov, saj v bazah 
mikropodatkov (IS CSD baze) znesek subvencije ni podan (tabela 12). Število 
simuliranih prejemnikov pravice subvencionirane malice kot tudi kosila je bilo 
precenjeno glede na zunanje podatke (MIZŠ, 2022), zato smo vpeljali dodatne 
funkcije, ki upoštevajo predpostavko, da vsi potencialno upravičeni ne izkoristijo 
posamezne pravice. Določili smo delež upravičencev, ločeno za učence in dijake, 
ki ne zaprosijo za subvencijo malice, in delež učencev, ki ne zaprosijo za 
subvencijo kosila, pri tem pa smo zasledovali cilj priti čim bližje zunanji statistiki. 
Predpostavljamo namreč, da vsi, ki bi lahko bili upravičeni do subvencionirane 
prehrane, za subvencijo šolske prehrane ne zaprosijo. Delno pa lahko razloge za 
precenjenost najdemo tudi v že opisanih pojasnilih za precenjenost otroškega 
dodatka.  
S simulacijo števila upravičencev do subvencije vrtca se dobro približamo zunanji 
statistiki (SURS, 2022b) in skoraj popolnoma približamo mikropodatkom iz IS CSD 
baz. Pri tem je treba opozoriti, da so mikropodatki o številu upravičencev, tj. 
številu otrok, ki so bili v letu 2017 v vrtcu, dobljeni na podlagi podatka o trenutni 
izobrazbi (dec), ki smo jo dokončno določili sami (podrobneje opisano v poglavju 
3.1.1). Tudi simulirano število vrtčevskih otrok po starostnih skupinah (tako število 
otrok, starih 0–3 let, kot število otrok, starih 4–5 let) se dobro ujame z zunanjimi 
podatki (za prvo skupino je simulirano število precenjeno za 4 %, za drugo le 1 
%). Nekoliko le izstopa število najstarejše skupine otrok, kar je deloma posledica 
tega, da se zunanji podatki nanašajo na šolsko leto 2017/18, medtem ko 
simulirani podatki zajamejo vse otroke, ki so bili v letu 2017 vključeni v vrtec.  
 
 


 
51 
Tabela 12: Simulirana subvencija prehrane za učence in dijake ter znižano 
plačilo vrtca v primerjavi z zunanjimi in mikropodatki (IS CSD baze) – število, 
leto 2017 
Subvencija šolske prehrane in znižano 
plačilo vrtca  
Legenda: Razlika v razmerju:
SLOmod 
Zunanji  
podatki 
(zp) 
Razmerje 
SLOmod/zp 
Mikro-
podatki (IS 
CSD baze)* 
Razmerje 
SLOmod/ 
baze 
   
2017 
2017 
2017 
2017 
2017 
Subvencionirana malica (bedrd01_s) 
133.546 
137.637 
0,97 
n.p. 
n.p. 
Subvencionirano kosilo (bedrd02_s) 
39.947 
41.827 
0,96 
n.p. 
n.p. 
Znižano plačilo vrtca (bchedyc_s) 
94.582 
86.703 
1,09 
93.299 
1,01 
Opomba: * Mikropodatki so podatki, pridobljeni na osnovi povezovanja uporabljenih baz podatkov in 
lastnih preračunov. 
Vir: MIZŠ (2022), SURS (2022b) in lastni izračuni.  
Ker pri simulaciji pravice denarne socialne pomoči v primerjavi z mikro in 
zunanjimi podatki (MDDSZ, 2022) prihaja do velike precenjenosti tako z vidika 
zneska kot števila prejemnikov oziroma upravičencev, predpostavimo, da določen 
delež oseb, kljub temu da so na podlagi dohodka in premoženja upravičeni do 
pravice, zanjo ne zaprosijo. Na ta način se približamo zunanjim in mikropodatkom 
(IS CSD baze). Razlogov za razhajanje med simuliranimi in zunanjimi oziroma 
mikropodatki je lahko več: 
1. Za denarno socialno pomoč dejansko ne zaprosijo vse osebe oziroma 
gospodinjstva, ki bi bila upravičena do nje. Tudi če upravičenec zaprosi 
enkrat, ni nujno, da po treh mesecih ponovno zaprosi.  
2. Kljub popravkom/prilagoditvi sestave oziroma tipa gospodinjstev, tudi z 
upoštevanjem gospodinjstev/družin iz vlog za uveljavljenje pravic iz 
javnih sredstev (IS CSD baze), še vedno prihaja do razhajanj med 
dejanskimi in registrskimi gospodinjstvi (glej poglavje 3.1). 
3. Uporaba vzorca (zaradi tega so v neki meri spregledani tudi naši popravki 
glede oblikovanja gospodinjstev).  
4. Z izjemo uporabe mesečnih podatkov o plači, drugih dohodkih iz 
delovnega razmerja in regresu uporabljamo podatke o letnih dohodkih, 
za katere predpostavimo, da je dohodek enakomerno porazdeljen skozi 
vse leto. Mesečni dohodki so ob tej predpostavki enaki letnim 
dohodkom, deljenim z 12. Dejanski dohodkovni položaj posameznikov 


52 
EkonomIERa  
03-2023 
pa se lahko drastično spremeni znotraj enega leta in tako se trimesečno 
povprečje lahko močno razlikuje od letnega povprečja.   
5. Vrednost upoštevanega premoženja v modelu se lahko razlikuje od 
vrednosti premoženja iz uradnih evidenc zaradi diskrecijske pravice 
socialnega delavca.  
6. Neupoštevanje krivdnih razlogov pri simulaciji pravice. 
7. Zunanji podatki so podani za povprečno mesečno število upravičencev v 
letu 2017.  
Ob predpostavki, da vsi potencialno upravičeni ne zaprosijo za denarno socialno 
pomoč, simuliran znesek pravice ostaja nekoliko precenjen, medtem ko je 
simulirano število upravičencev nekoliko podcenjeno.  
Tako kot pri denarni socialni pomoči, tudi pri varstvenemu dodatku prihaja do 
precenjenosti simuliranih vrednosti v primerjavi z mikro (IS CSD baze) in zunanjimi 
podatki (MDSSZ, 2022). Zato tudi pri varstvenemu dodatku predpostavljamo, da 
vsi potencialni upravičenci ne zaprosijo za pravico. Osebe, ki pravice do 
varstvenega dodatka ne izkoristijo, kljub temu da bi bili glede na dohodke in 
premoženje lahko upravičeni, določimo podrobneje kot pri drugih pravicah. 
Osebe, ki pravice do varstvenega dodatka kljub potencialni upravičenosti ne 
izkoristijo, ločimo na skupino oseb, ki ima odrasle otroke, in skupino oseb, ki jih 
nima. Predpostavljamo, da osebe, ki so same upravičene do prejemanja 
varstvenega dodatka, a imajo odrasle otroke, v manjši meri zaprosijo za pravico 
kot tiste, ki jih nimajo. Tako v modelu različno predpostavimo delež oseb, ki ne 
zaprosi za varstveni dodatek glede na to, ali ima odraslega otroka ali ne. Razlogi 
za razhajanje med simuliranimi in zunanjimi oziroma mikropodatki so podobni 
kot pri denarni socialni pomoči.  
Simulirano število prejemnikov varstvenega dodatka, ob predpostavki, da vsi 
potencialno upravičeni ne zaprosijo za pravico, popolnoma ustreza podatkom iz 
IS CSD baz, le v primerjavi z zunanjimi podatki število ostaja nekoliko precenjeno 
(10 %). Simulirani znesek pravice postane nekoliko podcenjen, vendar ne več kot 
za 10 %.  
V okviru socialne pomoči smo simulirali tudi pravici pogrebnine in posmrtnine. 
Kot je že bilo opisano v poglavju 3.1.1, smo posameznikom za določitev 
upravičencev do obeh pravic pripisali izgubo ožjega družinskega člana (partnerja 
ali starša) v letu 2017 (dfa=1). Simulirani podatki so v primerjavi z mikropodatki 


 
53 
(IS CSD baze) precej podcenjeni. Rezultati so nekoliko boljši, če primerjamo 
simulirane vrednosti z zunanjimi statistikami (MDDSZ, 2022), vendar še vedno 
ostajajo podcenjeni. Eden izmed razlogov za podcenjenost simulacij je lahko v 
določitvi oseb, ki so v letu 2017 izgubile svojca, saj se podatki CRP nanašajo na 1. 
2. 2018, najverjetneje pa baza ne vsebuje podatkov o vseh osebah, ki so umrle v 
obdobju enega leta, upoštevajoč vse dni v letu 2017. 
Obe simulirani vrednosti državne štipendije, znesek in število upravičencev 
oziroma prejemnikov, sta nekoliko precenjeni v primerjavi z zunanjimi podatki 
(MDDSZ, 2022) in podatki IS CSD baz. V primeru primerjave števila upravičencev 
z zunanjimi podatki, kjer simulirana vrednost najvidneje presega zunanje podatke, 
je ponovno treba opozoriti, da zunanja statistika navaja povprečno mesečno 
število upravičencev do državne štipendije v letu 2017, medtem ko simulirani 
podatki zajemajo število vseh prejemnikov državne štipendije v letu 2017. V 
spodnjih dveh tabelah (tabeli 13 in 14) so za znesek in prejemnike štipendije 
prikazani še podrobnejši rezultati glede na osnovno štipendijo (štipendija brez 
dodatkov) in posamezni dodatek – dodatek za uspeh, bivanje in dodatek za 
posebne potrebe. 
Pravica subvencije najemnine je še ena izmed simuliranih pravic, ki je napram 
podatkom iz IS CSD baz in zunanji statistiki (MDDSZ, 2022) precej precenjena. 
Zato podobno kot pri denarni socialni pomoči in varstvenemu dodatku vpeljemo 
prilagoditev in predpostavko, da določen delež upravičenih gospodinjstev za 
pravico ne zaprosi. Prilagoditev naredimo v dveh korakih, in sicer: 1) 
predpostavimo, da vsi tisti, ki kljub potencialni upravičenosti ne zaprosijo za 
denarno socialno pomoč, ne zaprosijo za subvencijo najemnine, kljub temu da so 
do nje (glede na simulirane rezultate) upravičeni; 2) predpostavimo, da približno 
polovica upravičencev do subvencije najemnine za to pravico dejansko ne zaprosi. 
Na ta način se približamo mikro (IS CSD baze) in zunanjim podatkom. 
 
 


54 
EkonomIERa  
03-2023 
Tabela 13: Simulirana socialna pomoč, varstveni dodatek, državna štipendija in 
subvencija najemnine v primerjavi z zunanjimi in mikropodatki (IS CSD baze) – 
zneski (v EUR), leto 2017 
Socialna pomoč, varstveni dodatek, državna 
štipendija in subvencija najemnine 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  
podatki 
(zp) 
Razmerje 
SLOmod/z
p 
Mikro-
podatki (IS 
CSD baze)* 
Razmerje 
SLOmod/ 
baze 
   
2017 
2017 
2017 
2017 
2017 
Denarna socialna pomoč (bsa_s) 
193.938.168 176.190.360 
1,10 171.598.032 
1,13 
Varstveni dodatek (bsapm_s) 
25.219.800 
27.792.671 
0,91 
26.512.380 
0,95 
Državna štipendija (bedmt_s) 
83.400.528 
78.836.100 
1,06 
74.585.436 
1,12 
Državna štipendija – osnova 
(bedmt00_s) 
73.583.448 
n.p.  
n.p.  
65.583.768 
1,12 
Državna štipendija – dodatek za 
uspeh (bedmtadd1_s) 
3.256.920 
n.p.  
n.p.  
3.006.648 
1,08 
Državna štipendija – dodatek za 
bivanje (bedmtadd2_s) 
5.546.820 
n.p.  
n.p.  
4.916.064 
1,13 
Državna štipendija – dodatek za 
posebne potrebe (bedmtadd3_s) 
1.013.340 
n.p.  
n.p.  
873.312 
1,16 
Subvencija najemnine (bho_s) 
15.267.624 
15.563.207 
0,98 
15.270.744 
1,00 
Pogrebnina (bsafu_s) 
2.386.164 
3.039.730 
0,78 
3.316.416 
0,72 
Posmrtnina (bsawd_s) 
753.444 
944.110 
0,80 
1.106.220 
0,68 
Opomba: * Mikropodatki so podatki, pridobljeni na osnovi povezovanja uporabljenih baz podatkov in 
lastnih preračunov. 
Vir: MDDSZ (2022) in lastni izračuni.  
 
 


 
55 
Tabela 14: Simulirana socialna pomoč, varstveni dodatek, državna štipendija in 
subvencija najemnine v primerjavi z zunanjimi in mikropodatki (IS CSD baze) – 
število, leto 2017 
Socialna pomoč, varstveni dodatek, državna 
štipendija in subvencija najemnine 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  
podatki 
(zp) 
Razmerje 
SLOmod/z
p 
Mikro-
podatki (IS 
CSD baze)* 
Razmerje 
SLOmod/ 
baze 
   
2017 
2017 
2017 
2017 
2017 
Denarna socialna pomoč (bsa_s) 
66.640 
80.491 
0,83 
72.869 
0,91 
Varstveni dodatek (bsapm_s) 
18.086 
16.494 
1,10 
18.082 
1,00 
Državna štipendija (bedmt_s) 
75.721 
49.673 
1,52 
64.761 
1,17 
Državna štipendija – osnova 
(bedmt00_s) 
75.721 
n.p.  
n.p.  
64.761 
1,17 
Državna štipendija - dodatek za 
uspeh (bedmtadd1_s) 
17.507 
n.p.  
n.p.  
15.523 
1,13 
Državna štipendija - dodatek za 
bivanje (bedmtadd2_s) 
9.075 
n.p.  
n.p.  
8.002 
1,13 
Državna štipendija - dodatek za 
posebne potrebe (bedmtadd3_s) 
2.464 
n.p.  
n.p.  
2.100 
1,17 
Subvencija najemnine (bho_s) 
12.107 
10.863 
1,11 
12.999 
0,93 
Pogrebnina (bsafu_s) 
4.078 
5.178 
0,79 
5.626 
0,72 
Posmrtnina (bsawd_s) 
2.575 
3.206 
0,80 
3.738 
0,69 
Opomba: * Mikropodatki so podatki, pridobljeni na osnovi povezovanja uporabljenih baz podatkov in 
lastnih preračunov. 
Vir: MDDSZ (2022) in lastni izračuni.  
 
 


56 
EkonomIERa  
03-2023 
 
 


 
57 
6 
SIMULACIJE SCENARIJEV  
V tem poglavju na kratko povzemamo rezultate opravljenih simulacij z 
mikrosimulacijskem modelom SLOmod s ciljem oceniti učinke predpostavljenih 
reform sistema davkov in sistema socialnih transferjev. Ob tem je pomembno 
opozoriti, da gre za izključno hipotetične scenarije, s katerimi želimo prikazati 
uporabo/uporabnost modela in ne gre za nikakršen predlog reform. 
Predpostavili smo štiri scenarije: 
1. Scenarij 1 (S01): Osnovni znesek minimalnega dohodka je izenačen z 
zneskom praga tveganja revščine. 
2. Scenarij 2 (S02): Uveden je univerzalni otroški dodatek. 
3. Scenarij 3 (S03): Uvedena je enotna dohodninska stopnja v višini 25 %; 
vse olajšave ostanejo, kot so.  
4. Scenarij 4 (S04): Pri ugotavljanju materialnega položaja pri upravičenosti 
do pravic po ZUPJS je ukinjeno upoštevanje premoženja.    
Izračuni so prikazani na agregatni ravni za celotno populacijo za obdobje petih 
let (2017–2021). V prvem delu so prikazani prihodki in izdatki državnega 
proračuna (dohodnina in le simulirani socialni transferji) in število davčnih 
zavezancev oziroma upravičencev do posameznega socialnega transferja. Ker se 
dohodki gospodinjstev, kot so dohodek iz (samo)zaposlitve (yemtx, yse, yseag), 
dohodek iz študentskega dela (yst in ystw) ter dohodki iz pogodbenega razmerja 
(yaj01 in yaj02), ne spreminjajo pri nobenem scenariju, niso posebej predstavljeni 
v tabelah. Sledi prikaz dohodkovne porazdelitve po decilnih razredih glede na 
ekvivalentni razpoložljivi dohodek11. Razpoložljivi dohodek gospodinjstva obsega 
dohodke in socialne transferje, znižane za davke in prispevke za socialno varnost 
vseh članov gospodinjstva (podrobneje glej prilogo 1, kjer so opredeljene liste 
dohodkov). Prikazani so tudi kazalniki neenakosti porazdelitve dohodka (Ginijev 
količnik in razmerje kvintilnih razredov (80/20)) ter stopnja tveganja revščine. Vse 
tabele, vezane na simulacije posameznega scenarija, so prikazane na koncu 
posameznega scenarija oziroma poglavja.  
 
11 Za izračun ekvivalentnega razpoložljivega dohodka je uporabljena OECD-ejeva ekvivalenčna 
lestvica: prvi odrasli ima utež 1, otroci, mlajši od 14 let, imajo utež 0,3, drugi člani, stari 14 let ali več, 
pa imajo utež 0,5. 


58 
EkonomIERa  
03-2023 
Za zaključek še primerjamo vpliv predpostavljenih scenarijev na porazdelitev po 
dohodkovnih razredih za pravice, ki so vezane na uvrstitev v dohodkovni razred 
(otroški dodatek, znižano plačilo vrtca in državna štipendija), in za dohodnino. 
Prehode analiziramo tako z vidika števila prejemnikov/zavezancev kot tudi glede 
na izdatek (vrednost) pravice oziroma dohodnine.  
Vsak scenarij primerjamo z osnovnim scenarijem za vsako leto posebej. V 
osnovnem modelu smo na podlagi podatkov iz leta 2017 in takratne veljavne 
zakonodaje oblikovali sistem politik za izračun davkov in socialnih transferjev v 
letu 2017. Sisteme politik v naslednjih letih, 2018–202212, smo oblikovali na 
podlagi revaloriziranih vrednosti monetarnih spremenljivk (dohodkov in socialnih 
transferjev), ki smo jih dobili z upoštevanjem faktorjev sprememb, in ob 
upoštevanju zakonodajnih sprememb v posameznem letu. Na ta način ocenimo 
vpliv predpostavljenih sprememb v politikah davkov in socialnih transferjev na 
javne izdatke države in razpoložljivi dohodek posameznika. 
6.1 Scenarij 1: Minimalni dohodek  
V prvem scenariju (S01) osnovni znesek minimalnega dohodka (292,56 EUR v letu 
2017) močno zvišamo  in izenačimo z zneskom praga tveganja revščine (636 EUR 
v letu 2017). Z vidika fiskalnih vplivov bi se to odrazilo v povečanju izdatkov države 
za socialne transferje skozi vsa leta 2017–2021, saj bi se pričakovano znatno 
povečalo število upravičencev do denarne socialne pomoči in varstvenega 
dodatka. Močno bi se povečalo tudi število upravičencev do subvencije 
najemnine. Posledično bi se močno zvišali tudi višina posmrtnine in pogrebnine, 
saj je njuna višina vezana na osnovni znesek minimalnega dohodka. Izenačenje 
osnovnega zneska minimalnega dohodka z zneskom praga tveganja revščine bi 
prikrajšalo le upravičence do državne štipendije – teh bi bilo manj zaradi uvedbe 
predlagane reforme (S01) in posledično bi bili nižji tudi izdatki države za državno 
štipendijo. Spomnimo, da se po ZUPJS državno štipendijo uveljavlja kot zadnji 
denarni prejemek (po otroškem dodatku, denarni socialni pomoči in varstvenem 
dodatku). Čeprav minimalni dohodek neposredno ne vpliva na višino otroškega 
dodatka, ta scenarij za zelo majhen odstotek zviša število prejemnikov in vrednost 
otroškega dodatka. Po 19. členu ZUPJS se upošteva ugotovljena vrednost 
 
12 Leto 2022 ni vključeno v izračune tega dela, saj v času simulacij scenarijev (januar 2023) uradnih 
(popolnih) podatkov za leto 2022, ki bi nam omogočali smiselno primerjavo simuliranih rezultatov z 
zunanjo statistiko, še ni bilo na voljo. 


 
59 
premoženja, znižana za 48 osnovnih zneskov minimalnega dohodka. Na ta način 
se v S01 zniža upoštevana vrednost premoženja, kar vodi do večjega števila 
prejemnikov otroškega dodatka in za zelo majhno število oseb tudi višjo vrednost 
otroškega dodatka. Kot je že bilo napisano v uvodnem delu poglavja 0, 
sprememba v scenariju S01 ne vpliva na dohodke (iz dela) oseb. Podrobneje so 
rezultati predstavljeni v tabelah 15–20. 
Kot je razvidno iz tabele 17, bi se z uvedbo sprememb scenarija S01 povprečni 
ekvivalentni razpoložljivi dohodek povečal skozi celotno opazovano obdobje 
2017–2021, in sicer od 3,36 % v letu 2018 do 5,41 % v letu 2017. Po pričakovanjih 
bi se razpoložljivi dohodek najvidneje povišal v spodnji polovici decilnih razredov, 
še posebej v prvih dveh.  
Tabela zmagovalcev in poražencev (tabela 18) nakazuje, da bi z uvedbo 
predlaganega S01 po vseh decilnih razredih pridobil večji delež prebivalstva, imel 
višji razpoložljivi dohodek, kot izgubil, in sicer skozi celotno opazovano obdobje 
2017–2021. Pričakovano bi največ pridobilo prvih pet decilnih razredov, z drugim 
in tretjim decilnim razredom na vrhu, najmanj pa deveti in deseti decilni razred. 
Zelo majhen delež je tistih, ki bi na ta račun imeli nižji razpoložljivi dohodek, 
vendar pa ta delež v drugem decilu kljub temu ni povsem zanemarljiv. Predvsem 
gre za prejemnike nižje državne štipendije na račun višje denarne socialne 
pomoči.  
Kazalnika dohodkovne neenakosti, nižji Ginijev količnik in nižje razmerje kvintilnih 
razredov (kazalnik 80/20), kažeta na vidno izboljšanje dohodkovne porazdelitve 
ob uvedbi S01 (tabela 19). 
Tudi stopnje tveganja revščine13 bi se z uvedbo S01 izboljšale (znižale). 
Enočlanskemu gospodinjstvu (odrasli osebi, mlajši od 65 let, brez otrok) bi se 
stopnja tveganja revščine znižala za največ, in sicer v letu 2017 za 18,9 odstotne 
točke (z 41,5 % na 22,7 %) (tabela 20Tabela 20). 
 
13 Meja tveganja revščine je določena kot 60 % mediane ekvivalentnega razpoložljivega dohodka vseh 
gospodinjstev, kar velja za vse izračune v poročilu. 


60 
EkonomIERa  
03-2023 
Tabela 15: Simulirani podatki S01: Sprememba vrednosti socialnih transferjev v S01 glede na osnovni scenarij (v milijonih) 
 
Osnovni scenarij 
S01 
Sprememba v %*** S01/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 
2018 2019 2020 2021 2017 2018 2019 2020 2021 
2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
194 
236 
284 
294 
281 
908 
714 
935 1.016 1.017 368,4% 202,2% 228,8% 246,1% 262,6% 
+ otroški dodatek (bchmt_s) 
274 
281 
274 
277 
260 
275 
281 
275 
277 
260 
0,2% 
0,1% 
0,1% 
0,1% 
0,1% 
+ državna štipendija (bedmt_s) 
83 
77 
84 
85 
76 
72 
70 
75 
75 
67 
-13,4% 
-9,9% -10,1% -11,0% -12,0% 
+ pomoč ob rojstvu otroka* (bchba_s) 
5 
6 
6 
6 
7 
5 
6 
6 
6 
7 
0,1% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
10 
10 
11 
11 
11 
10 
10 
11 
11 
11 
0,1% 
0,0% 
0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
25 
35 
39 
39 
33 
349 
225 
287 
314 
314 1.282,3% 542,0% 626,1% 713,3% 840,1% 
+ subvencija najemnine (bho_s) 
15 
16 
20 
20 
20 
29 
26 
34 
34 
34 
89,1% 61,1% 66,2% 70,6% 72,6% 
+ posmrtnina (bsawd_s) 
1 
1 
1 
1 
1 
6 
6 
6 
6 
6 660,2% 339,6% 388,2% 411,3% 460,3% 
+ pogrebnina (bsafu_s) 
2 
3 
3 
3 
3 
7 
6 
7 
7 
7 177,7% 107,7% 127,1% 141,6% 154,9% 
+ starševski dodatek (bmanc_s) 
10 
10 
10 
10 
15 
10 
10 
10 
10 
15 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
196 
200 
253 
269 
285 
196 
200 
253 
269 
285 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
12 
12 
14 
15 
16 
12 
12 
14 
15 
16 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dohodnina (tin00_s) 
1.904 2.003 2.142 2.152 2.486 1.904 2.003 2.142 2.152 2.486 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon.   
Vir: Lastni izračuni. 
 
 
 


 
61 
Tabela 16: Simulirani podatki S01: Sprememba števila prejemnikov socialnih transferjev v S01 glede na osnovni scenarij (v 
tisočih) 
 
Osnovni scenarij 
S01 
Sprememba v %*** S01/osnovni 
scenarij 
Leto 
Socialni transferji in dohodnina 
2017 2018 2019 2020 2021 2017 2018 2019 2020 2021 
2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
67 
67 
78 
78 
73 
175 
140 
172 
177 
168 162,3% 110,5% 119,2% 125,6% 129,4% 
+ otroški dodatek (bchmt_s)# 
299 
348 
346 
345 
339 
299 
348 
346 
345 
339 0,12% 0,02% 0,03% 0,02% 0,02% 
+ državna štipendija (bedmt_s) 
76 
71 
82 
81 
74 
70 
67 
79 
77 
70 -7,22% -5,60% -4,09% -5,02% -6,33% 
+ pomoč ob rojstvu otroka* (bchba_s) 
17 
19 
19 
19 
19 
17 
19 
19 
19 
19 
0,1% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
24 
24 
27 
27 
27 
24 
24 
27 
27 
27 
0,1% 
0,0% 
0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
18 
25 
28 
26 
22 
85 
69 
80 
83 
80 372,7% 173,4% 189,6% 213,6% 260,4% 
+ subvencija najemnine (bho_s) 
12 
12 
15 
15 
15 
22 
18 
24 
24 
24 85,5% 47,9% 53,2% 57,0% 57,0% 
+ izredna denarna pomoč (bsaec) 
43 
43 
43 
43 
43 
43 
43 
43 
43 
43 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ posmrtnina (bsawd_s) 
3 
3 
3 
3 
3 
9 
9 
8 
8 
8 250,8% 156,2% 173,5% 179,2% 192,8% 
+ pogrebnina (bsafu_s) 
4 
4 
4 
4 
3 
5 
5 
5 
5 
5 27,8% 21,0% 27,0% 31,6% 33,1% 
+ starševski dodatek (bmanc_s) 
6 
6 
6 
6 
6 
6 
6 
6 
6 
6 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
31 
31 
31 
31 
31 
31 
31 
31 
31 
31 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
13 
13 
13 
13 
13 
13 
13 
13 
13 
13 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dohodnina (il_itbase0) 
1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon. # Za otroški dodatek simulirani podatki podajajo 
število upravičencev v posameznem letu.   
Vir: Lastni izračuni. 
 


62 
EkonomIERa  
03-2023 
Tabela 17: Simulirani podatki S01: Povprečni ekvivalentni razpoložljivi dohodek na člana gospodinjstva po decilih (v EUR) 
 
Osnovni scenarij 
S01 
Sprememba v % S01/Osnovni scenarij 
Leto 
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
3.321 
3.453 
3.763 
3.879 
3.982 
4.978 
4.253 
4.913 
5.167 
5.508 49,87% 23,17% 30,55% 33,19% 
38,33% 
2. decil 
6.587 
7.012 
7.251 
7.482 
7.749 
9.033 
8.721 
9.483 
9.961 
10.299 37,13% 24,38% 30,79% 33,14% 
32,91% 
3. decil 
8.314 
8.644 
8.903 
9.211 
9.669 
9.614 
9.634 
10.212 
10.634 
11.009 15,65% 11,46% 14,70% 15,45% 
13,85% 
4. decil 
9.690 
10.023 
10.326 
10.701 
11.292 
10.447 
10.523 
10.991 
11.451 
11.988 
7,82% 
4,99% 
6,44% 
7,01% 
6,16% 
5. decil 
10.947 
11.306 
11.667 
12.108 
12.823 
11.351 
11.550 
12.006 
12.490 
13.162 
3,68% 
2,16% 
2,91% 
3,15% 
2,65% 
6. decil 
12.242 
12.634 
13.053 
13.554 
14.387 
12.425 
12.736 
13.200 
13.731 
14.542 
1,49% 
0,81% 
1,13% 
1,30% 
1,07% 
7. decil 
13.659 
14.093 
14.566 
15.140 
16.118 
13.725 
14.128 
14.620 
15.205 
16.171 
0,48% 
0,25% 
0,37% 
0,43% 
0,32% 
8. decil 
15.407 
15.916 
16.459 
17.123 
18.280 
15.430 
15.931 
16.479 
17.144 
18.298 
0,14% 
0,09% 
0,12% 
0,12% 
0,10% 
9. decil 
18.041 
18.653 
19.313 
20.115 
21.502 
18.051 
18.661 
19.323 
20.127 
21.512 
0,06% 
0,04% 
0,05% 
0,06% 
0,04% 
10. decil 
28.287 
29.552 
31.728 
31.668 
33.781 
28.292 
29.554 
31.732 
31.673 
33.785 
0,02% 
0,01% 
0,01% 
0,01% 
0,01% 
Skupaj 
12.649 
13.128 
13.703 
14.098 
14.958 
13.334 
13.569 
14.296 
14.758 
15.627 
5,41% 
3,36% 
4,33% 
4,68% 
4,47% 
Vir: Lastni izračuni. 
 
 
 


 
63 
Tabela 18: Simulirani podatki S01: Zmagovalci in poraženci 
 
Zmagovalci 
Poraženci 
Leto  
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
37,3% 
26,0% 
32,3% 
33,0% 
34,6% 
0,1% 
0,1% 
0,0% 
0,0% 
0,1% 
2. decil 
49,1% 
44,1% 
50,7% 
51,6% 
49,4% 
1,5% 
2,5% 
2,1% 
2,0% 
1,7% 
3. decil 
40,8% 
37,3% 
42,9% 
43,3% 
41,3% 
0,1% 
0,4% 
0,4% 
0,3% 
0,3% 
4. decil 
35,5% 
30,2% 
35,2% 
36,3% 
34,3% 
0,1% 
0,1% 
0,1% 
0,1% 
0,1% 
5. decil 
27,4% 
21,1% 
25,5% 
26,7% 
23,5% 
0,1% 
0,1% 
0,0% 
0,0% 
0,1% 
6. decil 
18,1% 
10,3% 
13,3% 
14,9% 
12,6% 
0,1% 
0,1% 
0,0% 
0,0% 
0,0% 
7. decil 
7,3% 
4,2% 
5,7% 
6,6% 
5,3% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
8. decil 
2,3% 
1,5% 
1,9% 
1,9% 
1,6% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
9. decil 
0,9% 
0,8% 
0,9% 
1,0% 
0,8% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
10. decil 
0,3% 
0,3% 
0,4% 
0,3% 
0,3% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Skupaj 
24,9% 
20,0% 
23,8% 
24,5% 
23,4% 
0,2% 
0,4% 
0,3% 
0,3% 
0,3% 
Vir: Lastni izračuni. 
Tabela 19: Simulirani podatki S01: Kazalniki dohodkovne neenakosti 
 
Osnovni scenarij 
S01 
Leto  
Kazalnik 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
Ginijev koeficient 
0,2863 
0,2860 
0,2909 
0,2856 
0,2901 
0,2521 
0,2639 
0,2626 
0,2557 
0,2601 
Razmerje kvint. razr. (80/20) 
4,6754 
4,6060 
4,6337 
4,5578 
4,7124 
3,8768 
4,1131 
4,0085 
3,9090 
3,9950 
Vir: Lastni izračuni. 
 


64 
EkonomIERa  
03-2023 
Tabela 20: Simulirani podatki S01: Stopnje tveganja revščine 
 
Osnovni scenarij 
S01 
Razlika v odst. točkah 
S01-osnovni scenarij 
Leto 
Tip gospodinjstva 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1 odrasla os. <65, brez otrok 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
22,7% 
25,9% 
22,6% 
22,3% 
22,9% 
-18,9 
-13,9 
-17,0 
-17,4 
-18,4 
1 odrasla os. ≥65, brez otrok 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
21,0% 
22,1% 
20,7% 
19,8% 
21,1% 
-14,6 
-10,7 
-12,8 
-12,6 
-14,0 
1 odrasla os. z otroci 
30,1% 
28,2% 
27,3% 
28,2% 
30,9% 
17,9% 
21,0% 
18,3% 
18,6% 
19,4% 
-12,2 
-7,2 
-9,0 
-9,7 
-11,5 
2 odrasli os.<65, brez otrok  
15,8% 
15,3% 
15,4% 
15,5% 
15,8% 
9,7% 
10,6% 
9,7% 
9,7% 
9,9% 
-6,0 
-4,7 
-5,6 
-5,8 
-5,9 
2 odrasli os., vsaj 1 ≥65, brez 
otrok  
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
7,9% 
8,3% 
8,0% 
7,8% 
8,1% 
-4,1 
-3,1 
-3,5 
-3,6 
-3,7 
2 odrasli os., 1 otrok 
14,1% 
13,7% 
13,5% 
13,9% 
14,5% 
8,8% 
9,8% 
8,8% 
9,0% 
9,1% 
-5,3 
-3,8 
-4,6 
-4,9 
-5,3 
2 odrasli os., 2 otroka 
11,5% 
10,5% 
10,4% 
10,8% 
11,6% 
7,1% 
7,9% 
7,1% 
7,2% 
7,3% 
-4,4 
-2,5 
-3,3 
-3,7 
-4,3 
2 odrasli os., 3 ali več otrok 
16,1% 
14,3% 
13,8% 
14,8% 
16,3% 
10,2% 
11,7% 
10,5% 
10,7% 
11,0% 
-5,9 
-2,6 
-3,3 
-4,2 
-5,4 
3 ali več odraslih os., brez 
otrok 
7,5% 
7,2% 
7,3% 
7,5% 
7,7% 
5,1% 
5,4% 
5,2% 
5,2% 
5,4% 
-2,4 
-1,7 
-2,1 
-2,3 
-2,4 
3 ali več odraslih os. z otroci 
9,1% 
8,6% 
8,7% 
8,9% 
9,4% 
6,5% 
7,0% 
6,76 
6,7% 
7,0% 
-2,6 
-1,6 
-2,0 
-2,2 
-2,4 
Skupaj 
16,9% 
16,0% 
16,0% 
16,1% 
17,0% 
10,3% 
11,4% 
10,4% 
10,3% 
10,7% 
-6,6% 
-4,6 
-5,6 
-5,8 
-6,4 
Vir: Lastni izračuni. 
 
 


 
65 
6.2 Scenarij 2: Univerzalni otroški dodatek 
Pri drugem scenariju (S02) smo predpostavili uvedbo univerzalnega otroškega 
dodatka v višini 50 evrov za vsakega otroka. Z vidika državnega proračuna bi se 
to odrazilo v zmanjšanju skupnih izdatkov za socialne transferje v celotnem 
obdobju 2017–2021. Kljub temu da bi se število upravičencev do otroškega 
dodatka sicer povečalo, saj so po S02 do otroškega dodatka upravičeni vsi otroci 
do 18. leta, bi bili skupni izdatki države za otroški dodatek nižji, saj ta ni več 
odvisen od dohodka družine in števila otrok (oziroma vrstnega reda). Nekoliko bi 
se po S02 povišalo tudi število prejemnikov socialne pomoči, spremembe števila 
prejemnikov ostalih oblik pomoči pa so relativno manjše. Rezultati so podrobneje 
predstavljeni v spodnjih tabelah (tabele 21–26). 
Uvedba univerzalnega otroškega dodatka (S02) bi se sicer odrazila v minimalnem 
zmanjšanju povprečnega ekvivalentnega razpoložljivega dohodka v celotnem 
proučevanem obdobju. Vendar bi ta scenarij najmočneje vplival na razpoložljivi 
dohodek tistih z najnižjimi dohodki. Razpoložljivi dohodek bi se zmanjšal v 
celotnem opazovanem obdobju do vključno šestega decilnega razreda, z izjemo 
v šestem decilnem razredu v letu 2021. Najrevnejši (prvi decilni razred) bi v 
celotnem obdobju občutili znižanje razpoložljivega dohodka za približno 5 % 
(tabela 23). 
Iz tabele zmagovalcev in poražencev (tabela 24) je razvidno, da bi z uvedbo 
univerzalnega otroškega dodatka (S02) del prebivalstva pridobil, del pa izgubil. 
Razpoložljivi dohodek bi se v vseh letih povišal predvsem tistim v višjih decilnih 
razredih (od sedmega decila dalje bi bilo takšnih približno četrtina), medtem ko 
je v najnižjih dveh decilih zmagovalcev zanemarljivo malo. Na drugi strani je med 
poraženci zanemarljivo malo tistih v najvišjem decilu, največ pa jih ni v najnižjem, 
temveč v nižjih srednjih decilih. 
Pregled kazalnikov neenakosti pokaže, da bi se dohodkovna porazdelitev po 
uvedbi S02 nekoliko poslabšala. Poviša se razmerje kvintilnih razredov (kazalnik 
80/20) kot tudi Ginijev količnik, sicer v nekoliko manjši meri (tabela 25).  
Stopnja tveganja revščine bi z uvedbo univerzalnega otroškega dodatka (S02) 
ostala nespremenjena ali pa bi se nekoliko zvišala. To bi veljalo predvsem za 
gospodinjstva z eno odraslo osebo z otroci ter gospodinjstva z dvema odraslima 


66 
EkonomIERa  
03-2023 
osebama in tremi ali več otroci. Povečanje je v obeh primerih najvišje v letu 2017, 
ko se stopnja tveganja revščine poveča za 5,4 odstotne točke (tabela 26). 
 
 


 
 67 
Tabela 21: Simulirani podatki S02: Sprememba vrednosti socialnih transferjev v S02 glede na osnovni scenarij (v milijonih) 
 
Osnovni scenarij 
S02 
Sprememba v %*** S02/osnovni 
scenarij 
Leto 
Socialni transferji in dohodnina 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
194 
236 
284 
294 
281 
209 
251 
302 
312 
297 
7,7% 
6,5% 
6,3% 
6,3% 
5,9% 
+ otroški dodatek (bchmt_s) 
274 
281 
274 
277 
260 
222 
222 
222 
222 
222 -19,1% -21,0% -19,1% -19,9% -14,7% 
+ državna štipendija (bedmt_s) 
83 
77 
84 
85 
76 
84 
78 
84 
85 
77 
0,6% 
0,3% 
0,5% 
0,5% 
0,3% 
+ pomoč ob rojstvu otroka* (bchba_s) 
5 
6 
6 
6 
7 
5 
6 
6 
6 
7 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
10 
10 
11 
11 
11 
10 
10 
11 
11 
11 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
25 
35 
39 
39 
33 
25 
36 
40 
39 
34 
0,9% 
1,3% 
1,2% 
1,2% 
1,1% 
+ subvencija najemnine (bho_s) 
15 
16 
20 
20 
20 
16 
16 
20 
20 
20 
2,7% 
0,4% 
0,6% 
0,7% 
0,7% 
+ posmrtnina (bsawd_s) 
1 
1 
1 
1 
1 
1 
1 
1 
1 
1 
0,0% 
0,2% 
0,0% 
0,2% 
0,2% 
+ pogrebnina (bsafu_s) 
2 
3 
3 
3 
3 
2 
3 
3 
3 
3 
0,0% 
0,3% 
0,3% 
0,4% 
0,5% 
+ starševski dodatek (bmanc_s) 
10 
10 
10 
10 
15 
10 
10 
10 
10 
15 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
196 
200 
253 
269 
285 
196 
200 
253 
269 
285 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
12 
12 
14 
15 
16 
12 
12 
14 
15 
16 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dohodnina (tin00_s) 
1.904 2.003 2.142 2.152 2.486 1.904 2.003 2.142 2.152 2.486 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon.   
Vir: Lastni izračuni. 
 
 
 


68 
EkonomIERa  
03-2023 
Tabela 22: Simulirani podatki S02: Sprememba števila prejemnikov socialnih transferjev v S02 glede na osnovni scenarij (v 
tisočih) 
 
Osnovni scenarij 
S02 
Sprememba v %*** 
S02/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
67 
67 
78 
78 
73 
68 
68 
80 
80 
75 
2,6% 
1,9% 
1,8% 
1,8% 
1,7% 
+ otroški dodatek (bchmt_s)
 # 
299 
348 
346 
345 
339 
370 
370 
370 
370 
370 23,8% 
6,2% 
6,8% 
7,3% 
9,1% 
+ državna štipendija (bedmt_s) 
76 
71 
82 
81 
74 
75 
70 
82 
81 
74 -0,7% -1,1% -0, 5% -0,7% -0,8% 
+ pomoč ob rojstvu otroka* (bchba_s) 
17 
19 
19 
19 
19 
17 
19 
19 
19 
19 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
24 
24 
27 
27 
27 
24 
24 
27 
27 
27 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
18 
25 
28 
26 
22 
18 
25 
28 
27 
22 
0,9% 
0,6% 
0,5% 
0,5% 
0,4% 
+ subvencija najemnine (bho_s) 
12 
12 
15 
15 
15 
12 
12 
15 
15 
15 
1,0% 
0,0% 
0,3% 
0,2% 
0,2% 
+ posmrtnina (bsawd_s) 
3 
3 
3 
3 
3 
3 
3 
3 
3 
3 
0,0% 
0,2% 
0,0% 
0,2% 
0,2% 
+ pogrebnina (bsafu_s) 
4 
4 
4 
4 
3 
4 
4 
4 
4 
3 
0,0% 
0,3% 
0,3% 
0,4% 
0,5% 
+ starševski dodatek (bmanc_s) 
6 
6 
6 
6 
6 
6 
6 
6 
6 
6 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
31 
31 
31 
31 
31 
31 
31 
31 
31 
31 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
13 
13 
13 
13 
13 
13 
13 
13 
13 
13 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dohodnina (il_itbase0) 
1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon. # Za otroški dodatek simulirani podatki podajajo 
število upravičencev v posameznem letu.     
Vir: Lastni izračuni. 
 
 


 
 69 
Tabela 23: Simulirani podatki S02: Povprečni ekvivalentni razpoložljivi dohodek na člana gospodinjstva po decilih (v EUR) 
 
Osnovni scenarij 
S02 
Sprememba v % S02/osnovni scenarij 
Leto 
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
3.321 
3.453 
3.763 
3.879 
3.982 
3.149 
3.247 
3.573 
3.680 
3.789 
-5,20% 
-5,96% 
-5,06% 
-5,14% 
-4,84% 
2. decil 
6.587 
7.012 
7.251 
7.482 
7.749 
6.423 
6.861 
7.113 
7.339 
7.605 
-2,49% 
-2,14% 
-1,90% 
-1,91% 
-1,86% 
3. decil 
8.314 
8.644 
8.903 
9.211 
9.669 
8.156 
8.500 
8.769 
9.071 
9.542 
-1,90% 
-1,66% 
-1,51% 
-1,52% 
-1,32% 
4. decil 
9.690 
10.023 
10.326 
10.701 
11.292 
9.571 
9.920 
10.230 
10.604 
11.218 
-1,22% 
-1,03% 
-0,93% 
-0,90% 
-0,66% 
5. decil 
10.947 
11.306 
11.667 
12.108 
12.823 
10.869 
11.247 
11.616 
12.058 
12.794 
-0,71% 
-0,52% 
-0,43% 
-0,41% 
-0,23% 
6. decil 
12.242 
12.634 
13.053 
13.554 
14.387 
12.216 
12.618 
13.045 
13.545 
14.397 
-0,22% 
-0,13% 
-0,06% 
-0,07% 
0,07% 
7. decil 
13.659 
14.093 
14.566 
15.140 
16.118 
13.670 
14.110 
14.591 
15.165 
16.163 
0,08% 
0,12% 
0,17% 
0,17% 
0,27% 
8. decil 
15.407 
15.916 
16.459 
17.123 
18.280 
15.477 
15.967 
16.515 
17.179 
18.349 
0,45% 
0,32% 
0,34% 
0,33% 
0,38% 
9. decil 
18.041 
18.653 
19.313 
20.115 
21.502 
18.166 
18.722 
19.385 
20.188 
21.586 
0,70% 
0,37% 
0,37% 
0,36% 
0,39% 
10. decil 
28.287 
29.552 
31.728 
31.668 
33.781 
28.441 
29.680 
31.861 
31.805 
33.925 
0,54% 
0,43% 
0,42% 
0,43% 
0,43% 
Skupaj 
12.649 
13.128 
13.703 
14.098 
14.958 
12.614 
13.087 
13.670 
14.063 
14.937 
-0,28% 
-0,31% 
-0,24% 
-0,25% 
-0,15% 
Vir: Lastni izračuni. 
 
 
 


70 
EkonomIERa  
03-2023 
Tabela 24: Simulirani podatki S02: Zmagovalci in poraženci 
 
Zmagovalci 
Poraženci 
Leto  
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
0,2% 
0,0% 
0,0% 
0,0% 
0,1% 
11,4% 
12,7% 
12,1% 
12,2% 
12,0% 
2. decil 
0,6% 
0,3% 
0,4% 
0,5% 
0,7% 
15,7% 
15,4% 
15,0% 
15,0% 
15,1% 
3. decil 
1,8% 
2,2% 
2,6% 
3,0% 
4,3% 
20,5% 
20,3% 
19,5% 
19,1% 
18,0% 
4. decil 
5,1% 
6,5% 
7,0% 
7,6% 
8,8% 
20,3% 
18,9% 
18,3% 
17,9% 
16,7% 
5. decil 
10,6% 
11,2% 
11,4% 
11,7% 
13,1% 
19,5% 
18,6% 
18,3% 
17,8% 
15,9% 
6. decil 
13,6% 
14,8% 
15,5% 
16,0% 
19,5% 
17,1% 
15,6% 
14,8% 
14,1% 
10,8% 
7. decil 
18,2% 
21,3% 
22,7% 
23,4% 
26,8% 
13,7% 
10,0% 
8,7% 
7,6% 
4,5% 
8. decil 
25,8% 
26,4% 
27,1% 
27,2% 
28,5% 
5,4% 
3,9% 
3,4% 
3,1% 
2,2% 
9. decil 
25,0% 
25,2% 
25,6% 
25,7% 
26,4% 
2,3% 
1,8% 
1,7% 
1,6% 
1,4% 
10. decil 
24,3% 
24,5% 
24,9% 
25,1% 
25,2% 
0,8% 
0,7% 
0,6% 
0,6% 
0,5% 
Skupaj 
10,8% 
11,4% 
11,8% 
12,1% 
13,3% 
13,2% 
12,4% 
11,9% 
11,6% 
10,5% 
Vir: Lastni izračuni. 
Tabela 25: Simulirani podatki S02: Kazalniki dohodkovne neenakosti 
 
Osnovni scenarij 
S02 
Leto  
Kazalnik 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
Ginijev koeficient 
0,2863 
0,2860 
0,2909 
0,2856 
0,2901 
0,2925 
0,2916 
0,2959 
0,2906 
0,2947 
Razmerje kvint. razr. (80/20) 
4,6754 
4,6060 
4,6337 
4,5578 
4,7124 
4,8822 
4,7989 
4,8047 
4,7280 
4,8801 
Vir: Lastni izračuni. 
 


 
 71 
Tabela 26: Simulirani podatki S02: Stopnje tveganja revščine 
 
Osnovni scenarij 
S02 
Razlika v odst. točkah 
S02-osnovni scenarij 
Leto 
Tip gospodinjstva 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1 odrasla os. <65, brez otrok 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
0,0 
0,0 
0,0 
0,0 
0,0 
1 odrasla os. ≥65, brez otrok 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
0,0 
0,0 
0,0 
0,0 
0,0 
1 odrasla os. z otroci 
30,1% 
28,2% 
27,3% 
28,2% 
30,9% 
35,6% 
32,6% 
31,4% 
32,5% 
34,5% 
5,4 
4,3 
4,1 
4,3 
3,6 
2 odrasli os.<65, brez otrok  
15,8% 
15,3% 
15,4% 
15,5% 
15,8% 
15,8% 
15,3% 
15,4% 
15,5% 
15,8% 
0,0 
0,0 
0,0 
0,0 
0,0 
2 odrasli os., vsaj 1 ≥65, brez 
otrok  
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
0,0 
0,0 
0,0 
0,0 
0,0 
2 odrasli os., 1 otrok 
14,1% 
13,7% 
13,5% 
13,9% 
14,5% 
15,3% 
14,6% 
14,4% 
14,8% 
15,1% 
1,2 
1,0 
0,9 
0,9 
0,7 
2 odrasli os., 2 otroka 
11,5% 
10,5% 
10,4% 
10,8% 
11,6% 
13,8% 
12,8% 
12,6% 
13,0% 
13,5% 
2,3 
2,3 
2,2 
2,2 
2,0 
2 odrasli os., 3 ali več otrok 
16,1% 
14,3% 
13,8% 
14,8% 
16,3% 
21,5% 
18,8% 
18,2% 
19,4% 
20,9% 
5,4 
4,5 
4,4 
4,5 
4,6 
3 ali več odraslih os., brez 
otrok 
7,5% 
7,2% 
7,3% 
7,5% 
7,7% 
7,5% 
7,2% 
7,3% 
7,5% 
7,7% 
0,0 
0,0 
0,0 
0,0 
0,0 
3 ali več odraslih os. z otroci 
9,1% 
8,6% 
8,7% 
8,9% 
9,4% 
10,5% 
9,9% 
9,8% 
10,1% 
10,4% 
1,4 
1,3 
1,1 
1,2 
1,0 
Skupaj 
16,9% 
16,0% 
16,0% 
16,1% 
17,0% 
17,9% 
16,9% 
16,8% 
17,0% 
17,8% 
1,0 
0,9 
0,9 
0,9 
0,8 
Vir: Lastni izračuni. 
 
 


72 
EkonomIERa  
03-2023 
6.3 Scenarij 3: Enotna dohodninska stopnja 
Tretji scenarij (S03) predvideva uvedbo enotne dohodninske stopnje v višini 25 %, 
olajšave pa se ne spremenijo. Takšen scenarij bi se v celotnem obdobju 2017–
2021 fiskalno odrazil v proračunskih prihrankih kot rezultat znatnega povečanja 
proračunskih prejemkov iz naslova dohodnine (od 11,8 % v 2019 do največ 16,4 
% v letu 2020). V povprečju višja dohodnina pomeni nižji povprečni neto dohodek 
in več upravičencev do (višjih) socialnih transferjev, a bi bilo povečanje izdatkov 
za socialne transferje manjše od povečanja prejemkov na račun več pobrane 
dohodnine. Povečanje izdatkov za socialne transferje bi bila predvsem posledica 
povečanja števila prejemnikov državne štipendije v vseh letih (za okoli 4 % v 
vsakem letu), v obdobju 2018–2021 pa bi prišlo tudi do majhnega povečanja 
števila prejemnikov subvencije najemnine. S03 ne privede do vidnih razlik pri 
upravičenosti do denarne socialne pomoči, saj njeni prejemniki ne plačujejo 
dohodnine (osnova za dohodnino je nižja od olajšav). Rezultati so podrobneje 
predstavljeni v spodnjih tabelah (tabele 27–32). 
Z uvedbo S03 bi se povprečni ekvivalentni razpoložljivi dohodek skozi celotno 
proučevano obdobje nekoliko zmanjšal. Razpoložljivi dohodek bi se zmanjšal 
veliki večini, zvišal bi se le tistim iz desetega decilnega razreda – skozi celotno 
opazovano obdobje bi se jim razpoložljivi dohodek povišal za več kot odstotek (z 
izjemo leta 2020).  
Tabela zmagovalcev in poražencev (tabela 30) kaže, da bi z uvedbo enotne 
dohodninske stopnje največ pridobili predstavniki zadnjega, desetega decilnega 
razreda, saj bi se razpoložljivi dohodek pri takšnem scenariju v vseh proučevanih 
letih povišal predvsem oziroma le predstavnikom tega razreda. Vsem osebam v 
najvišjem decilnem razredu se razpoložljiv dohodek ne bi povečal, saj bi bil tudi v 
desetem decilnem razredu delež poražencev nekoliko višji od deleža 
zmagovalcev. V vseh preostalih decilnih razredih bi bil delež poražencev občutno 
večji od deleža zmagovalcev. V sedmem, osmem in devetem decilnem razredu je 
delež tistih, ki bi se jim z uvedbo enotne dohodninske stopnje razpoložljivi 
dohodek zmanjšal, v vseh letih opazovanega obdobja 2017–2021 celo višji od 90 
%. V prvem decilnem razredu se razpoložljivi dohodek ne bi spremenil skoraj 
nikomur. 


 
 73 
Uvedba S03 ne bi bistveno vplivala na dohodkovno porazdelitev. Oba kazalnika 
dohodkovne neenakosti bi se sicer nekoliko povečala, vendar sta tako 
sprememba Ginijevega koeficienta kot tudi sprememba razmerja kvintilnih 
razredov (kazalnik 80/20) le minimalni (tabela 31).  
Tudi pri stopnji tveganja revščine z uvedbo S03 ne bi prišlo do pomembnih 
sprememb. Stopnja tveganja revščine bi pri vseh različnih tipih gospodinjstev 
ostala v vseh letih bolj ali manj nespremenjena (tabela 32). 
 


74 
EkonomIERa  
03-2023 
Tabela 27: Simulirani podatki S03: Sprememba vrednosti socialnih transferjev v S03 glede na osnovni scenarij (v milijonih) 
 
Osnovni scenarij 
S03 
Sprememba v %*** 
S03/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 2018 2019 2020 2021 2017 2018 2019 2020 2021 2017 
2018 
2019 
2020 2021 
+ socialna pomoč (bsa_s) 
194 
236 
284 
294 
281 
194 
236 
284 
294 
281 0,0% 0,0% 0,0% 0,0% 0,0% 
+ otroški dodatek (bchmt_s) 
274 
281 
274 
277 
260 
283 
288 
281 
284 
268 3,1% 2,4% 2,4% 2,7% 3,0% 
+ državna štipendija (bedmt_s) 
83 
77 
84 
85 
76 
87 
81 
87 
88 
80 4,5% 4,7% 4,3% 4,6% 4,7% 
+ pomoč ob rojstvu otroka* (bchba_s) 
5 
6 
6 
6 
7 
5 
6 
6 
6 
7 1,9% 0,0% 0,0% 0,0% 0,0% 
+ dodatek za veliko družino** (bchlg_s) 
10 
10 
11 
11 
11 
10 
10 
11 
11 
11 1,0% 0,6% 0,0% 0,0% 0,0% 
+ varstveni dodatek (bsapm_s) 
25 
35 
39 
39 
33 
25 
35 
40 
39 
34 0,0% 0,3% 0,4% 0,4% 0,4% 
+ subvencija najemnine (bho_s) 
15 
16 
20 
20 
20 
15 
16 
21 
20 
21 1,4% 2,3% 2,9% 3,1% 4,2% 
+ posmrtnina (bsawd_s) 
1 
1 
1 
1 
1 
1 
1 
1 
1 
1 0,4% 2,8% 1,4% 0,5% 1,3% 
+ pogrebnina (bsafu_s) 
2 
3 
3 
3 
3 
2 
3 
3 
3 
3 1,4% 0,5% 0,5% 0,4% 1,2% 
+ starševski dodatek (bmanc_s) 
10 
10 
10 
10 
15 
10 
10 
10 
10 
15 0,0% 0,0% 0,0% 0,0% 0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
196 
200 
253 
269 
285 
196 
200 
253 
269 
285 0,0% 0,0% 0,0% 0,0% 0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
12 
12 
14 
15 
16 
12 
12 
14 
15 
16 0,0% 0,0% 0,0% 0,0% 0,0% 
+ dohodnina (tin00_s) 
1.904 2.003 2.142 2.152 2.486 2.164 2.254 2.395 2.505 2.848 13,7% 12,6% 11,8% 16,4% 14,6% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon.   
Vir: Lastni izračuni. 
 
 


 
 75 
Tabela 28: Simulirani podatki S03: Sprememba števila prejemnikov socialnih transferjev v S03 glede na osnovni scenarij (v 
tisočih) 
 
Osnovni scenarij 
S03 
Sprememba v %*** 
S03/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 2018 2019 2020 2021 2017 2018 2019 2020 2021 2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
67 
67 
78 
78 
73 
67 
67 
78 
78 
73 0,0% 
0,0% 
0,0% 
0,0% 0,0% 
+ otroški dodatek (bchmt_s)# 
299 
348 
346 
345 
339 
305 
348 
346 
346 
340 2,0% 
0,0% 
0,0% 
0,3% 0,4% 
+ državna štipendija (bedmt_s) 
76 
71 
82 
81 
74 
79 
74 
85 
85 
78 4,5% 
4,9% 
3,7% 
4,1% 4,8% 
+ pomoč ob rojstvu otroka* (bchba_s) 
17 
19 
19 
19 
19 
17 
19 
19 
19 
19 1,9% 
0,0% 
0,0% 
0,0% 0,0% 
+ dodatek za veliko družino** (bchlg_s) 
24 
24 
27 
27 
27 
24 
24 
27 
27 
27 1,0% 
0,6% 
0,0% 
0,0% 0,0% 
+ varstveni dodatek (bsapm_s) 
18 
25 
28 
26 
22 
18 
25 
28 
27 
22 0,1% 
0,2% 
0,2% 
0,3% 0,2% 
+ subvencija najemnine (bho_s) 
12 
12 
15 
15 
15 
12 
13 
16 
16 
16 0,7% 
3,1% 
4,2% 
4,4% 4,2% 
+ posmrtnina (bsawd_s) 
3 
3 
3 
3 
3 
3 
3 
3 
3 
3 0,4% 
2,8% 
1,4% 
0,5% 1,3% 
+ pogrebnina (bsafu_s) 
4 
4 
4 
4 
3 
4 
4 
4 
4 
3 1,4% 
0,5% 
0,6% 
0,4% 1,2% 
+ starševski dodatek (bmanc_s) 
6 
6 
6 
6 
6 
6 
6 
6 
6 
6 0,0% 
0,0% 
0,0% 
0,0% 0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
31 
31 
31 
31 
31 
31 
31 
31 
31 
31 0,0% 
0,0% 
0,0% 
0,0% 0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
13 
13 
13 
13 
13 
13 
13 
13 
13 
13 0,0% 
0,0% 
0,0% 
0,0% 0,0% 
+ dohodnina (il_itbase0) 
1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 0,0% 
0,0% 
0,0% 
0,0% 0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon. # Za otroški dodatek simulirani podatki podajajo 
število upravičencev v posameznem letu.   
Vir: Lastni izračuni. 
 
 


76 
EkonomIERa  
03-2023 
Tabela 29: Simulirani podatki S03: Povprečni ekvivalentni razpoložljivi dohodek na člana gospodinjstva po decilih (v EUR) 
 
Osnovni scenarij 
S03 
Sprememba v %*** 
S03-osnovni scenarij 
Leto 
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
3.321 
3.453 
3.763 
3.879 
3.982 
3.320 
3.451 
3.760 
3.875 
3.976 
-0,05% 
-0,06% 
-0,09% 
-0,10% 
-0,13% 
2. decil 
6.587 
7.012 
7.251 
7.482 
7.749 
6.562 
6.981 
7.214 
7.442 
7.697 
-0,38% 
-0,43% 
-0,51% 
-0,53% 
-0,67% 
3. decil 
8.314 
8.644 
8.903 
9.211 
9.669 
8.223 
8.550 
8.797 
9.090 
9.513 
-1,09% 
-1,09% 
-1,19% 
-1,31% 
-1,61% 
4. decil 
9.690 
10.023 
10.326 
10.701 
11.292 
9.529 
9.855 
10.138 
10.495 
11.050 
-1,66% 
-1,68% 
-1,82% 
-1,92% 
-2,15% 
5. decil 
10.947 
11.306 
11.667 
12.108 
12.823 
10.710 
11.061 
11.400 
11.808 
12.467 
-2,17% 
-2,16% 
-2,29% 
-2,48% 
-2,78% 
6. decil 
12.242 
12.634 
13.053 
13.554 
14.387 
11.912 
12.301 
12.694 
13.145 
13.935 
-2,70% 
-2,64% 
-2,75% 
-3,02% 
-3,15% 
7. decil 
13.659 
14.093 
14.566 
15.140 
16.118 
13.249 
13.678 
14.141 
14.648 
15.592 
-3,0% 
-2,94% 
-2,92% 
-3,25% 
-3,27% 
8. decil 
15.407 
15.916 
16.459 
17.123 
18.280 
14.947 
15.453 
15.988 
16.561 
17.698 
-2,99% 
-2,91% 
-2,86% 
-3,28% 
-3,19% 
9. decil 
18.041 
18.653 
19.313 
20.115 
21.502 
17.573 
18.195 
18.865 
19.521 
20.917 
-2,59% 
-2,46% 
-2,32% 
-2,95% 
-2,72% 
10. decil 
28.287 
29.552 
31.728 
31.668 
33.781 
28.684 
30.017 
32.279 
31.927 
34.216 
1,40% 
1,57% 
1,74% 
0,82% 
1,29% 
Skupaj 
12.649 
13.128 
13.703 
14.098 
14.958 
12.471 
12.954 
13.528 
13.851 
14.706 
-1,41% 
-1,33% 
-1,28% 
-1,75% 
-1,69% 
Vir: Lastni izračuni. 
 
 
 


 
 77 
Tabela 30: Simulirani podatki S03: Zmagovalci in poraženci 
 
Zmagovalci 
Poraženci 
Leto  
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
0,8% 
1,1% 
1,7% 
1,5% 
1,9% 
2. decil 
0,2% 
0,2% 
0,2% 
0,1% 
0,3% 
13,3% 
16,7% 
18,5% 
14,4% 
16,9% 
3. decil 
0,5% 
0,6% 
0,7% 
0,6% 
0,7% 
44,9% 
44,2% 
45,8% 
43,5% 
46,9% 
4. decil 
0,7% 
0,9% 
0,6% 
0,7% 
0,5% 
56,3% 
57,1% 
57,6% 
55,8% 
58,2% 
5. decil 
0,7% 
0,7% 
0,5% 
0,4% 
0,3% 
69,3% 
67,0% 
70,8% 
73,3% 
81,7% 
6. decil 
0,6% 
0,5% 
0,5% 
0,4% 
0,4% 
86,3% 
85,0% 
86,8% 
88,3% 
91,7% 
7. decil 
0,7% 
0,6% 
1,1% 
0,5% 
0,5% 
93,9% 
92,9% 
93,7% 
95,5% 
97,7% 
8. decil 
1,5% 
1,5% 
1,9% 
0,4% 
1,0% 
96,8% 
96,4% 
96,5% 
98,3% 
98,0% 
9. decil 
4,2% 
4,6% 
5,5% 
2,1% 
3,2% 
95,0% 
94,4% 
93,6% 
97,2% 
96,3% 
10. decil 
39,5% 
41,9% 
44,9% 
29,6% 
35,3% 
59,4% 
56,9% 
53,7% 
69,3% 
63,8% 
Skupaj 
4,3% 
4,5% 
4,9% 
3,1% 
3,7% 
55,1% 
55,0% 
55,8% 
57,2% 
58,8% 
Vir: Lastni izračuni. 
Tabela 31: Simulirani podatki S03: Kazalniki dohodkovne neenakosti 
 
Osnovni scenarij 
S03 
Leto  
Kazalnik 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
Ginijev koeficient 
0,2863 
0,2860 
0,2909 
0,2856 
0,2901 
0,2892 
0,2893 
0,2948 
0,2878 
0,2937 
Razmerje kvint. razr. (80/20) 
4,6754 
4,6060 
4,6337 
4,5578 
4,7124 
4,6830 
4,6237 
4,6628 
4,5482 
4,7256 
Vir: Lastni izračuni. 
 


78 
EkonomIERa  
03-2023 
Tabela 32: Simulirani podatki S03: Stopnje tveganja revščine 
 
Osnovni scenarij 
S03 
Razlika v odst. točkah 
Leto 
Tip gospodinjstva 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1 odrasla os. <65, brez otrok 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
41,6% 
39,9% 
39,7% 
39,7% 
41,4% 
0,0 
0,1 
0,2 
0,0 
0,1 
1 odrasla os. ≥65, brez otrok 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
0,0 
0,0 
0,0 
0,0 
0,0 
1 odrasla os. z otroci 
30,1% 
28,2% 
27,3% 
28,2% 
30,9% 
30,3% 
28,5% 
27,7% 
28,9% 
32,2% 
0,2 
0,2 
0,4 
0,6 
1,3 
2 odrasli os.<65, brez otrok  
15,8% 
15,3% 
15,4% 
15,5% 
15,8% 
16,2% 
15,7% 
15,9% 
16,1% 
16,4% 
0,4 
0,4 
0,5 
0,6 
0,6 
2 odrasli os., vsaj 1 ≥65, brez 
otrok  
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
0,0 
0,0 
0,0 
0,0 
0,1 
2 odrasli os., 1 otrok 
14,1% 
13,7% 
13,5% 
13,9% 
14,5% 
14,7% 
14,2% 
14,1% 
14,5% 
15,2% 
0,6 
0,6 
0,6 
0,7 
0,7 
2 odrasli os., 2 otroka 
11,5% 
10,5% 
10,4% 
10,8% 
11,6% 
11,8% 
10,8% 
10,8% 
11,3% 
12,1% 
0,3 
0,4 
0,4 
0,5 
0,6 
2 odrasli os., 3 ali več otrok 
16,1% 
14,3% 
13,8% 
14,8% 
16,3% 
16,2% 
14,4% 
14,1% 
15,0% 
16,6% 
0,1 
0,2 
0,3 
0,1 
0,3 
3 ali več odraslih os., brez 
otrok 
7,5% 
7,2% 
7,3% 
7,5% 
7,7% 
7,7% 
7,4% 
7,5% 
7,7% 
8,0% 
0,2 
0,2 
0,3 
0,2 
0,3 
3 ali več odraslih os. z otroci 
9,1% 
8,6% 
8,7% 
8,9% 
9,4% 
9,3% 
8,8% 
8,8% 
9,1% 
9,6% 
0,2 
0,2 
0,2 
0,2 
0,3 
Skupaj 
16,9% 
16,0% 
16,0% 
16,1% 
17,0% 
17,1% 
16,2% 
16,2% 
16,4% 
17,4% 
0,2 
0,2 
0,3 
0,3 
0,4 
Vir: Lastni izračuni. 
 
 


 
 79 
6.4 Scenarij 4: Neupoštevanje premoženja po ZUPJS 
Po četrtem scenariju (S04) smo pri ugotavljanju materialnega položaja pri 
upravičenosti do pravic po ZUPJS ukinili upoštevanje premoženja14. V tem 
primeru bi se v vseh opazovanih letih nekoliko povečali izdatki države za socialne 
transferje, katerih upravičenost oziroma materialni položaj posameznika/družine 
se presoja na podlagi ZUPJS. Izdatki bi se povečali predvsem na račun večjega 
števila prejemnikov otroškega dodatka in državne štipendije. V letu 2017 je bila 
na dohodek in premoženje družine vezana tudi pravica pomoč ob rojstvu otroka, 
v letih 2017 in 2018 pa tudi pravica dodatek za veliko družino, zato se vpliv 
neupoštevanja premoženja vidi tudi pri simulacij teh dveh pravic v omenjenih 
letih. Podrobneje so rezultati predstavljeni v spodnjih tabelah (tabele 33–38). 
Uvedba S04 bi se odrazila v zanemarljivem povečanju povprečnega 
ekvivalentnega razpoložljivega dohodka v celotnem obdobju 2017–2021. Uvedba 
S04 bi spremenila višino posameznih socialnih transferjev za majhno število oseb, 
zato bi bilo število zmagovalcev zanemarljivo majhno. V vseh decilnih razredih v 
celotnem obdobju 2017–2021 je le minimalni delež zmagovalcev, poražencev pa 
ne bi bilo. 
Kazalniki dohodkovne neenakosti prav tako ne odražajo relevantnih sprememb 
ob uvedbi S04 (tabela 37). Ginijev količnik in razmerje kvintilnih razredov (kazalnik 
80/20) se znižata, vendar zanemarljivo malo oziroma celo nič, kar kaže na 
neznatno izboljšanje dohodkovne porazdelitve. Prav tako se pričakovano ne 
spremenijo niti stopnje tveganja revščine (tabela 38). 
  
 
 
 
 
14 Vrednost upoštevanega premoženja v modelu se lahko razlikuje od vrednosti dejansko 
upoštevanega premoženja (zaradi predpostavk in sprejetih odločitev v fazi priprave podatkov, kot tudi 
zaradi diskrecijske pravice socialnega delavca), kar lahko močno vpliva na rezultate simulacij. 


80 
EkonomIERa  
03-2023 
Tabela 33: Simulirani podatki S04: Sprememba vrednosti socialnih transferjev v S04 glede na osnovni scenarij (v milijonih) 
 
Osnovni scenarij 
S04 
Sprememba v %*** 
S04/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 2018 2019 2020 2021 2017 2018 2019 2020 2021 
2017 2018 2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
194 
236 
284 
294 
281 
194 
236 
284 
294 
281 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ otroški dodatek (bchmt_s) 
274 
281 
274 
277 
260 
276 
282 
276 
278 
261 
0,8% 0,5% 0,5% 
0,5% 
0,3% 
+ državna štipendija (bedmt_s) 
83 
77 
84 
85 
76 
85 
78 
85 
86 
77 
1,7% 1,3% 1,4% 
1,2% 
0,6% 
+ pomoč ob rojstvu otroka* (bchba_s) 
5 
6 
6 
6 
7 
5 
6 
6 
6 
7 
0,3% 0,0% 0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
10 
10 
11 
11 
11 
10 
10 
11 
11 
11 
0,4% 0,3% 0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
25 
35 
39 
39 
33 
25 
35 
39 
39 
33 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ subvencija najemnine (bho_s) 
15 
16 
20 
20 
20 
15 
16 
20 
20 
20 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ posmrtnina (bsawd_s) 
1 
1 
1 
1 
1 
1 
1 
1 
1 
1 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ pogrebnina (bsafu_s) 
2 
3 
3 
3 
3 
2 
3 
3 
3 
3 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ starševski dodatek (bmanc_s) 
10 
10 
10 
10 
15 
10 
10 
10 
10 
15 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
196 
200 
253 
269 
285 
196 
200 
253 
269 
285 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
12 
12 
14 
15 
16 
12 
12 
14 
15 
16 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
+ dohodnina (tin00_s) 
1.904 2.003 2.142 2.152 2.486 1.904 2.003 2.142 2.152 2.486 
0,0% 0,0% 0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon.   
Vir: Lastni izračuni. 
 
 
 


 
 81 
Tabela 34: Simulirani podatki S04: Sprememba števila prejemnikov socialnih transferjev v S04 glede na osnovni scenarij (v 
tisočih) 
 
Osnovni scenarij 
S04 
Sprememba v %*** 
S04/osnovni scenarij 
Leto 
Socialni transferji in dohodnina 
2017 2018 2019 2020 2021 2017 2018 2019 2020 2021 
2017 
2018 
2019 
2020 
2021 
+ socialna pomoč (bsa_s) 
67 
67 
78 
78 
73 
67 
67 
78 
78 
73 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ otroški dodatek (bchmt_s)# 
299 
348 
346 
345 
339 
300 
349 
347 
345 
339 
0,6% 
0,2% 
0,2% 
0,2% 
0,1% 
+ državna štipendija (bedmt_s) 
76 
71 
82 
81 
74 
77 
72 
83 
82 
75 
1,3% 
1,0% 
1,0% 
0,8% 
0,4% 
+ pomoč ob rojstvu otroka* (bchba_s) 
17 
19 
19 
19 
19 
17 
19 
19 
19 
19 
0,3% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dodatek za veliko družino** (bchlg_s) 
24 
24 
27 
27 
27 
24 
24 
27 
27 
27 
0,4% 
0,3% 
0,0% 
0,0% 
0,0% 
+ varstveni dodatek (bsapm_s) 
18 
25 
28 
26 
22 
18 
25 
28 
26 
22 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ subvencija najemnine (bho_s) 
12 
12 
15 
15 
15 
12 
12 
15 
15 
15 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ posmrtnina (bsawd_s) 
3 
3 
3 
3 
3 
3 
3 
3 
3 
3 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ pogrebnina (bsafu_s) 
4 
4 
4 
4 
3 
4 
4 
4 
4 
3 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ starševski dodatek (bmanc_s) 
6 
6 
6 
6 
6 
6 
6 
6 
6 
6 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ materinsko in starševsko nadomestilo (bmact_s) 
31 
31 
31 
31 
31 
31 
31 
31 
31 
31 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ nadomestilo za očetovski dopust (bcrbafh_s) 
13 
13 
13 
13 
13 
13 
13 
13 
13 
13 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
+ dohodnina (il_itbase0) 
1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 1.530 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Opombe: * 2012–2017 pravica, vezana na osebni prejemek/premoženje, od 2018 nič več. ** 2012–2018 pravica, vezana na osebni prejemek/premoženje, od 2019 
nič več. *** Sprememba je izračunana na podlagi natančnih vrednosti in ne vrednosti, zaokroženih na milijon. # Za otroški dodatek simulirani podatki podajajo 
število upravičencev v posameznem letu.   
Vir: Lastni izračuni. 
 
 


82 
EkonomIERa  
03-2023 
Tabela 35: Simulirani podatki S04: Povprečni ekvivalentni razpoložljivi dohodek na člana gospodinjstva po decilih (v EUR) 
 
Osnovni scenarij 
S04 
Sprememba v %*** 
S04/osnovni scenarij 
Leto 
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
3.321 
3.453 
3.763 
3.879 
3.982 
3.323 
3.454 
3.764 
3.880 
3.982 
0,04% 
0,03% 
0,03% 
0,03% 
0,01% 
2. decil 
6.587 
7.012 
7.251 
7.482 
7.749 
6.590 
7.014 
7.253 
7.484 
7.750 
0,04% 
0,03% 
0,03% 
0,02% 
0,02% 
3. decil 
8.314 
8.644 
8.903 
9.211 
9.669 
8.317 
8.647 
8.907 
9.214 
9.671 
0,05% 
0,04% 
0,04% 
0,03% 
0,02% 
4. decil 
9.690 
10.023 
10.326 
10.701 
11.292 
9.694 
10.026 
10.328 
10.703 
11.294 
0,05% 
0,03% 
0,02% 
0,02% 
0,02% 
5. decil 
10.947 
11.306 
11.667 
12.108 
12.823 
10.952 
11.309 
11.670 
12.110 
12.824 
0,04% 
0,03% 
0,02% 
0,02% 
0,01% 
6. decil 
12.242 
12.634 
13.053 
13.554 
14.387 
12.246 
12.637 
13.056 
13.557 
14.389 
0,03% 
0,02% 
0,02% 
0,02% 
0,01% 
7. decil 
13.659 
14.093 
14.566 
15.140 
16.118 
13.664 
14.095 
14.569 
15.142 
16.119 
0,04% 
0,01% 
0,02% 
0,01% 
0,01% 
8. decil 
15.407 
15.916 
16.459 
17.123 
18.280 
15.412 
15.917 
16.460 
17.124 
18.281 
0,03% 
0,01% 
0,01% 
0,01% 
0,0% 
9. decil 
18.041 
18.653 
19.313 
20.115 
21.502 
18.042 
18.654 
19.314 
20.116 
21.503 
0,01% 
0,01% 
0,0% 
0,0% 
0,0% 
10. decil 
28.287 
29.552 
31.728 
31.668 
33.781 
28.288 
29.553 
31.729 
31.669 
33.781 
0,0% 
0,01% 
0,0% 
0,0% 
0,0% 
Skupaj 
12.649 
13.128 
13.703 
14.098 
14.958 
12.653 
13.130 
13.705 
14.100 
14.959 
0,02% 
0,02% 
0,02% 
0,01% 
0,01% 
Vir: Lastni izračuni. 
 
 
 


 
 83 
Tabela 36: Simulirani podatki S04: Zmagovalci in poraženci 
 
Zmagovalci 
Poraženci 
Leto  
Decilni razred 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1. decil 
0,4% 
0,2% 
0,3% 
0,3% 
0,2% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
2. decil 
0,8% 
0,6% 
0,7% 
0,6% 
0,4% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
3. decil 
1,1% 
0,9% 
1,1% 
0,9% 
0,7% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
4. decil 
1,5% 
1,0% 
1,0% 
0,9% 
0,6% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
5. decil 
1,6% 
1,1% 
1,1% 
0,9% 
0,5% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
6. decil 
1,3% 
1,2% 
1,2% 
1,1% 
0,5% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
7. decil 
1,5% 
0,9% 
1,0% 
0,7% 
0,5% 
0,1% 
0,0% 
0,0% 
0,0% 
0,0% 
8. decil 
1,0% 
0,8% 
0,9% 
0,8% 
0,4% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
9. decil 
0,3% 
0,9% 
0,8% 
0,7% 
0,4% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
10. decil 
0,1% 
0,6% 
0,5% 
0,3% 
0,2% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Skupaj 
0,9% 
0,8% 
0,8% 
0,7% 
0,4% 
0,0% 
0,0% 
0,0% 
0,0% 
0,0% 
Vir: Lastni izračuni. 
Tabela 37: Simulirani podatki S04: Kazalniki dohodkovne neenakosti 
 
Osnovni scenarij 
S04 
Leto  
Kazalnik 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
Ginijev koeficient 
0,2863 
0,2860 
0,2909 
0,2856 
0,2901 
0,2862 
0,2860 
0,2908 
0,2855 
0,2901 
Razmerje kvint. razr. (80/20) 
4,6754 
4,6060 
4,6337 
4,5578 
4,7124 
4,6738 
4,6054 
4,6325 
4,5570 
4,7119 
Vir: Lastni izračuni. 
 


84 
EkonomIERa  
03-2023 
Tabela 38: Simulirani podatki S04: Stopnje tveganja revščine 
 
Osnovni scenarij 
S04 
Razlika v odst. točkah 
Leto 
Tip gospodinjstva 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
2017 
2018 
2019 
2020 
2021 
1 odrasla os. <65, brez otrok 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
41,5% 
39,8% 
39,6% 
39,7% 
41,3% 
0,0 
0,0 
0,0 
0,0 
0,0 
1 odrasla os. ≥65, brez otrok 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
35,6% 
32,8% 
33,5% 
32,4% 
35,1% 
0,0 
0,0 
0,0 
0,0 
0,0 
1 odrasla os. z otroci 
30,1% 
28,2% 
27,3% 
28,2% 
30,9% 
30,1% 
28,2% 
27,2% 
28,2% 
30,9% 
-0,1 
0,0 
-0,1 
0,0 
0,0 
2 odrasli os.<65, brez otrok  
15,8% 
15,3% 
15,4% 
15,5% 
15,8% 
15,8% 
15,2% 
15,4% 
15,5% 
15,8% 
0,0 
0,0 
0,0 
0,0 
0,0 
2 odrasli os., vsaj 1 ≥65, brez 
otrok  
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
12,0% 
11,4% 
11,5% 
11,4% 
11,9% 
0,0 
0,0 
0,0 
0,0 
0,0 
2 odrasli os., 1 otrok 
14,1% 
13,7% 
13,5% 
13,9% 
14,5% 
14,1% 
13,7% 
13,4% 
13,8% 
14,5% 
0,0 
0,0 
-0,1 
0,0 
0,0 
2 odrasli os., 2 otroka 
11,5% 
10,5% 
10,4% 
10,8% 
11,6% 
11,5% 
10,5% 
10,4% 
10,8% 
11,6% 
0,0 
0,0 
0,0 
0,0 
0,0 
2 odrasli os., 3 ali več otrok 
16,1% 
14,3% 
13,8% 
14,8% 
16,3% 
16,0% 
14,2% 
13,8% 
14,8% 
16,3% 
-0,1 
-0,1 
-0,1 
0,0 
0,0 
3 ali več odraslih os., brez 
otrok 
7,5% 
7,2% 
7,3% 
7,5% 
7,7% 
7,5% 
7,2% 
7,2% 
7,5% 
7,7% 
0,0 
0,0 
0,0 
0,0 
0,0 
3 ali več odraslih os. z otroci 
9,1% 
8,6% 
8,7% 
8,9% 
9,4% 
9,1% 
8,6% 
8,6% 
8,8% 
9,4% 
0,0 
0,0 
0,0 
0,0 
0,0 
Skupaj 
16,9% 
16,0% 
16,0% 
16,1% 
17,0% 
16,9% 
16,0% 
15,9% 
16,1% 
17,0% 
0,0 
0,0 
0,0 
0,0 
0,0 
Vir: Lastni izračuni. 
 
 


 
 85 
6.5 Porazdelitev po dohodkovnih razredih 
V tem poglavju primerjamo učinke posameznih scenarijev iz prejšnjega poglavja. 
Za predpostavljene scenarije, opisane v predhodnih poglavjih (6–6.4), smo 
pogledali, kako bi vplivali na porazdelitev prejemnikov po dohodkovnih razredih 
pri otroškemu dodatku, znižanemu plačilu vrtca in državni štipendiji ter 
dohodnini. Na spodnjih slikah prikazujemo spremembe v porazdelitvi 
prejemnikov/zavezancev glede na dohodkovne razrede za posamezno pravico 
oziroma dohodnino. Analiziramo tudi spremembe skupne vrednosti posamezne 
pravice oziroma dohodnine po dohodkovnih razredih in na agregatni ravni, ki so 
posledica uvedbe posameznega scenarija. Spremembe vsakega posameznega 
scenarija analiziramo v primerjavi z osnovnim scenarijem (S01 vs. Osnovni 
scenarij, S02 vs. Osnovni scenarij, S03 vs. Osnovni scenarij in S04 vs. Osnovni 
scenarij) in jih izrazimo v odstotnih točkah (slike 1–11). Razredi so oblikovani 
glede na porazdelitev upravičencev v osnovnem scenariju. Prikažemo tudi celotne 
izdatke za posamezne pravice za vsak posamezen scenarij (stolpiči na sliki) v 
primerjavi z osnovnim scenarijem (trikotnik na sliki). S to primerjavo želimo 
nakazati predvsem velikost in smer učinka vsakega predpostavljenega scenarija.  
Na spremembe pri porazdelitvi upravičencev do otroškega dodatka najbolj vpliva 
scenarij S02. Ob uvedbi univerzalnega otroškega dodatka (S02) bi se na račun 
novo upravičenih (otrok) oziroma novih prejemnikov (staršev) povišalo skupno 
število prejemnikov otroškega dodatke. Vsi prejemniki otroškega dodatka v 
osnovnem scenariju bi v scenariju S02 pravico obdržali. Zaradi ukinitve razredov 
pri otroškem dodatku v scenariju S02 ga v sliki 1 ne prikazujemo.   
Primerjava celotnega zneska, namenjenega za otroški dodatek, nakaže, da bi se 
ob scenariju S02 relativno znižali skupni izdatki za otroške dodatke prejemnikov 
iz prvih štirih dohodkovnih razredov (v osnovnem scenariju), a bi bili višji za 
prejemnike petega in višjega dohodkovnega razreda. To je posledica tako uvedbe 
predpostavljenega univerzalnega dohodka v višini 50 evrov kot tudi novega 
števila upravičencev. S predpostavljeno reformo bi namreč prejemniki iz nižjih 
dohodkovnih razredov prejeli nižji znesek otroškega dodatka v primerjavi s 
trenutno veljavno ureditvijo, medtem ko bi tisti iz zadnjih treh razredov brez 
omejitve dohodka navzgor prejeli višji znesek otroškega dodatka v primerjavi z 
osnovnim scenarijem, ki upošteva veljavno zakonodajo po posameznih letih.     


86 
EkonomIERa  
03-2023 
Malo vidnejša sprememba je še pri S03. Kot lahko razberemo iz slik 1 in 2, bi se 
ob uveljavitvi enotne dohodninske stopnje v višini 25 % povišal delež prejemnikov 
otroškega dodatka predvsem v tretjem dohodkovnem razredu, rahlo pa tudi v 
drugem in četrtem. Nasprotno bi se delež upravičencev nekoliko znižal v zadnjih 
treh ter prvem dohodkovnem razredu. Posledično bi se v podobni smeri gibala 
tudi sprememba izdatkov za otroški dodatek ob uvedbi S03 v primerjavi z 
osnovnim modelom. Enotna dohodninska stopnja bi torej najbolj vplivala na 
prejemnike otroškega dodatka v tretjem dohodkovnem razredu.  
Skupni izdatki za otroški dodatek bi se najbolj znižali ob vpeljavi 
predpostavljenega S02 in povišali v vseh ostalih treh predpostavljenih scenarijih. 
Slika 3 prikazuje skupne izdatke za otroški dodatek po posameznih scenarijih 
(stolpiči) v primerjav z osnovnim scenarijem (trikotniki).  
 


 
 87 
Slika 1: Otroški dodatek: Spremembe v porazdelitvi prejemnikov po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
Slika 2: Otroški dodatek: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
 
-10,00
-5,00
0,00
5,00
1DR
2DR
3DR
4DR
5DR
6aDR
6bDR
Novo
upravičeni
S01  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij
-15,00
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
1DR
2DR
3DR
4DR
5DR
6aDR
6bDR
Novo
upravičeni
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij


88 
EkonomIERa  
03-2023 
Slika 3: Izdatki za otroški dodatek ob uveljavitvi scenarijev v primerjavi z 
osnovnim scenarijem (v milijonih EUR), leto 2017 
 
Vir: Lastni izračuni. 
Starši otrok, vključenih v vrtec, bi v največji meri občutili spremembe ob uvedbi 
S01 (slika 4). Do vključno četrtega dohodkovnega razreda bi se relativno število 
prejemnikov subvencije15 zmanjšalo na račun povečanja števila prejemnikov v 
višjih dohodkovnih razredih (od petega do devetega). Višji znesek minimalnega 
dohodka bi pomenil višji neto dohodek družin in uvrstitev v višji razred ter 
posledično prejemanje nižje subvencije za plačilo vrtca. Najbolj bi se število 
prejemnikov subvencije znižalo v drugem dohodkovnem razredu, zvišalo pa v 
petem. V enaki smeri se gibljejo tudi izdatki za subvencijo vrtca (slika 5). Iz slike 6 
je razvidno, da so skupni izdatki za subvencijo vrtca ob uvedbi S01 višji napram 
osnovnemu scenariju. V primerjavi z ostalimi predpostavljenimi scenariji bi bilo 
povišanje izdatkov za subvencijo vrtca najizrazitejše ravno ob uvedbi tega 
scenarija (S01).  
Zaradi vpeljave univerzalnega otroškega dodatka (S02), bi se število oziroma 
delež prejemnikov pravice do znižanega plačila vrtca povečalo v prvih dveh 
dohodkovnih razredih in malenkostno v zadnjih treh, medtem ko bi se v srednjih 
dohodkovnih razredih (tretji–šesti) temu primerno znižalo. Skladno z omenjenimi 
prehodi po dohodkovnih razredih se giblje tudi znesek oziroma javni izdatki za 
subvencijo vrtca.  
 
15 Ker je višina subvencije vezana tudi na ceno vrtca (in ne le na dohodkovni razred), je v tem delu 
treba omeniti, da smo ceno vrtca določili za dve starostni obdobji na podlagi povprečnih cen vrtcev v 
Sloveniji za leto 2022 in stopnje rasti cene vrtca med letoma 2012 in 2019 v Ljubljani, ločeno za prvo 
in drugo starostno obdobje (podatki o cenah vrtcev, dostopni na spletnih straneh). 
200
220
240
260
280
200
220
240
260
280
S01
S02
S03
S04
Znesek OD po scenarijih
Osnovni scenarij


 
 89 
Tudi uvedba enotne dohodninske stopnje (S03) bi nekoliko vidnejše vplivala na 
prehode med dohodkovnimi razredi, in sicer število oziroma delež prejemnikov 
bi se povišal v drugem, tretjem, četrtem in le malenkostno v zadnjem, devetem, 
dohodkovnem razredu, medtem ko bi se v ostalih dohodkovnih razredih skladno 
znižal. Izjema ostaja prvi dohodkovni razred, kjer se število prejemnikov ne bi 
spremenilo. Podobnemu gibanju sledili tudi javni izdatki za subvencijo vrtca. 
Uvedba scenarija S04, neupoštevanje premoženja po ZUPJS, ne nakazuje vidnejših 
sprememb.   
Slika 4: Znižano plačilo vrtca: Spremembe v porazdelitvi prejemnikov po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
 
 
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
25,00
1DR
2DR
3DR
4DR
5DR
6DR
7DR
8DR
9DR
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij


90 
EkonomIERa  
03-2023 
Slika 5: Znižano plačilo vrtca: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
Slika 6: Izdatki za subvencijo vrtca ob uveljavitvi scenarijev v primerjavi z 
osnovnim scenarijem (v milijonih EUR), leto 2017 
 
Vir: Lastni izračuni. 
Državna štipendija je še tretja pravica iz javnih sredstev, katere upravičenost in 
višina sta odvisni od uvrstitve osebe v dohodkovni razred. Uvedbe 
predpostavljenih scenarijev vplivajo tako na skupno število prejemnikov kot tudi 
na delež prejemnikov po posameznih razredih. Tudi na državno štipendijo bi 
najbolj vplival scenarij S01; znižalo bi se skupno število prejemnikov državne 
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
25,00
1DR
2DR
3DR
4DR
5DR
6DR
7DR
8DR
9DR
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij
295
300
305
310
315
320
295
300
305
310
315
320
S01
S02
S03
S04
Znesek VR po scenarijih
Osnovni scenarij


 
 91 
štipendije, slednje pa bi vplivalo tudi na porazdelitev upravičencev po 
dohodkovnih razredih. Tako bi se relativno zmanjšalo število prejemnikov v prvih 
treh dohodkovnih razredih, v (predvsem) četrtem in petem pa bi se povišalo (slika 
7). Enako se gibljejo tudi izdatki za državno štipendijo (slika 8).  
Ob uvedbi ostalih treh scenarijev (S02, S03 in S04) spremembe ne bi bile tako 
močno opazne. Še najbolj bi na porazdelitev upravičencev do državne štipendije 
vplivala vpeljava univerzalnega otroškega dodatka (S02), ko bi se število 
upravičencev kot tudi znesek izdatkov za državno štipendijo povečal v prvem 
dohodkovnem razredu.  
Ob primerjavi skupnih izdatkov za državno štipendijo po posameznih scenarijih 
glede na osnovni scenarij lahko vidimo, da bi uvedba S01 izdatke, namenjene za 
državno štipendijo, znižala, vsi ostali scenariji pa bi jih zvišali.   
Slika 7: Državna štipendija: Spremembe v porazdelitvi prejemnikov po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
 
 
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
25,00
1DR
2DR
3DR
4DR
5DR
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij


92 
EkonomIERa  
03-2023 
Slika 8: Državna štipendija: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
Slika 9: Izdatki za državno štipendijo ob uveljavitvi scenarijev v primerjavi z 
osnovnim scenarijem (v milijonih EUR), leto 2017 
 
Vir: Lastni izračuni. 
Kot so nakazali že rezultati simulacij scenarijev, predstavljenih v predhodnih 
poglavjih (6–6.4), uvedba katerega koli predpostavljenega scenarija ne bi vplivala 
na absolutno število davčnih zavezancev. Bi pa vpeljava enotne dohodninske 
stopnje (S03) vplivala tako na absolutni znesek pobrane dohodnine kot tudi na 
prehode med dohodkovnimi razredi. Osebe iz prvega in drugega dohodkovnega 
-15,00
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
1DR
2DR
3DR
4DR
5DR
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij
50
60
70
80
90
100
50
60
70
80
90
100
S01
S02
S03
S04
Znesek DŠ po scenarijih
Osnovni scenarij


 
 93 
razreda bi plačale več dohodnine, medtem ko bi se za osebe iz tretjega, četrtega 
in petega dohodkovnega razreda delež pobrane dohodnine znižal (najbolj v 
četrtem dohodkovnem razredu). Ostali trije predpostavljeni scenariji (S01, S02 in 
S04) ne bi imeli vpliva na višino dohodnine.  
Slika 10: Dohodnina: Spremembe v porazdelitvi pobrane dohodnine po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 
 
Vir: Lastni izračuni. 
Slika 11: Pobrana dohodnina ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v milijonih EUR), leto 2017 
 
Vir: Lastni izračuni. 
 
-15,00
-10,00
-5,00
0,00
5,00
10,00
15,00
20,00
1DR
2DR
3DR
4DR
5DR
S01  vs. osnovni scenarij
S02  vs. osnovni scenarij
S03  vs. osnovni scenarij
S04  vs. osnovni scenarij
1500
1700
1900
2100
2300
1500
1700
1900
2100
2300
S01
S02
S03
S04
Znesek dohodnine po scenarijih
Osnovni scenarij


94 
EkonomIERa  
03-2023 
 
 


 
 95 
7 
ZAKLJUČEK 
To delo predstavlja statični mikrosimulacijski simulacijski model davkov in 
socialnih transferjev SLOmod.  SLOmod je nadgradnja obstoječega statičnega 
mikrosimulacijskega modela, ki temelji na širokem naboru podatkov iz 
administrativnih baz podatkov. Uporaba širokega nabora administrativnih baz 
podatkov nam je omogočila številne priložnosti/možnosti izboljšav pri izgradnji 
končnega modela v primerjavi s trenutno obstoječimi modeli. Model so izboljšali 
podatki o dohodkih iz delovnega razmerja na mesečni ravni, kar je pomembno 
pri simulaciji denarne socialne pomoči, in širok nabor podatkov iz informacijskega 
sistema centrov za socialno delo IS CSD s podatki o premoženju vlagateljev. 
SLOmod je tako prvi slovenski mikrosimulacijski model, ki pri simulaciji socialnih 
transferjev upošteva tudi premoženje posameznika oziroma družinskih članov. 
Veliko različnih baz podatkov in njihovo medsebojno povezovanje je vedno 
povezano z več izzivi. V fazi priprave podatkov kot izgradnji mikrosimulacijskega 
modela SLOmod je bilo treba sprejeti nekaj predpostavk, ki jih je moramo 
upoštevati pri interpretaciji rezultatov simulacij. Največja omejitev je sestava 
gospodinjstva oziroma družine, ki je pri simuliranju upravičenosti do socialnih 
transferjev zelo pomembna. Kljub našim popravkom in prilagoditvam sestave 
oziroma tipa gospodinjstev, pri čemer smo upoštevali tudi sestavo gospodinjstev 
in družin iz vlog za uveljavljenje pravic iz javnih sredstev (IS CSD baze), še vedno 
prihaja do razhajanj med sestavo gospodinjstev iz registrskih virov in dejansko 
sestavo. Poleg tega so zaradi uporabe vzorca večkrat spregledani tudi naši 
popravki glede oblikovanja gospodinjstev, saj posamezne osebe iz gospodinjstva 
oziroma družine niso bile izbrane v vzorec. Vse simulacije v modelu SLOmod 
temeljijo na vzorčnih podatkih iz leta 2017, kar pomeni, da upravičenost do 
posameznih transferjev presojamo na podlagi dohodkov iz leta 2017. Dejansko 
se o upravičenosti do posameznega socialnega transferja odloča na podlagi 
dohodka iz leta 2016 ali celo 2015. Podatke o premoženju imamo zgolj za 
družine/gospodinjstva, ki so zaprosila za katerokoli pravico, za ostale pa vrednost 
premoženja ocenjujemo. Poleg tega se vrednost upoštevanega premoženja v 
modelu lahko razlikuje od vrednosti premoženja iz uradnih evidenc zaradi 
diskrecijske pravice socialnega delavca. Ker gre za statičen model, spremenljivke, 
ki opisujejo socio-demografske značilnosti oseb (kot so zaposlitveni status, 
demografske spremenljivke in sestava gospodinjstva), ostajajo čez celotno 
obdobje opazovanja 2018–2022 enake kot v baznem letu 2017. 


96 
EkonomIERa  
03-2023 
Ne glede na omejitve in predpostavke ter dejstva, da model ne poda vedno 
popolnoma skladnih rezultatov simulacij z uradnimi podatki, nam SLOmod lahko 
pokaže smer in obseg pričakovanih sprememb, tako glede števila prejemnikov in 
obsega sredstev za posamezni transfer kot tudi glede porazdelitve dohodka med 
posameznimi skupinami prebivalstva.  
Uporaba modela je razmeroma enostavna. Uporabnik lahko v modelu s pomočjo 
vmesnika poljubno spreminja parametre in dodaja nove funkcije/politike. V 
poglavju 0 opišemo rezultate simulacij različnih hipotetičnih scenarijev, s čimer 
želimo konkretneje prikazati, kako lahko uporabljamo model. Seveda je možno z 
modelom simulirati tudi vrsto drugih scenarijev – bodisi tiste, ki spreminjajo le 
vrednosti nekaterih parametrov (kot so npr. višina določenega denarnega 
transferja, 
dohodkovna 
meja 
za 
presojanje 
upravičenosti, 
cena 
vrtca/malice/kosila, na podlagi katere je izračunana subvencija, ali višina 
posameznega dodatka pri državni štipendiji ipd.), ali pa zahtevnejše, za katere so 
potrebne prilagoditve modela (popravljanje/dodajanje/brisanje funkcij, kot so 
npr. ponovna uvedba ugotavljanja materialnega položaja pri presojanju 
upravičenosti do dodatka za veliko družino/pomoči ob rojstvu otroka, uvedba 
nove pravice, sprememba načina ugotavljanja materialnega položaja, spremenjen 
vrstni red uveljavljanja pravic ipd.).   
V načrtih za prihodnje delo je tudi že razširitev oziroma nadgradnja modela z 
modulom prilagoditve trga dela (LMA) in vključitvijo indirektnih davkov (davek na 
dodano vrednost, trošarine) v model. Pri vpeljavi modula LMA bomo na podlagi 
baze podatkov o aktivnem in neaktivnem prebivalstvu, ki prikazuje stanje in 
spremembe na slovenskem trgu (SURS, 2021), ocenili tranzicije na trgu dela 
(premik osebe iz nezaposlenosti/neaktivnosti v zaposlenost, zaposlenosti v 
kratkotrajno brezposelnost, zaposlenosti v dolgotrajno brezposelnost ter iz 
kratkotrajne brezposelnosti v dolgotrajno brezposelnost). Z vključitvijo modula 
LMA bomo tako lahko upoštevali tudi spremembe na trgu dela med posameznimi 
leti in baznim letom. Zaradi sprememb na trgu dela se spremenijo tudi dohodki, 
ki so osnova za simuliranje davkov in socialnih transferjev. Tako bi bilo na primer 
leta 2022 manj brezposelnih kot leta 2017, hkrati pa bi bilo več prejemnikov plač. 
Indirektni davki oziroma potrošnja pa bodo vpeljani v model na podlagi 
razširjenega nabora vhodnih podatkov, ki bo vseboval tudi podatke o izdatkih 
gospodinjstev za potrošnjo – življenjske potrebščine (ki se objavljajo skladno z 
evropsko klasifikacijo individualne potrošnje po namenu – ECOICOP (SURS, 


 
 97 
2019)), ter implementacije dodatnega sklopa politik (funkcij), vezanih na 
indirektne davke v vmesniku modela.   
Uporaba modela za ocenjevanje različnih hipotetičnih scenarijev bo vodila k 
izboljšanju modela, odpravi morebitnih napak in tudi k novim idejam, kako bi 
lahko model še dopolnili.  
 
 


98 
EkonomIERa  
03-2023 
 
 


 
 99 
LITERATURA IN VIRI 
EUROMOD 
(2023). 
Projects. 
Dostopno 
na: 
https://euromod-web.jrc. 
ec.europa.eu/research/projects 
Heckman, J. J. (1979). Sample Selection Bias as a Specification Error. Econometrica, 
47, 153–161. 
Ministrstvo za finance [MF], Sektor za analize in koordinacijo davčne politike, 
(2019). Osnovni statistični podatki iz odločb odmere dohodnine za leto 2017. MF: 
Ljubljana. 
Ministrstvo za finance [MF], Sektor za analize in koordinacijo davčne politike, 
(2020). Osnovni statistični podatki iz odločb odmere dohodnine za leto 2018. MF: 
Ljubljana. 
Ministrstvo za finance [MF], Sektor za analize in koordinacijo davčne politike, 
(2021). Osnovni statistični podatki iz odločb odmere dohodnine za leto 2019. MF: 
Ljubljana. 
Ministrstvo za finance [MF], Sektor za analize in koordinacijo davčne politike, 
(2022a). Osnovni statistični podatki iz odločb odmere dohodnine za leto 2020. 
MF: Ljubljana. 
Ministrstvo za finance [MF] (2022b). Konsolidirana bilanca javnega financiranja. 
MF: Ljubljana. 
Ministrstvo za delo, družino socialne zadeve in enake možnosti [MDDSZ] (2022). 
Tabela izplačil socialnih transferjev (oktober, 2022). Pridobljeno na naslovu: 
https://www.gov.si/podrocja/socialna-varnost/pravice-iz-javnih-sredstev-in-
socialnovarstveni-programi/ 
Ministrstvo za izobraževanje, znanost in šport [MIZŠ] (2022). Interni podatki.   
Statistični urad Republike Slovenije [SURS] (2019). Poraba v gospodinjstvih, 
Metodološko pojasnilo. SURS: Ljubljana. 
Statistični urad Republike Slovenije [SURS] (2021). Aktivno in neaktivno 
prebivalstvo, Metodološko pojasnilo. SURS: Ljubljana. 


100 
EkonomIERa  
03-2023 
Statistični urad Republike Slovenije [SURS] (2022a). Registrski popis prebivalstva, 
gospodinjstev in stanovanj, Metodološko pojasnilo. SURS: Ljubljana. 
Statistični urad Republike Slovenije [SURS] (2022b). Otroci, vključeni v vrtec, po 
vrsti vrtca (lastnina), starosti, spolu in kohezijski regiji zavoda, Slovenija, letno 
(2022). Pridobljeno na naslovu: https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-
/0952540S.px/table/tableViewLayout2/ 
Sutherland, H., and Figari, F. (2013). EUROMOD: The European Union Tax-Benefit 
Microsimulation Model. International Journal of Microsimulation, 6(1), 4–26. 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije [ZPIZ], (2018). Letno 
poročilo 2017. ZPIZ: Ljubljana. 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije [ZPIZ], (2019). Letno 
poročilo 2018. ZPIZ: Ljubljana. 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije [ZPIZ], (2020). Letno 
poročilo 2019. ZPIZ: Ljubljana. 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije [ZPIZ], (2021). Letno 
poročilo 2020. ZPIZ: Ljubljana. 
Zavod za pokojninsko in invalidsko zavarovanje Slovenije [ZPIZ], (2022). Letno 
poročilo 2021. ZPIZ: Ljubljana. 
 
 


 
 101 
PRILOGE 
Priloga 1: Opisi vhodnih spremenljivk modela SLOmod, ki izhajajo iz 
mikropodatkov (podatki iz povezanih baz podatkov in lastnih preračunov, na 
podlagi katerih ustvarimo vhodno bazo) 
Spremenljivka 
Opis spremenljivke 
Dodana spremenljivka/opomba 
idhh 
Identifikator gospodinjstva 
  
idfamily 
Identifikator družine 
Dodana spremenljivka 
idperson 
Identifikator osebe 
  
idfather 
Identifikator mame 
  
idmother 
Identifikator očeta 
  
idpartner 
Identifikator partnerja 
  
idhh_f 
Opozorilo pri ID gospodinjstva: 0 = ni 
skupinsko/posebno gospodinjstvo, 1 = študentski 
dom oziroma prevladujejo mladi, 2 = dom 
starejših občanov oziroma prevladujejo starejši, 3 
= drugo 
Dodana spremenljivka 
dag 
Starost v letu 2017 
  
dag00 
Št. mesecev v starosti 0 let v letu 2017 (za 
določitev št. mesecev prejemanja starševskega 
dodatka) 
Dodana spremenljivka 
dmb 
Mesec rojstva 
  
dgn 
Spol: 0 = ženske, 1 = moški  
  
dms 
Zakonski stan: 1 =samski, 2 = poročen, 3 = 
razvezan, 4 = vdovec, 5 = partnerstvo  
  
dcz 
Državljanstvo: 1 = SLO,  2 = drug EU država, 3 = 
ostalo 
  
dwt 
Utež 
  
dfa 
Označuje posameznike, ki so v letu 2017 izgubili 
ožjega družinskega člana (partnerja ali starša): 0 = 
ne, 1 = da 
Dodana spremenljivka 
dec 
Izobrazba - trenutni status: 0 = se ne izobražuje, 
1 = otroci v vrtcu, 2 = učenci, 3 = dijaki, 4 = 
študentje 
 
deh 
Najvišja dosežena izobrazba: 0 = brez izobrazbe, 
1 = osnovnošolska izobrazba, 2 = srednješolska 
izobrazba, 3 =  visokošolska ali višješolska 
izobrazba 
  
dec00 
Ali je bil otrok v letu 2017 v vrtcu: 0 = ne, 1 = da  Dodana spremenljivka 
ddi 
Status invalidnosti: 0 = ne, 1 = da, -1 = ni 
relevantno (mlajši od 16. let)  
Spremenljivka, določena na podlagi podatka 
o vrsti invalidnosti iz baze SRDAP. 
ddpch 
Vzdrževani otrok: 0 = ne, 1 = da  
Dodana spremenljivka 
dadch 
Ali ima oseba odraslega otroka: 0 = ne, 1 = da   
Dodana spremenljivka 
dch 
Vrstni red otroka (po starosti od najstarejšega do 
najmlajšega) 
Dodana spremenljivka 
decmy 
Št. mesecev v izobrazbi za tiste, ki se trenutno 
izobražujejo 
Dodana spremenljivka, določena na podlagi 
statusa mesečne aktivnosti 
decmy01 
Št. mesecev v izobrazbi v študijskem letu 
2016/2017 za tiste, ki so trenutno v izobrazbi 
Dodana spremenljivka 
decmy02 
Št. mesecev v izobrazbi v študijskem letu 
2017/2018 za tiste, ki so trenutno v izobrazbi 
Dodana spremenljivka 
decst01 
Status/vrsta vpisa v študijskem letu 2016/2017 za 
tiste, ki so trenutno v izobrazbi 
Dodana spremenljivka 
decst02 
Status/vrsta vpisa v študijskem letu 2017/2018 za 
tiste, ki so trenutno v izobrazbi 
Dodana spremenljivka 


102 
EkonomIERa  
03-2023 
Spremenljivka 
Opis spremenljivke 
Dodana spremenljivka/opomba 
les 
Ekonomski status: 0 = predšolski otroci (osebe, 
mlajše od 6 let), 1 = kmetje, 2 = samozaposleni, 3 
= zaposleni, 4 = upokojenci, 5 = brezposelni, 6 = 
učenci, dijaki in študentje, 7 = druge neaktivne 
osebe, 8 = bolni in invalidi 
Na podlagi podatka o statusu mesečne 
aktivnosti, les določen za 3 obdobja v letu: 
januar (les01), junij(les06) in december 
(les12); letni status les je enak junijskemu (les 
= les06) 
lpb 
Javni sektor: 0 = ne, 1 = da, -1 = ni relevantno 
Dodana spremenljivka 
lindi 
Dejavnost: 1 = kmetijstvo in ribištvo, 2 = 
rudarstvo in predelovalne dejavnosti, 3 = 
gradbeništvo, 4 = trgovina na debelo in drobno, 
5 = gostinstvo in restavracije, 6 = promet in 
komunikacije, 7 = finančno posredništvo, 8 = 
poslovanje z nepremičninami in poslovne 
dejavnosti, 9 = javna uprava in obramba, 10 = 
izobraževanje, 11 = zdravstvo in socialno varstvo, 
12 = drugo, 0 = ni relevantno 
  
liwmy 
Št. mesecev v zaposlitvi v referenčnem letu 
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti 
liwftmy 
Št. mesecev v zaposlitvi – polni delovni čas 
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti 
liwptmy 
 Št. mesecev v zaposlitvi – krajši delovni čas 
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti 
lhw 
Št. delovnih ur na teden 
  
liwwh 
Št. mesecev zaposlitve (delovna doba) 
  
lunmy 
Št. mesecev brezposelnosti  
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti 
tchmy 
Št. mesecev, ko je otrok lahko vzdrževani član 
Dodana spremenljivka 
yivwg 
Plača na uro za leto 2017 
  
yemtx 
Obdavčljivi dohodek iz zaposlitve – plača 
Dodana spremenljivka 
yemot 
Drugi obdavčljivi dohodki iz zaposlitve 
Dodana spremenljivka 
yemhl 
Regres  
Dodana spremenljivka 
yem 
Dohodek iz zaposlitve: yemtx + yemot + yemhl 
  
yemmy 
Št. mesecev prejemanje dohodka iz zaposlitve 
(yemtx + yemot + yemhl) 
Spremenljivka, določena na podlagi podatka 
o mesečnem/letnem dohodku in statusa 
mesečne aktivnosti  
yse 
Dohodek iz samozaposlitve: yse00 + ysen 
  
yse00 
Dohodek iz samozaposlitve (navadni s.p.) 
  
ysen  
Dohodek iz samozaposlitve – normiranec 
Dodana spremenljivka 
ysemy 
Št. mesecev prejemanje dohodka iz 
samozaposlitve (yse00 + ysen) 
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti in letnega dohodka 
yseag 
Dohodek iz samozaposlitve – kmetijska dejavnost Dodana spremenljivka 
yseagmy 
Št. mesecev prejemanje dohodka iz 
samozaposlitve – kmetijska dejavnost 
Dodana spremenljivka 
bedmt 
Znesek državne štipendije z upoštevanjem 
dodatkov 
Dodana spremenljivka 
bedmtmy 
Št. mesecev prejemanja državne štipendije 
Dodana spremenljivka 
bedmt00 
Osnovni znesek državne štipendije  
Dodana spremenljivka 
bedmtadd1 
Državna štipendija: znesek dodatka za uspeh 
Dodana spremenljivka 
bedmtadd2 
Državna štipendija: znesek dodatka za bivanje 
Dodana spremenljivka 
bedmtadd3 
Državna štipendija: znesek dodatka za posebne 
potrebe 
Dodana spremenljivka 
bhl 
Znesek nadomestila za bolniško nad 30 dni 
  
pdi00 
Znesek invalidske pokojnine 
  
poa00 
Znesek starostne pokojnine 
  
psu00 
Znesek družinske in vdovske pokojnine 
  
yiy 
Dohodek iz kapitala: yiyot + yiyitdp 
  
ypr 
Dohodek iz premoženja 
  


 
 103 
Spremenljivka 
Opis spremenljivke 
Dodana spremenljivka/opomba 
yptmp 
Znesek prejetih preživnin 
  
bho 
Znesek subvencije za najemnino 
  
tprrt 
Davek iz oddajanja premoženja v najem 
  
yot 
Drugi dohodki 
  
tiy 
Davek na kapital 
Dodana spremenljivka 
yro  
Avtorski honorar 
Dodana spremenljivka 
yemabtx 
Tuji dohodki: 0 = domači dohodki, 1 = tuji 
dohodki, 2 = tuji in domači dohodki 
Dodana spremenljivka 
bunmy 
Št. mesecev prejemanja denarnega nadomestila 
za brezposelnost 
Spremenljivka, določena na podlagi statusa 
mesečne aktivnosti in letnega dohodka 
pdimy 
Št. mesecev prejemanja invalidske pokojnine 
Spremenljivka, določena glede na mesečni 
podatek o vrsti pokojnine 
poamy 
Št. mesecev prejemanja starostne pokojnine 
Spremenljivka, določena glede na mesečni 
podatek o vrsti pokojnine 
psumy 
Št. mesecev prejemanja družinske in vdovske 
pokojnine 
Spremenljivka, določena glede na mesečni 
podatek o vrsti pokojnine 
bunct 
Znesek denarnega nadomestila za brezposelnost   
yempv 
Osnova za izračun denarnega nadomestila za 
brezposelnost  
  
yemnt 
Neobdavčljivi dohodek iz zaposlitve 
  
yaj 
Dohodek iz dodatne zaposlitve: yaj01 + yaj02 
  
yst 
Dohodek študentov, upravičenih do posebne 
olajšave 
  
ystw 
Dohodek študentov, neupravičenih do posebne 
olajšave 
  
bdica 
Znesek dodatka za pomoč in postrežbo 
  
bdicamy 
Št. mesecev prejemanja dodatka za pomoč in 
postrežbo 
Dodana spremenljivka 
bdixp 
Znesek invalidnine 
  
bdixpmy 
Št. mesecev prejemanja invalidnine 
Dodana spremenljivka 
pls 
Znesek letnega dodatka za upokojence  
  
plsmy 
Št. mesecev prejemanja letnega dodatka za 
upokojence 
  
bdirw 
Znesek nadomestila za delovne invalide 
  
bdirwmy 
Št. mesecev prejemanja nadomestila za delovne 
invalide 
Dodana spremenljivka 
bfapt 
Znesek plačila prispevkov v primeru koriščenja 
krajšega delovnega časa 
  
bfaptmy 
Št. mesecev koriščenja pravice do plačila 
prispevkov zaradi krajšega delovnega časa  
  
bfabk 
Znesek plačila prispevkov zaradi varovanja štirih 
ali več otrok 
  
bfabkmy 
Št. mesecev koriščenja pravice do plačila 
prispevkov zaradi varovanja štirih ali več otrok 
  
bmact 
Znesek materinskega in starševskega nadomestila   
bmactmy 
Št. mesecev starševskega dopusta 
  
bcrbafh 
Znesek očetovskega nadomestila 
  
bcrbafhmy 
Št. mesecev očetovskega dopusta 
  
bcrsvcc 
Znesek nadomestila za izgubljeni dohodek zaradi 
otroka, ki potrebuje posebno nego  
  
bcrsvccmy 
Št. mesecev koriščenja nadomestila za izgubljeni 
dohodek zaradi otroka, ki potrebuje posebno 
nego 
  
bchba 
Znesek pomoči ob rojstvu otroka 
  
bmanc 
Znesek starševskega dodatka 
  
bmancmy 
Št. mesecev prejemanja starševskega dodatka 
  


104 
EkonomIERa  
03-2023 
Spremenljivka 
Opis spremenljivke 
Dodana spremenljivka/opomba 
bchlg 
Znesek dodatka za veliko družino 
  
bchmt 
Znesek otroškega dodatka 
  
bchmtmy 
Št. mesecev prejemanja otroškega dodatka   
  
bchcc 
Znesek dodatka za nego otroka 
  
bchccmy 
Št. mesecev prejemanja dodatka za nego otroka    
bsapm 
Znesek varstvenega dodatka 
  
bsapmmy 
Št. mesecev prejemanja varstvenega dodatka  
  
bsa00 
Znesek denarne socialne pomoči 
  
bsamy 
Št. mesecev prejemanja denarne socialne pomoči    
bsaec 
Znesek izredne denarne pomoči  
  
bsafu 
Znesek pogrebnine 
  
bsawd 
Znesek posmrtnine 
  
bhomy 
Št. mesecev prejemanja subvencije najemnine 
  
bchedycmy 
Št. mesecev v vrtcu 
Dodana spremenljivka 
amrow 
Status lastništva nepremičnine: 0 = ne, 1 = da 
Dodana spremenljivka 
amrmv00 
Tržna vrednost nepremičnine stanovanja/hiše 
Dodana spremenljivka 
amrmv01 
Tržna vrednost nepremičnine stanovanja/hiše, 
namenjene za opravljanje dejavnosti  
Dodana spremenljivka 
aotmv00 
Vrednost drugih nepremičnin 
Dodana spremenljivka 
aotmv01 
Vrednost drugih nepremičnin, namenjenih 
dejavnosti 
Dodana spremenljivka 
amrar00 
Velikost stanovanja/hiše v m2 
Dodana spremenljivka 
amrtn 
1 = lastniško, 2 = najemniško - tržno, 3 = 
najemniško - dr. članom, 4 = najemniško - 
neprofitno, 5 = najemniško - neznana vrsta 
najema, 6 = drugo (0: os. tu ne živi --> ni takega 
primera) 
  
amrp 
Št. Oseb, ki biva v isti nepremičnini 
Dodana spremenljivka 
acaow 
Osebno vozilo: 0 = ne, 1 = da 
  
aca 
Št. osebnih vozil, ki jih oseba ima 
Dodana spremenljivka 
adp 
Vrednost prihrankov 
Dodana spremenljivka 
ash 
Vrednost vrednostnih papirjev in lastniških 
deležev 
Dodana spremenljivka 
acamv 
Povprečna vrednost vozil 
Dodana spremenljivka 
xmp 
Plačane preživnine 
  
x1101 
Stroški dela 
Dodana spremenljivka 
x1103 
Stroški regresa 
Dodana spremenljivka 
x1109 
Stroški drugih obdavčljivih dohodkov iz 
zaposlitve 
Dodana spremenljivka 
x1211 
Stroški študentskega dela, upravičenega do 
posebne olajšave 
Dodana spremenljivka 
x1212 
Stroški študentskega dela, neupravičenega do 
posebne olajšave 
Dodana spremenljivka 
x1230 
Stroški dodatnega dela (pogodbeno delo) 
Dodana spremenljivka 
x4100 
Stroški oddajanja premoženja v najem 
Dodana spremenljivka 
x4200 
Stroški avtorskega honorarja 
Dodana spremenljivka 
x6700 
Stroški Fulbrightovega programa 
Dodana spremenljivka 
 
 
 
 


 
 105 
Priloga 2: Opredelitev list dohodkov uporabljenih v modelu SLOmod 
Oznaka liste 
dohodka 
Naziv liste dohodka 
Upoštevani dohodki, 
nadomestila, 
transferji, liste 
dohodkov 
Naziv upoštevanih dohodkov, 
nadomestil, transferjev, list dohodkov 
ils_origy 
Osnovni dohodek 
+ yemtx 
Obdavčljivi dohodek iz zaposlitve (plača) 
 
 
+ yemhl 
Regres za letni dopust 
 
 
+ yemot 
Drugi obdavčljivi dohodki iz zaposlitve 
 
 
+ yemnt 
Neobdavčljivi dohodek iz zaposlitve 
 
 
+ yse00 
Dohodek iz samozaposlitve  
 
 
+ ysen 
Dohodek iz samozaposlitve – normiranci 
 
 
+ yseag 
Dohodek iz samozaposlitve – kmetijska 
dejavnost 
 
 
+ yaj01 
Dohodek iz dodatne zaposlitve 1 (verski 
delavci) 
 
 
+ yaj02 
Dohodek iz dodatne zaposlitve 2 
(pogodbeno delo) 
 
 
+ yst 
Dohodek študentov, upravičenih do 
posebne olajšave 
 
 
+ ystw 
Dohodek študentov, neupravičenih do 
posebne olajšave 
 
 
+ yprrt 
Dohodek iz oddajanja premoženja v 
najem 
 
 
+ yiyitdp 
Kapitalski dohodek – obresti dosežene na 
denarne depozite 
 
 
+ yiyot 
Kapitalski dohodek – ostalo 
 
 
+ yot 
Drugi dohodki 
 
 
+ yro 
Avtorski honorar  
 
 
- xmp 
Plačane preživnine 
 
 
+ yptmp 
Prejete preživnine 
ils_pen 
Pokojnine  
+ poa00 
Starostna pokojnina 
 
 
+ pdi00 
Invalidska pokojnina 
 
 
+ psu00 
Družinska in vdovska pokojnina 
ils_benmt 
Socialni transferji, vezani na 
osebni prejemek/premoženje + bchmt_s 
Otroški dodatek 
 
 
+ bchba_s 
Pomoč ob rojstvu otroka (le za leto 2017) 
 
 
+ bchlg_s 
Dodatek za veliko družino (za leti 2017 in 
2018) 
 
 
+ bsa_s 
Socialna pomoč 
 
 
+ baspm_s 
Varstveni dodatek 
 
 
+ bsafu_s 
Pogrebnina  
 
 
+ bsawd_s 
Posmrtnina  
 
 
+bsaec 
Izredna socialna denarna pomoč 
 
 
+ bedmt_s 
Državna štipendija 
 
 
+ bho_s 
Subvencija najemnine 
ils_bennt 
Socialni transferji, ki niso 
vezani na osebni 
prejemek/premoženje 
+ bcrsvcc 
Delno plačilo za izgubljeni dohodek zaradi 
nege otroka 
 
 
+ bdica 
Dodatek za pomoč in postrežbo 
 
 
+ bchba_s 
Pomoč ob rojstvu otroka (od leta 2018 
dalje) 
 
 
+ bchlg_s 
Dodatek za veliko družino (od leta 2019 
dalje) 
 
 
+ bcham 
Nadomestilo preživnine 
 
 
+bmanc_s 
Starševski dodatek  
 
 
+ bmact / bmact_s 
Materinsko in starševsko nadomestilo 


106 
EkonomIERa  
03-2023 
Oznaka liste 
dohodka 
Naziv liste dohodka 
Upoštevani dohodki, 
nadomestila, 
transferji, liste 
dohodkov 
Naziv upoštevanih dohodkov, 
nadomestil, transferjev, list dohodkov 
 
 
+ bcrbafh/ bcrbafh_s 
Očetovsko nadomestilo 
 
 
+ bdirw 
Denarna nadomestila delovnim invalidom 
 
 
+ bednm01 
Zoisova štipendija 
 
 
+ bednm02 
Deficitarna štipendija 
 
 
+ bhl 
Bolniško nadomestilo 
 
 
+ bchcc 
Dodatek za nego otroka 
 
 
+ bdixp 
Invalidnina  
 
 
+ bunct/bunct_s 
Denarno nadomestilo za brezposelne 
ils_ben 
Socialni transferji 
+ ils_pen 
Pokojnine  
 
 
+ ils_benmt 
Socialni transferji, vezani na osebni 
prejemek/premoženje 
 
 
+ ils_bennt 
Socialni transferji, ki niso vezani na osebni 
prejemek/premoženje 
ils_taxsim 
Simulirani davki 
+ tiy_s 
Davek na kapital 
 
 
+ tin00_s 
Dohodnina  
ils_tax 
Davki  
+ ils_taxsim 
Simulirani davki 
 
 
+ tprrt 
Davek iz oddajanja premoženja v najem 
ils_sicdy 
Prispevki za socialno varnost 
+ ils_sicee 
Prispevki za socialno varnost zavarovanca 
 
 
+ ils_sicot 
Drugi prispevki za socialno varnost (iz 
naslova nadomestil in starševskega 
dodatka) 
ils_dispy 
Razpoložljivi dohodek 
+ ils_origy 
Osnovni dohodek 
 
 
+ ils_ben 
Socialni transferji 
 
 
- ils_tax 
Davki  
 
 
- ils_sicdy 
Prispevki za socialno varnost 
ils_base_tin 
Obdavčljivi dohodek, pred 
upoštevanjem stroškov 
+ yemtx 
Obdavčljivi dohodek iz zaposlitve (plača) 
 
 
+ yemhl 
Regres za letni dopust 
 
 
- sin19_s 
Neobdavčljivi del regresa 
 
 
+ yemot 
Drugi obdavčljivi dohodki iz zaposlitve 
 
 
+ yse00 
Dohodek iz samozaposlitve  
 
 
+ ysen 
Dohodek iz samozaposlitve – normiranci 
 
 
+ yseag 
Dohodek iz samozaposlitve – kmetijska 
dejavnost 
 
 
+ yst  
Dohodek študentov, upravičenih do 
posebne olajšave 
 
 
+ ystw 
Dohodek študentov, neupravičenih do 
posebne olajšave 
 
 
+ yaj01 
Dohodek iz dodatne zaposlitve 1 (verski 
delavci) 
 
 
+ yaj02 
Dohodek iz dodatne zaposlitve 2 
(pogodbeno delo) 
 
 
+ yro 
Avtorski honorar 
 
 
+ yot 
Drugi dohodki  
 
 
+ Ils_pen 
Pokojnine (starostna, invalidska in 
družinska in vdovska) 
 
 
+ bmact / bmact_s 
Materinsko in starševsko nadomestilo 
 
 
+ bcrbafh/ bcrbafh_s 
Očetovsko nadomestilo 
 
 
+ bunct/bunct_s 
Denarno nadomestilo za brezposelne 
 
 
+ bdirw 
Denarna nadomestila delovnim invalidom 
 
 
+ bhl 
Bolniško nadomestilo 
 
 
+ ypp 
Zasebna pokojnina 


 
 107 
Oznaka liste 
dohodka 
Naziv liste dohodka 
Upoštevani dohodki, 
nadomestila, 
transferji, liste 
dohodkov 
Naziv upoštevanih dohodkov, 
nadomestil, transferjev, list dohodkov 
 
 
+ bcrsvcc 
Delno plačilo za izgubljeni dohodek zaradi 
nege otroka 
 
 
+ tscctfa01 
Pravica do plačila prispevkov iz naslova 
krajšega delovnega časa 
 
 
+ tscctfa03 
Pravica do plačila prispevkov zaradi 
varovanja štirih ali več otrok 
il_ITbase0 
Obdavčljivi dohodek, po 
upoštevanju stroškov 
+ ils_base_tin 
Obdavčljivi dohodek pred upoštevanjem 
stroškov 
 
 
- x1101 
Stroški dela 
 
 
- x1103 
Stroški regresa 
 
 
- x1109 
Stroški drugih obdavčljivih dohodkov iz 
zaposlitve 
 
 
- x1211 
Stroški študentskega dela, upravičenega 
do posebne olajšave 
 
 
- x1212 
Stroški študentskega dela, 
neupravičenega do posebne olajšave 
 
 
- x1230 
Stroški dodatnega dela (pogodbeno delo) 
 
 
- x4200 
Stroški avtorskega honorarja 
 
 
- x6700 
Stroški Fulbrightovega programa 
il_ITbase1 
Vmesna davčna osnova 
+ il_ITbase0 
Obdavčljivi dohodek po upoštevanju 
stroškov 
 
 
- ils_sicee 
Prispevki za socialno varnost zavarovanca 
 
 
- ils_sicot 
Drugi prispevki za socialno varnost (iz 
naslova nadomestil in starševskega 
dodatka) 
 
 
- tscctfa01_s 
Pravica do plačila prispevkov iz naslova 
krajšega delovnega časa 
 
 
- tscctfa03_s 
Pravica do plačila prispevkov zaradi 
varovanja štirih ali več otrok 
il_ITbase2 
Končna davčna osnova 
+ il_ITbase1 
Vmesna davčna osnova 
 
 
- tinta_s 
Celotna davčna olajšava 
il_CBmeans 
Dohodek za določitev 
otroškega dodatka 
+ il_ITbase0 
Obdavčljivi dohodek po upoštevanju 
stroškov 
 
 
+ ysen 
Dohodek iz samozaposlitve – normiranci  
 
 
- ils_sicee 
Prispevki za socialno varnost zavarovanca 
 
 
- ils_sicot 
Drugi prispevki za socialno varnost (iz 
naslova nadomestil in starševskega 
dodatka) 
 
 
- tin00_s 
Dohodnina  
 
 
- tiy_s 
Davek na kapital 
 
 
+ bcham 
Nadomestilo preživnine 
 
 
+ bmanc_s 
Starševski dodatek 
 
 
+ yiy 
Dohodek iz kapitala 
 
 
+ yprrt 
Dohodek iz oddajanja premoženja v 
najem (za leta 2017–2019 znižan za 10 %, 
od 2020 dalje znižan za 15 %) 
 
 
- xmp 
Plačane preživnine 
 
 
+ yptmp 
Prejete preživnine 
 
 
+ bdixp 
Invalidnina  
il_asset 
Premoženje po zupjs 
+ amr00_s 
Nepremičnina – stanovanje/hiša  
 
 
+ aotmv00 
Druge nepremičnine 
 
 
+ aca_s 
Osebno vozilo 
 
 
+ adp 
Prihranki 


108 
EkonomIERa  
03-2023 
Oznaka liste 
dohodka 
Naziv liste dohodka 
Upoštevani dohodki, 
nadomestila, 
transferji, liste 
dohodkov 
Naziv upoštevanih dohodkov, 
nadomestil, transferjev, list dohodkov 
 
 
+ ash 
Vrednostni papirji in lastniški deleži 
il_SAasset 
Premoženje po zsvar 
+ amr01_s 
Nepremičnina – stanovanje/hiša (do 
vrednosti 120.000 EUR se ne upošteva) 
 
 
+ aotmv00 
Druge nepremičnine 
 
 
+ aca_s 
Osebno vozilo 
 
 
+ adp_s 
Prihranki po ZSVAR 
 
 
+ ash 
Vrednostni papirji in lastniški deleži 
il_yocc 
Občasni dohodki brez 
upoštevanja kapitalskih 
dohodkov (za izračun DSP) 
+ yst 
Dohodek študentov, upravičenih do 
posebne olajšave 
 
 
+ ystw 
Dohodek študentov, neupravičenih do 
posebne olajšave 
 
 
+ yaj01 
Dohodek iz dodatne zaposlitve 1 (verski 
delavci) 
 
 
+ yaj02 
Dohodek iz dodatne zaposlitve 2 
(pogodbeno delo) 
 
 
+ yro 
Avtorski honorar 
 
 
+ yot 
Drugi dohodki  
 
 
- x1211 
Stroški študentskega dela, upravičenega 
do posebne olajšave 
 
 
- x1212 
Stroški študentskega dela, 
neupravičenega do posebne olajšave 
 
 
- x1230 
Stroški dodatnega dela (pogodbeno delo) 
 
 
- x4200 
Stroški avtorskega honorarja 
 
 
- x6700 
Stroški Fulbrightovega programa 
il_yreg 
Redni dohodki brez 
upoštevanja plače (za izračun 
DSP) 
+ yse00 
Dohodek iz samozaposlitve  
 
 
+ ysen 
Dohodek iz samozaposlitve – normiranci 
 
 
+ yseag 
Dohodek iz samozaposlitve – kmetijska 
dejavnost 
 
 
+ ils_pen 
 
 
 
+ bmact/+bmact_s 
Materinsko in starševsko nadomestilo 
 
 
+ bcrbafh/+bcrbafh_s 
Očetovsko nadomestilo 
 
 
+ bdirw 
Denarna nadomestila delovnim invalidom 
 
 
+ bunct/+bunct_s 
Pokojnine (starostna, invalidska in 
družinska in vdovska) 
 
 
+ bhl 
Bolniško nadomestilo 
 
 
+ ypp 
Zasebna pokojnina 
 
 
+ bcrsvcc 
Delno plačilo za izgubljeni dohodek zaradi 
nege otroka 
 
 
- x1101 
Stroški dela 
 
 
- x1103 
Stroški regresa 
il_sic_base 
Osnova za prispevke 
zavarovanca in delodajalca 
+ yemtx 
Obdavčljivi dohodek iz zaposlitve (plača) 
 
 
+ yemot 
Drugi obdavčljivi dohodki iz zaposlitve 
 
 
+ yemhl 
Regres za letni dopust 
 
 
- sin19_s 
Neobdavčljivi del regresa 
 
 
+ bhl 
Bolniško nadomestilo 
il_ymy01–12  
+ il_yreg 
Redni dohodki brez upoštevanja plače 
 
 
+ il_yocc 
Občasni dohodki brez upoštevanja 
kapitalskih dohodkov 


 
 109 
Oznaka liste 
dohodka 
Naziv liste dohodka 
Upoštevani dohodki, 
nadomestila, 
transferji, liste 
dohodkov 
Naziv upoštevanih dohodkov, 
nadomestil, transferjev, list dohodkov 
 
 
+ yprrt 
Dohodek iz oddajanja premoženja v 
najem 
 
 
- x4100 
Stroški oddajanja premoženja v najem 
 
 
- tprrt_s 
Davek iz oddajanja premoženja v najem 
 
 
+ yiy 
Dohodek iz kapitala 
 
 
- tiy_s 
Davek na kapitalski dohodek 
 
 
+ yemtx01-12 
Obdavčljivi dohodek iz zaposlitve (plača) 
januar–december 
 
 
+ yemot01-12 
Drugi dohodki iz delovnega razmerja 
januar–december 
 
 
+ yemhl01-12 
Regres januar–december 
 
 
- int_sicee01-12 
Prispevki zavarovanca januar–december 
 
 
- tin01_s-12_s 
Dohodnina januar–december  
 
 
+ int_yst_ded 
Upošteva se celoten dohodek študentov 
(ne le dohodek nad zneskom minimalne 
plače kot pri otroškem dodatku, državni 
štipendiji in vrtcu; velja le za leto 2022) 
 
 
+ bchmt_s 
Otroški dodatek 
 
 
- int_bchmt_ded 
20 % višine otroškega dodatka za prvega 
otroka iz prvega dohodkovnega razreda 
 
 
+ bmanc_s 
Starševski dodatek 
 
 
- xmp 
Plačane preživnine 
 
 
+ yptmp 
Prejete preživnine 
Opomba: Končnica »_s« predstavlja simulirano vrednost. Pripis »ils_« pred oznako liste dohodka 
predstavlja: standardne liste dohodkov, poenotene med EU državami. Pripis »il_« pred oznako liste 
dohodka predstavlja: liste dohodkov, specifične za SI. Znak »-« ali »+« pred upoštevanim dohodkom, 
nadomestilom, transferjem ali listo dohodkov (tretji stolpec) pomeni, da posamezen dohodek, 
nadomestilo, transfer ali listo dohodka odštejemo oziroma prištejemo, da oblikujemo posamezno listo 
dohodka (prvi stolpec).  


110 
EkonomIERa  
03-2023 
Priloga 3: Podatki simulacij za leta 2018–202116 
Ne simulirani dohodki in simulirani dohodnina ter socialni prispevki v primerjavi z zunanjimi podatki – zneski (v milijonih EUR), 2018–2021   
Dohodki, dohodnina in socialni prispevki 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji podatki (zp) 
Razmerje SLOmod/zp 
 
2018 2019 2020 2021 2018 2019 2020 2021 2018 2019 2020 2021 
Obdavčljivi dohodek iz zaposlitve (plača) (yemtx) 
14.743 15.263 15.897 17.279 15.257 16.338 17.008 
n.p. 
0,97 
0,93 
0,93 
n.p. 
Dohodki iz zaposlitve (yem) 
15.687 16.243 16.925 18.374 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Dohodek iz samozaposlitve (yse00) 
461 
477 
453 
490 
434 
430 
362 
n.p. 
1,06 
1,11 
1,25 
n.p. 
Dohodek iz samozaposlitve - kmetijska dejavnost (yseag) 
102 
103 
113 
122 
108 
123 
116 
n.p. 
0,95 
0,84 
0,97 
n.p. 
Dohodek iz samozaposlitve – normiranci (ysen) 
229 
236 
225 
243 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Avtorski honorar (yro) 
6 
5 
5 
5 
10 
10 
10 
n.p. 
0,59 
0,56 
0,51 
n.p. 
Dohodek študentov, upravičenih do posebne olajšave (yst) 
232 
236 
220 
238 
250 
249 
193 
n.p. 
0,93 
0,95 
1,14 
n.p. 
Dohodek študentov, neupravičenih do posebne olajšave (ystw) 
5 
5 
4 
5 
4 
4 
3 
n.p. 
1,17 
1,31 
1,57 
n.p. 
Dohodek iz dodatne zaposlitve 1 (yaj01) 
0 
1 
1 
1 
0 
0 
0 
n.p. 
1,26 
1,28 
1,26 
n.p. 
Dohodek iz dodatne zaposlitve 2 (yaj02) 
220 
230 
239 
258 
217 
223 
200 
n.p. 
1,01 
1,03 
1,19 
n.p. 
Starostna pokojnina (poa00) 
3.626 3.724 3.901 4.078 3.484 3.646 3.913 4.164 
1,04 
1,02 
1,00 
0,98 
Invalidska pokojnina (pdi00) 
488 
501 
525 
549 
480 
482 
492 
500 
1,02 
1,04 
1,07 
1,10 
Družinska in vdovska pokojnina (psu00) 
385 
395 
414 
433 
484 
491 
504 
513 
0,79 
0,81 
0,82 
0,84 
Dohodnina (il_itbase0) 
2.003 2.142 2.152 2.486 2.111 2.156 2.139 
n.p. 
0,95 
0,99 
1,01 
n.p. 
Prispevki za socialno varnost za zaposlene (ils_sicee) 
3.379 3.494 3.634 3.948 3.471 3.730 3.885 4.235 
0,97 
0,94 
0,94 
0,93 
Prispevki za socialno varnost za delodajalce (ils_sicer) 
2.480 2.565 2.651 2.880 2.578 2.766 2.858 3.117 
0,96 
0,93 
0,93 
0,92 
Prispevki za socialno varnost za samozaposlene (ils_sicse) 
359 
374 
383 
408 
348 
364 
360 
390 
1,03 
1,03 
1,06 
1,05 
Vir: MF (2020–2022a, 2022b), ZPIZ (2019-2022) in lastni izračuni.  
 
 
16 Leto 2022 ni vključeno v izračune tega dela, saj v času priprave (januar 2023) uradnih (popolnih) podatkov za leto 2022, ki bi nam omogočali smiselno 
primerjavo simuliranih rezultatov z zunanjo statistiko, še ni bilo na voljo. 


 
 111 
Ne simulirani dohodki in simulirani dohodnina ter socialni prispevki v primerjavi z zunanjimi podatki – število (v tisočih), 2018–2021  
Dohodki, dohodnina in socialni prispevki 
Legenda: Razlika v razmerju:  
SLOmod 
Zunanji podatki (zp) 
Razmerje SLOmod/zp 
 
2018 2019 2020 2021 2018 2019 2020 2021 2018 2019 2020 2021 
Obdavčljivi dohodek iz zaposlitve (plača) (yemtx) 
815 
815 
815 
815 
841 
857 
914 
n.p. 
0,97 
0,95 
0,89 
n.p. 
Dohodki iz zaposlitve (yem) 
846 
846 
846 
846 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Dohodek iz samozaposlitve (yse00) 
56 
56 
56 
56 
62 
59 
53 
n.p. 
0,90 
0,94 
1,06 
n.p. 
Dohodek iz samozaposlitve - kmetijska dejavnost (yseag) 
116 
116 
116 
116 
122 
137 
119 
n.p. 
0,95 
0,85 
0,97 
n.p. 
Dohodek iz samozaposlitve – normiranci (ysen) 
43 
43 
43 
43 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Avtorski honorar (yro) 
7 
7 
7 
7 
7 
7 
8 
n.p. 
1,00 
0,97 
0,88 
n.p. 
Dohodek študentov, upravičenih do posebne olajšave (yst) 
88 
88 
88 
88 
97 
95 
79 
n.p. 
0,91 
0,93 
1,11 
n.p. 
Dohodek študentov, neupravičenih do posebne olajšave (ystw) 
2 
2 
2 
2 
2 
1 
1 
n.p. 
1,14 
1,29 
1,54 
n.p. 
Dohodek iz dodatne zaposlitve 1 (yaj01) 
0 
0 
0 
0 
0 
0 
0 
n.p. 
1,17 
1,19 
1,17 
n.p. 
Dohodek iz dodatne zaposlitve 2 (yaj02) 
115 
115 
115 
115 
113 
112 
97 
0 
1,02 
1,03 
1,20 
n.p. 
Starostna pokojnina (poa00) 
404 
404 
404 
404 
445 
451 
459 
464 
0,91 
0,89 
0,88 
0,87 
Invalidska pokojnina (pdi00) 
67 
67 
67 
67 
80 
78 
76 
74 
0,84 
0,86 
0,88 
0,92 
Družinska in vdovska pokojnina (psu00) 
57 
57 
57 
57 
89 
88 
86 
84 
0,64 
0,66 
0,67 
0,69 
Dohodnina (il_itbase0) 
1.530 1.530 1.530 1.530 1.555 1.567 1.540 
n.p. 
0,98 
0,98 
0,99 
n.p. 
Prispevki za socialno varnost za zaposlene (ils_sicee) 
971 
970 
970 
970 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Prispevki za socialno varnost za delodajalce (ils_sicer) 
971 
970 
970 
970 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Prispevki za socialno varnost za samozaposlene (ils_sicse) 
107 
107 
107 
107 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Vir: MF (2020–2022a, 2022b), ZPIZ (2019-2022) in lastni izračuni.  
 
 


112 
EkonomIERa  
03-2023 
Simulirani starševski in družinski transferji v primerjavi z zunanjimi podatki – zneski (v milijonih EUR), 2018–2021 
Starševski in družinski transferji 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  podatki (zp) 
Razmerje SLOmod/zp 
   
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
Očetovsko nadomestilo (bcrbafh_s) 
12 
14 
15 
16 
244 
281 
292 
309 
0,87 
0,95 
0,97 
0,97 
Materinsko in starševsko nadomestilo (bmact_s) 
200 
253 
269 
285 
Starševski dodatek (bmanc_s) 
10 
10 
10 
15 
9 
8 
8 
11 
1,10 
1,28 
1,28 
1,44 
Pomoč ob rojstvu otroka (bchba_s) 
6 
6 
6 
7 
6 
5 
5 
7 
0,90 
1,06 
1,16 
0,93 
Dodatek za veliko družino (bchlg_s) 
10 
11 
11 
11 
11 
12 
13 
14 
0,89 
0,91 
0,86 
0,84 
Otroški dodatek (bchmt_s) 
281 
274 
277 
260 
247 
250 
251 
246 
1,13 
1,10 
1,10 
1,06 
Plačilo prispevkov iz naslova krajšega 
delovnega časa (tscctfa01_s in tscctfa02_s) 
19 
20 
21 
26 
18 
19 
20 
24 
1,03 
1,03 
1,07 
1,10 
Plačilo prispevkov zaradi zapustitve trga dela 
(tscctfa03_s in tscctfa04_s) 
4 
4 
4 
4 
3 
3 
3 
3 
1,03 
1,10 
1,18 
1,23 
Opomba: Očetovsko ter materinsko in starševsko nadomestilo sta v zunanjih podatkih poročana skupaj v okviru starševskih nadomestil.  
Vir: MDDSZ (2022) in lastni izračuni.  
 
 


 
 113 
Simulirani starševski in družinski transferji v primerjavi z zunanjimi podatki – število (v tisočih), 2018–2021 
Starševski in družinski transferji 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  podatki (zp) 
Razmerje SLOmod/zp 
   
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
Očetovsko nadomestilo (bcrbafh_s) 
13 
13 
13 
13 
22 
22 
22 
21 
2,00 
2,05 
2,08 
2,10 
Materinsko in starševsko nadomestilo 
(bmact_s) 
32 
32 
32 
32 
Starševski dodatek (bmanc_s) 
6 
6 
6 
6 
3 
3 
3 
3 
1,85 
2,19 
2,14 
1,99 
Pomoč ob rojstvu otroka (bchba_s) 
19 
19 
19 
19 
21 
18 
17 
21 
0,90 
1,08 
1,16 
0,92 
Dodatek za veliko družino (bchlg_s) 
24 
27 
27 
27 
27 
30 
32 
33 
0,88 
0,90 
0,85 
0,83 
Otroški dodatek (bchmt_s) 
348 
346 
345 
339 
307 
320 
325 
327 
1,14 
1,08 
1,06 
1,04 
Plačilo prispevkov iz naslova krajšega 
delovnega časa (tscctfa01_s in 
tscctfa02_s) 
21 
21 
21 
21 
14 
15 
14 
13 
1,46 
1,44 
1,48 
1,56 
Plačilo prispevkov zaradi zapustitve 
trga dela (tscctfa03_s in tscctfa04_s) 
1 
1 
1 
1 
1 
1 
1 
1 
1,25 
1,34 
1,43 
1,49 
Opombe: Očetovsko ter materinsko in starševsko nadomestilo sta v zunanjih podatkih poročana skupaj v okviru starševskih nadomestil. Za starševska 
nadomestila, starševski dodatek in obe pravici do plačila prispevkov simulirani podatki podajajo število prejemnikov v posameznem letu, zunanji podatki pa 
poročajo povprečno letno število upravičencev. V primeru otroškega dodatka simulirani podatki podajajo število upravičencev v posameznem letu, zunanji 
podatki pa poročajo povprečno letno število upravičencev. Medtem ko za pravici pomoč ob rojstvu otroka in dodatek za veliko družino simulirani podatki 
podajajo število prejemnikov v posameznem letu, zunanji podatki pa poročajo letno število upravičencev. 
Vir: MDDSZ (2022) in lastni izračuni.  
 


114 
EkonomIERa  
03-2023 
Simulirana subvencija prehrane za učence in dijake ter znižano plačilo vrtca v primerjavi z zunanjimi podatki – število (v tisočih), 2018–2021 
Subvencija šolske prehrane in znižano 
plačilo vrtca  
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  podatki (zp) 
Razmerje SLOmod/ baze 
   
2018 
2019 
202
0 
2021 
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
Subvencionirana malica (bedrd01_s) 
131 
133 
130 
118 
138 
137 
138 
129 
0,95 
0,98 
0,94 
0,91 
Subvencionirano kosilo (bedrd02_s) 
48 
46 
45 
40 
49 
48 
47 
44 
0,98 
0,96 
0,95 
0,92 
Znižano plačilo vrtca (bchedyc_s) 
79 
79 
79 
79 
73 
74 
75 
74 
1,08 
1,07 
1,06 
1,06 
Opombe: Pri pravici znižanega plačila vrtca simulirani podatki podajajo število vseh prejemnikov v posameznem letu, zunanji podatki pa navajajo povprečno 
letno število upravičencev. Simulirane vrednosti subvencije šolske prehrane za učence in dijake ter znižanega plačila vrtca lahko primerjamo le z vidika števila 
prejemnikov in ne tudi zneskov, saj zunanjih podatkov o znesku teh pravic nismo pridobili.  
Vir: MIZŠ (2022) in lastni izračuni.  
 
 


 
 115 
Simulirana socialna pomoč, varstveni dodatek, državna štipendija in subvencija najemnine v primerjavi z zunanjimi podatki – zneski (v 
milijonih EUR), 2018–2021 
Socialna pomoč, varstveni dodatek, državna štipendija 
in subvencija najemnine 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  podatki (zp) 
Razmerje SLOmod/ baze 
   
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
Denarna socialna pomoč (bsa_s) 
236 
284 
294 
281 
206 
246 
267 
270 
1,15 
1,16 
1,10 
1,04 
Varstveni dodatek (bsapm_s) 
35 
39 
39 
33 
33 
39 
42 
43 
1,07 
1,01 
0,91 
0,79 
Državna štipendija (bedmt_s) 
77 
84 
85 
76 
75 
84 
85 
84 
1,03 
1,00 
0,99 
0,91 
Državna štipendija – osnova (bedmt00_s) 
68 
73 
74 
67 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za uspeh 
(bedmtadd1_s) 
3 
4 
4 
3 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za bivanje 
(bedmtadd2_s) 
5 
6 
6 
6 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za posebne 
potrebe (bedmtadd3_s) 
1 
1 
1 
1 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Subvencija najemnine (bho_s) 
16 
20 
20 
20 
17 
19 
20 
21 
0,97 
1,09 
1,02 
0,94 
Pogrebnina (bsafu_s) 
3 
3 
3 
3 
4 
4 
4 
3 
0,82 
0,76 
0,74 
0,84 
Posmrtnina (bsawd_s) 
1 
1 
1 
1 
1 
2 
2 
1 
0,90 
0,66 
0,68 
0,77 
Vir: MDDSZ (2022) in lastni izračuni.  
 
 


116 
EkonomIERa  
03-2023 
Simulirana socialna pomoč, varstveni dodatek, državna štipendija in subvencija najemnine v primerjavi z zunanjimi podatki – število (v 
tisočih), 2018–2021 
Socialna pomoč, varstveni dodatek, 
državna štipendija in subvencija najemnine 
Legenda: Razlika v razmerju: 
SLOmod 
Zunanji  podatki (zp) 
Razmerje SLOmod/ baze 
   
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
2018 
2019 
2020 
2021 
Denarna socialna pomoč (bsa_s) 
67 
79 
78 
73 
82 
91 
99 
100 
0,81 
0,86 
0,79 
0,74 
Varstveni dodatek (bsapm_s) 
25 
28 
26 
22 
19 
20 
22 
23 
1,36 
1,36 
1,18 
0,95 
Državna štipendija (bedmt_s) 
71 
82 
81 
74 
49 
53 
55 
54 
1,45 
1,54 
1,48 
1,38 
Državna štipendija – osnova 
(bedmt00_s) 
71 
82 
81 
74 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za 
uspeh (bedmtadd1_s) 
16 
19 
19 
17 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za 
bivanje (bedmtadd2_s) 
8 
10 
10 
9 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Državna štipendija - dodatek za 
posebne potrebe (bedmtadd3_s) 
2 
3 
3 
2 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
n.p. 
Subvencija najemnine (bho_s) 
12 
15 
15 
15 
11 
12 
12 
13 
1,09 
1,29 
1,21 
1,16 
Pogrebnina (bsafu_s) 
4 
4 
4 
3 
5 
5 
5 
4 
0,75 
0,76 
0,74 
0,84 
Posmrtnina (bsawd_s) 
3 
3 
3 
3 
4 
5 
4 
4 
0,85 
0,67 
0,68 
0,77 
Opombe: Pri pravicah denarna socialna pomoč, varstveni dodatek, državna štipendija in subvencija najemnine simulirani podatki podajajo število vseh 
prejemnikov v posameznem letu, zunanji podatki pa navajajo povprečno letno število upravičencev.  
Vir: MDDSZ (2022) in lastni izračuni.  
 


 
 117 
KAZALO SLIK 
Slika 1: Otroški dodatek: Spremembe v porazdelitvi prejemnikov po dohodkovnih 
razredih ob uveljavitvi scenarijev v primerjavi z osnovnim scenarijem (v 
odstotnih točkah), leto 2017 ...................................................................................... 87 
Slika 2: Otroški dodatek: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 .......................................................... 87 
Slika 3: Izdatki za otroški dodatek ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v milijonih EUR), leto 2017 ................................................................ 88 
Slika 4: Znižano plačilo vrtca: Spremembe v porazdelitvi prejemnikov po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 .......................................................... 89 
Slika 5: Znižano plačilo vrtca: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 .......................................................... 90 
Slika 6: Izdatki za subvencijo vrtca ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v milijonih EUR), leto 2017 ................................................................ 90 
Slika 7: Državna štipendija: Spremembe v porazdelitvi prejemnikov po dohodkovnih 
razredih ob uveljavitvi scenarijev v primerjavi z osnovnim scenarijem (v 
odstotnih točkah), leto 2017 ...................................................................................... 91 
Slika 8: Državna štipendija: Spremembe v porazdelitvi izdatkov za pravico po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 .......................................................... 92 
Slika 9: Izdatki za državno štipendijo ob uveljavitvi scenarijev v primerjavi z 
osnovnim scenarijem (v milijonih EUR), leto 2017 ............................................ 92 
Slika 10: Dohodnina: Spremembe v porazdelitvi pobrane dohodnine po 
dohodkovnih razredih ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v odstotnih točkah), leto 2017 .......................................................... 93 
Slika 11: Pobrana dohodnina ob uveljavitvi scenarijev v primerjavi z osnovnim 
scenarijem (v milijonih EUR), leto 2017 ................................................................ 93 
 
 


118 
EkonomIERa  
03-2023 
 
 


 
 119 
KAZALO TABEL 
Tabela 1: Gospodinjstva in družine glede na simulirane in zunanje podatke, leti 
2017/18 ......................................................................................................................... 14 
Tabela 2: Porazdelitev oseb glede na ekonomski status, leto 2017 ............................ 18 
Tabela 3: Vključeni v formalno izobraževanje, leto 2017 ............................................... 20 
Tabela 4: Opredelitev dohodkov in nadomestil v mikropodatkih glede na opredelitev 
dohodkov po zakonu, ki ureja dohodnino (ZDoh) ......................................... 28 
Tabela 5: Opredelitev transferjev in nadomestil v mikropodatkih ............................... 33 
Tabela 6: Ne simulirani dohodki in simulirana dohodnina v primerjavi z zunanjimi 
podatki – zneski (v EUR), leto 2017 ..................................................................... 44 
Tabela 7: Ne simulirani dohodki in simulirana dohodnina v primerjavi z zunanjimi 
podatki – število, leto 2017 .................................................................................... 45 
Tabela 8: Primerjava porazdelitve simulirane dohodnine po davčnih razredih z 
zunanjimi podatki, 2017.......................................................................................... 46 
Tabela 9: Primerjava porazdelitve simuliranega števila davčnih zavezancev po 
davčnih razredih z zunanjimi podatki, 2017 .................................................... 46 
Tabela 10: Simulirani starševski in družinski transferji v primerjavi z zunanjimi in 
mikropodatki (IS CSD baze) – zneski (v EUR), leto 2017 ............................. 49 
Tabela 11: Simulirani starševski in družinski transferji v primerjavi z zunanjimi in 
mikropodatki (IS CSD baze) – število, leto 2017 ............................................. 49 
Tabela 12: Simulirana subvencija prehrane za učence in dijake ter znižano plačilo 
vrtca v primerjavi z zunanjimi in mikropodatki (IS CSD baze) – število, 
leto 2017 ....................................................................................................................... 51 
Tabela 13: Simulirana socialna pomoč, varstveni dodatek, državna štipendija in 
subvencija najemnine v primerjavi z zunanjimi in mikropodatki (IS CSD 
baze) – zneski (v EUR), leto 2017 ......................................................................... 54 
Tabela 14: Simulirana socialna pomoč, varstveni dodatek, državna štipendija in 
subvencija najemnine v primerjavi z zunanjimi in mikropodatki (IS CSD 
baze) – število, leto 2017 ......................................................................................... 55 
Tabela 15: Simulirani podatki S01: Sprememba vrednosti socialnih transferjev v S01 
glede na osnovni scenarij (v milijonih) ............................................................... 60 
Tabela 16: Simulirani podatki S01: Sprememba števila prejemnikov socialnih 
transferjev v S01 glede na osnovni scenarij (v tisočih) ................................. 61 


120 
EkonomIERa  
03-2023 
Tabela 17: Simulirani podatki S01: Povprečni ekvivalentni razpoložljivi dohodek na 
člana gospodinjstva po decilih (v EUR) ............................................................... 62 
Tabela 18: Simulirani podatki S01: Zmagovalci in poraženci ........................................ 63 
Tabela 19: Simulirani podatki S01: Kazalniki dohodkovne neenakosti ...................... 63 
Tabela 20: Simulirani podatki S01: Stopnje tveganja revščine ...................................... 64 
Tabela 21: Simulirani podatki S02: Sprememba vrednosti socialnih transferjev v S02 
glede na osnovni scenarij (v milijonih) ............................................................... 67 
Tabela 22: Simulirani podatki S02: Sprememba števila prejemnikov socialnih 
transferjev v S02 glede na osnovni scenarij (v tisočih) ................................. 68 
Tabela 23: Simulirani podatki S02: Povprečni ekvivalentni razpoložljivi dohodek na 
člana gospodinjstva po decilih (v EUR) ............................................................... 69 
Tabela 24: Simulirani podatki S02: Zmagovalci in poraženci ........................................ 70 
Tabela 25: Simulirani podatki S02: Kazalniki dohodkovne neenakosti ...................... 70 
Tabela 26: Simulirani podatki S02: Stopnje tveganja revščine ...................................... 71 
Tabela 27: Simulirani podatki S03: Sprememba vrednosti socialnih transferjev v S03 
glede na osnovni scenarij (v milijonih) ............................................................... 74 
Tabela 28: Simulirani podatki S03: Sprememba števila prejemnikov socialnih 
transferjev v S03 glede na osnovni scenarij (v tisočih) ................................. 75 
Tabela 29: Simulirani podatki S03: Povprečni ekvivalentni razpoložljivi dohodek na 
člana gospodinjstva po decilih (v EUR) ............................................................... 76 
Tabela 30: Simulirani podatki S03: Zmagovalci in poraženci ........................................ 77 
Tabela 31: Simulirani podatki S03: Kazalniki dohodkovne neenakosti ...................... 77 
Tabela 32: Simulirani podatki S03: Stopnje tveganja revščine ...................................... 78 
Tabela 33: Simulirani podatki S04: Sprememba vrednosti socialnih transferjev v S04 
glede na osnovni scenarij (v milijonih) ............................................................... 80 
Tabela 34: Simulirani podatki S04: Sprememba števila prejemnikov socialnih 
transferjev v S04 glede na osnovni scenarij (v tisočih) ................................. 81 
Tabela 35: Simulirani podatki S04: Povprečni ekvivalentni razpoložljivi dohodek na 
člana gospodinjstva po decilih (v EUR) ............................................................... 82 
Tabela 36: Simulirani podatki S04: Zmagovalci in poraženci ........................................ 83 
Tabela 37: Simulirani podatki S04: Kazalniki dohodkovne neenakosti ...................... 83 
Tabela 38: Simulirani podatki S04: Stopnje tveganja revščine ...................................... 84 
 
 


 




