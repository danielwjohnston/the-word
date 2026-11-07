#!/usr/bin/env python3
"""One-time conversion of section C phrase headings from English-first (LSV
phrase) to original-first: SBLGNT Greek, transliteration, and this book's own
gloss in single quotes. Idempotent: headings already converted are left alone.

Usage: python3 -I tools/greek_headings.py
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAP = {
 # ch01
 '"Judas"': ('Ἰούδας', 'Ioudas', 'Judas'),
 '"a servant of Jesus Christ"': ('Ἰησοῦ Χριστοῦ δοῦλος', 'Iēsou Christou doulos', 'a slave of Jesus Christ'),
 '"and brother of James"': ('ἀδελφὸς δὲ Ἰακώβου', 'adelphos de Iakōbou', 'and brother of James'),
 '"to those called"': ('κλητοῖς', 'klētois', 'to those called'),
 '"having been loved in God [the] Father"': ('ἐν θεῷ πατρὶ ἠγαπημένοις', 'en theō patri ēgapēmenois', 'loved in God the Father'),
 '"and having been kept in Jesus Christ"': ('καὶ Ἰησοῦ Χριστῷ τετηρημένοις', 'kai Iēsou Christō tetērēmenois', 'and kept for Jesus Christ'),
 '"mercy and peace and love"': ('ἔλεος … καὶ εἰρήνη καὶ ἀγάπη', 'eleos … kai eirēnē kai agapē', 'mercy and peace and love'),
 '"be multiplied to you!"': ('ὑμῖν … πληθυνθείη', 'hymin … plēthyntheiē', 'may it be multiplied to you'),
 # ch02
 '"Beloved"': ('Ἀγαπητοί', 'Agapētoi', 'beloved'),
 '"using all diligence to write to you concerning our common salvation"': ('πᾶσαν σπουδὴν ποιούμενος γράφειν ὑμῖν περὶ τῆς κοινῆς ἡμῶν σωτηρίας', 'pasan spoudēn poioumenos graphein hymin peri tēs koinēs hēmōn sōtērias', 'making every effort to write to you about our common salvation'),
 '"I had necessity to write to you"': ('ἀνάγκην ἔσχον γράψαι ὑμῖν', 'anankēn eschon grapsai hymin', 'I found it necessary to write to you'),
 '"exhorting [you]"': ('παρακαλῶν', 'parakalōn', 'urging you'),
 '"to fight for the faith"': ('ἐπαγωνίζεσθαι τῇ … πίστει', 'epagōnizesthai tē … pistei', 'to contend for the faith'),
 '"once delivered to the holy ones"': ('τῇ ἅπαξ παραδοθείσῃ τοῖς ἁγίοις', 'tē hapax paradotheisē tois hagiois', 'handed down once for all to the saints'),
 '"for there came in certain men stealthily"': ('παρεισέδυσαν γάρ τινες ἄνθρωποι', 'pareisedysan gar tines anthrōpoi', 'for certain people have slipped in'),
 '"having been written beforehand to this judgment long ago"': ('οἱ πάλαι προγεγραμμένοι εἰς τοῦτο τὸ κρίμα', 'hoi palai progegrammenoi eis touto to krima', 'written up long ago for this judgment'),
 '"impious"': ('ἀσεβεῖς', 'asebeis', 'impious'),
 '"perverting the grace of our God to licentiousness"': ('τὴν τοῦ θεοῦ ἡμῶν χάριτα μετατιθέντες εἰς ἀσέλγειαν', 'tēn tou theou hēmōn charita metatithentes eis aselgeian', 'turning the grace of our God into licentiousness'),
 '"and denying our only Master and Lord—Jesus Christ"': ('καὶ τὸν μόνον δεσπότην καὶ κύριον ἡμῶν Ἰησοῦν Χριστὸν ἀρνούμενοι', 'kai ton monon despotēn kai kyrion hēmōn Iēsoun Christon arnoumenoi', 'and denying our only Master and Lord, Jesus Christ'),
 # ch03
 '"Now I intend to remind you, you once having known all this"': ('Ὑπομνῆσαι δὲ ὑμᾶς βούλομαι, εἰδότας ὑμᾶς ἅπαξ πάντα', 'Hypomnēsai de hymas boulomai, eidotas hymas hapax panta', 'I want to remind you, though you once knew all things'),
 '"that Jesus, having saved a people out of the land of Egypt"': ('ὅτι Ἰησοῦς λαὸν ἐκ γῆς Αἰγύπτου σώσας', 'hoti Iēsous laon ek gēs Aigyptou sōsas', 'that Jesus, having saved a people out of the land of Egypt'),
 '"He secondly destroyed those not having believed"': ('τὸ δεύτερον τοὺς μὴ πιστεύσαντας ἀπώλεσεν', 'to deuteron tous mē pisteusantas apōlesen', 'afterward destroyed those who did not believe'),
 '"messengers also, those who did not keep their own principality"': ('ἀγγέλους τε τοὺς μὴ τηρήσαντας τὴν ἑαυτῶν ἀρχήν', 'angelous te tous mē tērēsantas tēn heautōn archēn', 'and the angels who did not keep their own position'),
 '"but left their proper dwelling"': ('ἀλλὰ ἀπολιπόντας τὸ ἴδιον οἰκητήριον', 'alla apolipontas to idion oikētērion', 'but abandoned their own dwelling'),
 '"He has kept in eternal bonds under darkness until [the] judgment of [the] great day"': ('εἰς κρίσιν μεγάλης ἡμέρας δεσμοῖς ἀϊδίοις ὑπὸ ζόφον τετήρηκεν', 'eis krisin megalēs hēmeras desmois aidiois hypo zophon tetērēken', 'he has kept in everlasting chains under gloom for the judgment of the great day'),
 '"as Sodom and Gomorrah, and the cities around them"': ('ὡς Σόδομα καὶ Γόμορρα καὶ αἱ περὶ αὐτὰς πόλεις', 'hōs Sodoma kai Gomorra kai hai peri autas poleis', 'just as Sodom and Gomorrah and the cities around them'),
 '"in like manner to these [messengers]"': ('τὸν ὅμοιον τρόπον τούτοις', 'ton homoion tropon toutois', 'in the same way as these'),
 '"having given themselves to whoredom"': ('ἐκπορνεύσασαι', 'ekporneusasai', 'having given themselves over to sexual immorality'),
 '"and having gone after other flesh"': ('καὶ ἀπελθοῦσαι ὀπίσω σαρκὸς ἑτέρας', 'kai apelthousai opisō sarkos heteras', 'and having gone after other flesh'),
 '"have been set before [as] an example"': ('πρόκεινται δεῖγμα', 'prokeintai deigma', 'are set out as an example'),
 '"undergoing the justice of continuous fire"': ('πυρὸς αἰωνίου δίκην ὑπέχουσαι', 'pyros aiōniou dikēn hypechousai', 'undergoing the penalty of eternal fire'),
 # ch04
 '"In like manner, nevertheless"': ('Ὁμοίως μέντοι', 'Homoiōs mentoi', 'yet in the same way'),
 '"those dreaming"': ('καὶ οὗτοι ἐνυπνιαζόμενοι', 'kai houtoi enypniazomenoi', 'these too, dreaming'),
 '"indeed defile the flesh"': ('σάρκα μὲν μιαίνουσιν', 'sarka men miainousin', 'defile the flesh'),
 '"and they disregard lordship"': ('κυριότητα δὲ ἀθετοῦσιν', 'kyriotēta de athetousin', 'reject lordship'),
 '"and they speak evil of glorious [ones]"': ('δόξας δὲ βλασφημοῦσιν', 'doxas de blasphēmousin', 'and slander glorious ones'),
 '"yet Michael, the chief messenger"': ('ὁ δὲ Μιχαὴλ ὁ ἀρχάγγελος', 'ho de Michaēl ho archangelos', 'but Michael the archangel'),
 '"when disputing with the Devil, reasoning about the body of Moses"': ('ὅτε τῷ διαβόλῳ διακρινόμενος διελέγετο περὶ τοῦ Μωϋσέως σώματος', 'hote tō diabolō diakrinomenos dielegeto peri tou Mōuseōs sōmatos', 'when, contending with the devil, he argued about the body of Moses'),
 '"did not dare to bring against [him] a judgment of slander"': ('οὐκ ἐτόλμησεν κρίσιν ἐπενεγκεῖν βλασφημίας', 'ouk etolmēsen krisin epenenkein blasphēmias', 'did not dare to bring a slanderous judgment'),
 '"but said, \'The LORD rebuke you!\'"': ('ἀλλὰ εἶπεν· Ἐπιτιμήσαι σοι κύριος', 'alla eipen: Epitimēsai soi kyrios', 'but said: may the Lord rebuke you'),
 '"But these, indeed, whatever [things] they have not known, they speak evil of"': ('οὗτοι δὲ ὅσα μὲν οὐκ οἴδασιν βλασφημοῦσιν', 'houtoi de hosa men ouk oidasin blasphēmousin', 'but these people slander whatever they do not understand'),
 '"and whatever [they know], like the irrational beasts, they understand naturally—in these they are corrupted"': ('ὅσα δὲ φυσικῶς ὡς τὰ ἄλογα ζῷα ἐπίστανται, ἐν τούτοις φθείρονται', 'hosa de physikōs hōs ta aloga zōa epistantai, en toutois phtheirontai', 'and what they know by instinct, like irrational animals, is what destroys them'),
 # ch05
 '"woe to them!"': ('οὐαὶ αὐτοῖς', 'ouai autois', 'woe to them'),
 '"Because they went on in the way of Cain"': ('ὅτι τῇ ὁδῷ τοῦ Κάϊν ἐπορεύθησαν', 'hoti tē hodō tou Kain eporeuthēsan', 'for they went the way of Cain'),
 '"and they rushed to the deceit of Balaam for reward"': ('καὶ τῇ πλάνῃ τοῦ Βαλαὰμ μισθοῦ ἐξεχύθησαν', 'kai tē planē tou Balaam misthou exechythēsan', 'and for pay they poured themselves into the error of Balaam'),
 '"and in the controversy of Korah they perished"': ('καὶ τῇ ἀντιλογίᾳ τοῦ Κόρε ἀπώλοντο', 'kai tē antilogia tou Kore apōlonto', 'and perished in the rebellion of Korah'),
 # ch06
 '"These are"': ('οὗτοί εἰσιν', 'houtoi eisin', 'these are'),
 '"stains at your love-feasts"': ('οἱ ἐν ταῖς ἀγάπαις ὑμῶν σπιλάδες', 'hoi en tais agapais hymōn spilades', 'the hidden reefs (or stains) at your love feasts'),
 '"feasting together with you without fear"': ('συνευωχούμενοι ἀφόβως', 'syneuōchoumenoi aphobōs', 'feasting with you without reverence'),
 '"shepherding themselves"': ('ἑαυτοὺς ποιμαίνοντες', 'heautous poimainontes', 'shepherding themselves'),
 '"waterless clouds, being carried away by winds"': ('νεφέλαι ἄνυδροι ὑπὸ ἀνέμων παραφερόμεναι', 'nephelai anydroi hypo anemōn parapheromenai', 'waterless clouds carried along by winds'),
 '"autumnal trees without fruit"': ('δένδρα φθινοπωρινὰ ἄκαρπα', 'dendra phthinopōrina akarpa', 'fruitless trees in late autumn'),
 '"having died twice, having been uprooted"': ('δὶς ἀποθανόντα ἐκριζωθέντα', 'dis apothanonta ekrizōthenta', 'twice dead, uprooted'),
 # ch07
 '"wild waves of a sea"': ('κύματα ἄγρια θαλάσσης', 'kymata agria thalassēs', 'wild waves of the sea'),
 '"foaming up their own shameful [deeds]"': ('ἐπαφρίζοντα τὰς ἑαυτῶν αἰσχύνας', 'epaphrizonta tas heautōn aischynas', 'foaming up their own shameful deeds'),
 '"stars going astray"': ('ἀστέρες πλανῆται', 'asteres planētai', 'wandering stars'),
 '"for whom the gloom of the darkness throughout the age has been kept"': ('οἷς ὁ ζόφος τοῦ σκότους εἰς αἰῶνα τετήρηται', 'hois ho zophos tou skotous eis aiōna tetērētai', 'for whom the gloom of darkness has been kept forever'),
 # ch08
 '"And Enoch, the seventh from Adam"': ('ἕβδομος ἀπὸ Ἀδὰμ Ἑνώχ', 'hebdomos apo Adam Henōch', 'Enoch, the seventh from Adam'),
 '"also prophesied to these"': ('Προεφήτευσεν δὲ καὶ τούτοις', 'Proephēteusen de kai toutois', 'prophesied also about these'),
 '"saying, \'Behold, the LORD has come\'"': ('λέγων· Ἰδοὺ ἦλθεν κύριος', 'legōn: Idou ēlthen kyrios', 'saying: see, the Lord has come'),
 '"with myriads of His holy ones"': ('ἐν ἁγίαις μυριάσιν αὐτοῦ', 'en hagiais myriasin autou', 'with his holy myriads'),
 '"to do judgment against all"': ('ποιῆσαι κρίσιν κατὰ πάντων', 'poiēsai krisin kata pantōn', 'to execute judgment on all'),
 '"and to convict all their impious ones"': ('καὶ ἐλέγξαι πάντας τοὺς ἀσεβεῖς', 'kai elenxai pantas tous asebeis', 'and to convict all the impious'),
 '"concerning all their works of impiety that they did impiously"': ('περὶ πάντων τῶν ἔργων ἀσεβείας αὐτῶν ὧν ἠσέβησαν', 'peri pantōn tōn ergōn asebeias autōn hōn ēsebēsan', 'for all the impious deeds they committed impiously'),
 '"and concerning all the harsh [words] that impious sinners spoke against Him"': ('καὶ περὶ πάντων τῶν σκληρῶν ὧν ἐλάλησαν κατ’ αὐτοῦ ἁμαρτωλοὶ ἀσεβεῖς', 'kai peri pantōn tōn sklērōn hōn elalēsan kat’ autou hamartōloi asebeis', 'and for all the harsh things impious sinners have spoken against him'),
 # ch09
 '"These are discontented grumblers"': ('οὗτοί εἰσιν γογγυσταί, μεμψίμοιροι', 'houtoi eisin gongystai, mempsimoiroi', 'these are grumblers, complaining of their lot'),
 '"walking according to their own lusts"': ('κατὰ τὰς ἐπιθυμίας αὐτῶν πορευόμενοι', 'kata tas epithymias autōn poreuomenoi', 'living by their own desires'),
 '"and their mouth speaks swollen words"': ('καὶ τὸ στόμα αὐτῶν λαλεῖ ὑπέρογκα', 'kai to stoma autōn lalei hyperonka', 'and their mouth speaks inflated words'),
 '"giving admiration to persons"': ('θαυμάζοντες πρόσωπα', 'thaumazontes prosōpa', 'flattering people (literally, admiring faces)'),
 '"for the sake of profit"': ('ὠφελείας χάριν', 'ōpheleias charin', 'for the sake of advantage'),
 # ch10
 '"but you, beloved"': ('Ὑμεῖς δέ, ἀγαπητοί', 'Hymeis de, agapētoi', 'but you, beloved'),
 '"remember"': ('μνήσθητε', 'mnēsthēte', 'remember'),
 '"the sayings spoken before by the apostles of our Lord Jesus Christ"': ('τῶν ῥημάτων τῶν προειρημένων ὑπὸ τῶν ἀποστόλων τοῦ κυρίου ἡμῶν Ἰησοῦ Χριστοῦ', 'tōn rhēmatōn tōn proeirēmenōn hypo tōn apostolōn tou kyriou hēmōn Iēsou Christou', 'the words spoken beforehand by the apostles of our Lord Jesus Christ'),
 '"that they said to you"': ('ὅτι ἔλεγον ὑμῖν', 'hoti elegon hymin', 'for they kept telling you'),
 '"that in the last time there will be scoffers"': ('Ἐπ’ ἐσχάτου χρόνου ἔσονται ἐμπαῖκται', 'Ep’ eschatou chronou esontai empaiktai', 'in the last time there will be scoffers'),
 '"following after their own lusts of impieties"': ('κατὰ τὰς ἑαυτῶν ἐπιθυμίας πορευόμενοι τῶν ἀσεβειῶν', 'kata tas heautōn epithymias poreuomenoi tōn asebeiōn', 'living by their own impious desires'),
 '"these are those causing divisions"': ('οὗτοί εἰσιν οἱ ἀποδιορίζοντες', 'houtoi eisin hoi apodiorizontes', 'these are the ones who cause divisions'),
 '"natural men"': ('ψυχικοί', 'psychikoi', 'unspiritual, merely natural people'),
 '"not having the Spirit"': ('πνεῦμα μὴ ἔχοντες', 'pneuma mē echontes', 'not having the Spirit'),
 # ch11
 '"But you, beloved"': ('ὑμεῖς δέ, ἀγαπητοί', 'hymeis de, agapētoi', 'but you, beloved'),
 '"building yourselves up on your most holy faith"': ('ἐποικοδομοῦντες ἑαυτοὺς τῇ ἁγιωτάτῃ ὑμῶν πίστει', 'epoikodomountes heautous tē hagiōtatē hymōn pistei', 'building yourselves up on your most holy faith'),
 '"praying in the Holy Spirit"': ('ἐν πνεύματι ἁγίῳ προσευχόμενοι', 'en pneumati hagiō proseuchomenoi', 'praying in the Holy Spirit'),
 '"keep yourselves in the love of God"': ('ἑαυτοὺς ἐν ἀγάπῃ θεοῦ τηρήσατε', 'heautous en agapē theou tērēsate', 'keep yourselves in the love of God'),
 '"waiting for the mercy of our Lord Jesus Christ"': ('προσδεχόμενοι τὸ ἔλεος τοῦ κυρίου ἡμῶν Ἰησοῦ Χριστοῦ', 'prosdechomenoi to eleos tou kyriou hēmōn Iēsou Christou', 'waiting for the mercy of our Lord Jesus Christ'),
 '"[resulting] in continuous life"': ('εἰς ζωὴν αἰώνιον', 'eis zōēn aiōnion', 'leading to eternal life'),
 # ch12
 '"and, indeed, show mercy"': ('καὶ οὓς μὲν ἐλεᾶτε', 'kai hous men eleate', 'and have mercy on some'),
 '"to those who are doubting"': ('διακρινομένους', 'diakrinomenous', 'who are doubting'),
 '"and rescue others by snatching [them] out of fire"': ('οὓς δὲ σῴζετε ἐκ πυρὸς ἁρπάζοντες', 'hous de sōzete ek pyros harpazontes', 'save others, snatching them out of the fire'),
 '"but show mercy to others in fear"': ('οὓς δὲ ἐλεᾶτε ἐν φόβῳ', 'hous de eleate en phobō', 'and on others have mercy with fear'),
 '"hating even the coat having been stained from the flesh"': ('μισοῦντες καὶ τὸν ἀπὸ τῆς σαρκὸς ἐσπιλωμένον χιτῶνα', 'misountes kai ton apo tēs sarkos espilōmenon chitōna', 'hating even the tunic stained by the flesh'),
 # ch13
 '"And to Him who is able"': ('Τῷ δὲ δυναμένῳ', 'Tō de dynamenō', 'now to the one who is able'),
 '"to guard you without stumbling"': ('φυλάξαι ὑμᾶς ἀπταίστους', 'phylaxai hymas aptaistous', 'to guard you from stumbling'),
 '"and to set [you] in the presence of His glory unblemished, in gladness"': ('καὶ στῆσαι κατενώπιον τῆς δόξης αὐτοῦ ἀμώμους ἐν ἀγαλλιάσει', 'kai stēsai katenōpion tēs doxēs autou amōmous en agalliasei', 'and to make you stand before his glory without blemish, with great joy'),
 '"to the only wise God our Savior"': ('μόνῳ θεῷ σωτῆρι ἡμῶν', 'monō theō sōtēri hēmōn', 'to the only God our Savior'),
 "‘through Jesus Christ our Lord’ (critical text)": ('διὰ Ἰησοῦ Χριστοῦ τοῦ κυρίου ἡμῶν', 'dia Iēsou Christou tou kyriou hēmōn', 'through Jesus Christ our Lord'),
 '"[is] glory and greatness, power and authority"': ('δόξα μεγαλωσύνη κράτος καὶ ἐξουσία', 'doxa megalōsynē kratos kai exousia', 'glory, majesty, power, and authority'),
 '‘before all time, and now, and forever’ (critical text) / "both now and forever" (LSV)': ('πρὸ παντὸς τοῦ αἰῶνος καὶ νῦν καὶ εἰς πάντας τοὺς αἰῶνας', 'pro pantos tou aiōnos kai nyn kai eis pantas tous aiōnas', 'before all time, and now, and to all the ages'),
 '"Amen."': ('ἀμήν', 'amēn', 'amen'),
}

def main():
    used = set()
    for path in sorted(glob.glob(os.path.join(ROOT, 'chapters', '[01][0-9]-jude-*.md'))):
        lines = open(path, encoding='utf-8').read().split('\n')
        n = 0
        for i, line in enumerate(lines):
            if not line.startswith('### '):
                continue
            key = line[4:].strip()
            if key in MAP:
                g, tr, gl = MAP[key]
                lines[i] = f'### {g} (*{tr}*) — ‘{gl}’'
                used.add(key); n += 1
        open(path, 'w', encoding='utf-8').write('\n'.join(lines))
        print(f'{os.path.basename(path)}: {n} headings converted')
    missing = [k for k in MAP if k not in used]
    if missing:
        print('Not found (already converted?):', *missing, sep='\n  ')

if __name__ == '__main__':
    main()
