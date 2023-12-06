import gmpy2
from Crypto.Util.number import long_to_bytes
from sympy.ntheory.modular import crt

N1 = int(
    "646904894760287467742318109486293509280580014135961865392444595616044986546825166715954740483544017233833511816168053145387172802081980579852280486113519964392329512219111501076740096456306173456902777199117385768308480625540049023337455983011697093413984111821824639960181910855761685023791812138931830494490341523436346061412549322649545995417318536374645297474617511874926046075483237078401380801899738487002556384937038336321289972068697938445050630146664514144948185981474091077386812448676450556585731222561480223045395658134699994797309267377968147057980552509341528515872672041153937164362915537",
)
c1 = int(
    "568709196259211352091325038735067423523903894344288952092472331581709718124288515699142122562765658908977308137147791014891882034429253612888716776123755087890383972829206469540390411374311142179663314371282391186215782615391427876168068776449974111466662029138959376483040473931851444811815760940897709030023729920008827898002086229469412007663304474091093189240172285252435191151824318825705670591759789590766400712650168113914773038228624112453860483151259727905629577762469763269201399144849197705388738638186192763590717687482846960249277451260365010314479643482002906980229997804195850974258534332",
)

N2 = int(
    "677766783011896611808617554966196608983963773749721499179200755407103109197869368636200811069065374998738512762202347056266849779916957156289157170961060851751657790446040167715855933639218298576902634590237928444091842846461704131768572261505135382198374076448840067936248196838572415134048641467562270328213993011863944749160082934281804457458074350653246419559493617622171821369237858698848483674765683518601719571340669199396187392505304526786336111126536499456096381824266398349984669463121664749241217428416716245660367787558386893887507350891512718870578576378433952776846193677440783754098905303",
)
c2 = int(
    "515846441631591779078425037017957202311264857266544957502076336186223729419394911558693733893266881712695671601722544504698477546009237718742791421848188173536627817652594922353201206303454745705099682834382659275551720143073131911114343190950629696545583358502669126378668060847210740799196533083886157612945024700610103957315304263758250581287581041615802498569524713948884156832486358496845999021100605099546561203483324996655710212914546535098453666500064451397877985477021004139937651790974659652289668846747486274114460630082584425488375467584583095325372389473932669241114682761826224691980808541",
)

N3 = int(
    "611842575197939285314740301033642412902876723925583892595721339294423892462210954981850836392143315875841588891180205157785050914076569163008989584159439265921330625708157406148947559054599570205187738649364273712790827139741045940072733039453398704344518641100236786060665789454388154186363489792497758901243435908293949943790898752740554438608693957610340065645638450386453002593479601897688482225770517450362389715954432228951218937001534755212585438569266104428524379563250894865923967187482039920054979384089155157960474283425817598781326455819360216842435013332362498262892239524451947604574316719",
)
c3 = int(
    "211240137270611363712813085032137722021321731240929751605197952369742709257564613724764919803504432738633157740772598284030924760631796218312082347056610540194775774587641713021364490163325245816137170218981867644962682093598858265944625879085194407877445801903452946113032322438038721646642275483807609256466692069107509586142802060992054239501674429442699975477676790395432166574714308407620208263529482091509017891611172243473834183481473949756705750707756445773023107331199395687665948314283474595941273702328674391212126861651696893183701812825863604848856800270902150056440341144731137122492193650",
)

e = 17
n = [N1, N2, N3]
c = [c1, c2, c3]
resultant, mod = crt(n, c)
value, is_perfect = gmpy2.iroot(resultant, e)
print(long_to_bytes(value))
