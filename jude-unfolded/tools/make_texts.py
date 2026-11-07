#!/usr/bin/env python3
"""Generate the source-text sections of each chapter from the cached open texts.

Section A ("The Text") of every commentary chapter is rebuilt from:
  * the SBL Greek New Testament (CC BY 4.0), printed first;
  * a table of readings in ten early or important Greek manuscripts, taken from
    the INTF New Testament Virtual Manuscript Room transcriptions (CC BY 4.0).
    Every manuscript claimed for a reading is checked against the cached
    transcription; the script stops if a claim is not supported;
  * the verses in eighteen free English translations, in order of first
    publication, each quoted exactly from its eBible.org edition.

Section L ("Texts Highlighted in This Chapter") prints every passage of
Scripture, the Apocrypha, and 1 Enoch that the chapter cites or alludes to by
reference: Hebrew/Aramaic (WLC) or Greek (SBLGNT; LXX for the Apocrypha) first,
then the BSB and the WEB (Brenton for the Apocrypha; Charles for 1 Enoch).
A long passage already printed in full earlier in the book is linked rather than
printed again.

Generated regions sit between <!-- BEGIN GENERATED … --> and <!-- END GENERATED … -->
markers and are replaced on every run. Usage: python3 -I tools/make_texts.py
"""
import os, re, sys, glob, json, unicodedata, functools, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sources import TRANSLATIONS, english, greek_nt, hebrew, lxx, enoch, is_nt, WLC, _usfm, ABBR, C as CACHE
from audit import BOOKS

CH = os.path.join(ROOT, 'chapters')
AP = os.path.join(ROOT, 'appendices')

# ----------------------------------------------------------------------------
# Book names
NAME = {'GEN':'Genesis','EXO':'Exodus','LEV':'Leviticus','NUM':'Numbers','DEU':'Deuteronomy','JOS':'Joshua','JDG':'Judges',
        'RUT':'Ruth','1SA':'1 Samuel','2SA':'2 Samuel','1KI':'1 Kings','2KI':'2 Kings','1CH':'1 Chronicles','2CH':'2 Chronicles',
        'EZR':'Ezra','NEH':'Nehemiah','EST':'Esther','JOB':'Job','PSA':'Psalm','PRO':'Proverbs','ECC':'Ecclesiastes',
        'SNG':'Song of Songs','ISA':'Isaiah','JER':'Jeremiah','LAM':'Lamentations','EZK':'Ezekiel','DAN':'Daniel','HOS':'Hosea',
        'JOL':'Joel','AMO':'Amos','OBA':'Obadiah','JON':'Jonah','MIC':'Micah','NAM':'Nahum','HAB':'Habakkuk','ZEP':'Zephaniah',
        'HAG':'Haggai','ZEC':'Zechariah','MAL':'Malachi','MAT':'Matthew','MRK':'Mark','LUK':'Luke','JHN':'John','ACT':'Acts',
        'ROM':'Romans','1CO':'1 Corinthians','2CO':'2 Corinthians','GAL':'Galatians','EPH':'Ephesians','PHP':'Philippians',
        'COL':'Colossians','1TH':'1 Thessalonians','2TH':'2 Thessalonians','1TI':'1 Timothy','2TI':'2 Timothy','TIT':'Titus',
        'PHM':'Philemon','HEB':'Hebrews','JAS':'James','1PE':'1 Peter','2PE':'2 Peter','1JN':'1 John','2JN':'2 John',
        '3JN':'3 John','JUD':'Jude','REV':'Revelation','SIR':'Sirach','WIS':'Wisdom of Solomon','3MA':'3 Maccabees',
        '1EN':'1 Enoch'}
CANON = ['GEN','EXO','LEV','NUM','DEU','JOS','JDG','RUT','1SA','2SA','1KI','2KI','1CH','2CH','EZR','NEH','EST','JOB','PSA',
         'PRO','ECC','SNG','ISA','JER','LAM','EZK','DAN','HOS','JOL','AMO','OBA','JON','MIC','NAM','HAB','ZEP','HAG','ZEC','MAL',
         'SIR','WIS','3MA',
         'MAT','MRK','LUK','JHN','ACT','ROM','1CO','2CO','GAL','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB',
         'JAS','1PE','2PE','1JN','2JN','3JN','JUD','REV','1EN']
APOC = {'Sir': 'SIR', 'Wis': 'WIS', '3 Macc': '3MA'}
ONE_CHAPTER = {'OBA', 'PHM', '2JN', '3JN', 'JUD'}
ALLBOOKS = dict(BOOKS); ALLBOOKS.update(APOC); ALLBOOKS['1 Enoch'] = '1EN'
BOOK_RE = '|'.join(sorted((re.escape(k) for k in ALLBOOKS), key=len, reverse=True))
REF = re.compile(r'(?<![\w])(' + BOOK_RE + r')\.?\s+(\d+(?::\d+)?(?:[–-]\d+(?::\d+)?)?(?:\s*[,;]\s*\d+(?::\d+)?(?:[–-]\d+(?::\d+)?)?(?!\s+[A-Z]))*)')

GEN_RE = re.compile(r'<!-- BEGIN GENERATED (\w+) -->.*?<!-- END GENERATED \1 -->\n?', re.S)

def strip_generated(text):
    return GEN_RE.sub('', text)

# ----------------------------------------------------------------------------
# Section A: manuscripts
SIGLA = {'P72': 'P72', 'P78': 'P78', '01': 'ℵ', '02': 'A', '03': 'B', '04': 'C', '044': 'Ψ', '018': 'K', '020': 'L', '1739': '1739'}
MS_ORDER = ['P72', 'P78', '01', '02', '03', '04', '044', '018', '020', '1739']
LEGEND = ('P72 and P78 (papyri, 3rd/4th c.); ℵ = 01 Sinaiticus (4th c.); A = 02 Alexandrinus (5th c.); '
          'B = 03 Vaticanus (4th c.); C = 04 Ephraemi Rescriptus (5th c.); Ψ = 044 (9th/10th c.); K = 018 (9th c.); '
          'L = 020 (9th c.); 1739 (10th c.)')

# Each unit: list of readings (Greek, English, [manuscripts], check). A manuscript
# may carry "*" (first hand) or "c" (a later corrector). A check is a string that
# must occur in the normalized transcription of every manuscript listed, or a
# dict {ms: string} of per-manuscript checks, or a tuple (must, must_not).
UNITS = {
 1: [[('ἠγαπημένοις', 'loved', ['P72','01','02','03','044','1739'], 'ηγαπημενοις'),
      ('ἡγιασμένοις', 'sanctified', ['018','020'], 'ηγιασμενοις')],
     [('τοῖς ἐν θεῷ πατρί', 'to those … in God the Father', ['P72','01','02','03','044','018','020'], 'τοισενθω'),
      ('τοῖς ἔθνεσιν ἐν θεῷ πατρί', 'to the Gentiles … in God the Father', ['1739'], 'τοισεθνεσινενθω')]],
 3: [[('κοινῆς ἡμῶν σωτηρίας', 'our common salvation', ['P72','02','03','04','1739'], ('κοινησημωνσ', 'καιζωησ')),
      ('κοινῆς ἡμῶν σωτηρίας καὶ ζωῆς', 'our common salvation and life', ['01','044'], 'κοινησημωνσ'),
      ('κοινῆς σωτηρίας', 'common salvation', ['018','020'], 'κοινησσριασ')]],
 4: [[('δεσπότην (καὶ) κύριον', 'Master and Lord', ['P72','P78','01','02','03','04','1739'], ('δεσποτην', 'δεσποτηνθν')),
      ('δεσπότην θεὸν καὶ κύριον', 'Master, God, and Lord', ['044','018','020'], 'δεσποτηνθν')]],
 5: [[('Ἰησοῦς', 'Jesus', ['02','03','1739'], 'οτιισ'),
      ('(ὁ) κύριος', 'the Lord', ['01','04*','044','018','020'], {'01':'οτικσ','04':'οτιοκσ','044':'οτικσ','018':'οτιοκσ','020':'οτιοκσ'}),
      ('ὁ θεός', 'God', ['04c'], 'οτιοθσ'),
      ('θεὸς Χριστός', 'God Christ', ['P72'], 'οτιθσχρσ')],
     [('εἰδότας (ὑμᾶς) ἅπαξ πάντα', 'though you once knew all things', ['P72','02','03'], ('απαξπαντα', 'απαξλαον')),
      ('… πάντα, ὅτι [subject] ἅπαξ λαόν …', 'knowing all things, that [the Lord/Jesus] once saved a people', ['01','04','044','1739'], 'απαξλαον'),
      ('εἰδότας ὑμᾶς τοῦτο ἅπαξ / ἅπαξ τοῦτο', 'though you once knew this', ['018','020'], 'τουτο')],
     [('βούλομαι ἀδελφοί', 'I want, brothers and sisters, (to remind you)', ['P78'], 'βουλομεαδελφο')]],
 7: [[('τὸν ὅμοιον τρόπον τούτοις', 'in the same way as these', ['P72','01','02','03','04','1739'], 'τροποντουτοισ'),
      ('τὸν ὅμοιον τρόπον αὐτοῖς', 'in the same way as they', ['044'], 'τροποναυτοισ'),
      ('τὸν ὅμοιον τούτοις τρόπον', '(word order only)', ['018','020'], 'ομοιοντουτοιστροπον')],
     [('δίκην ὑπέχουσαι', 'undergoing the penalty', ['P72','03','04','044','018','020','1739'], 'δικηνυπεχουσαι'),
      ('δίκην ἐπέχουσαι', '(spelling variant of the same)', ['P78'], 'δικηνεπεχουσαι'),
      ('δίκην ὑπερέχουσαι', '‘excelling’ (probably a copying slip)', ['02'], 'δικηνυπερεχουσαι'),
      ('δίκην οὐκ ἔχουσιν', '‘they do not have’ (corrected to ὑπέχουσιν)', ['01*'], 'δικηνουκεχουσιν')]],
 8: [[('κυριότητα', 'lordship', ['P72','P78','02','03','04','018','020','1739'], {'P78':'οτηταδε', '*':'κυριοτηταδε'}),
      ('κυριότητας', 'lordships', ['01','044'], 'κυριοτητασδε')],
     [('δόξας', 'glorious ones', ['P72','01','02','03','04','044','018','020','1739'], 'δοξασδε'),
      ('δόξαν', 'glory', ['P78'], 'δοξανδε')]],
 9: [[('κύριος', 'the Lord', ['P72','02','03','04','044','018','020'], 'σοικσ'),
      ('ὁ θεός', 'God', ['01*','1739'], 'σοιοθσ')]],
 12: [[('ἀγάπαις', 'love feasts', ['P72','01','03','044','018','020','1739'], 'ταισαγαπαισ'),
       ('ἀπάταις', 'deceptions', ['02','04'], 'ταισαπαταισ')],
      [('οὗτοί εἰσιν οἱ ἐν ταῖς …', 'these are the ones who … at your …', ['P72','02','03','04','044','020','1739'], 'οιενταισ'),
       ('οὗτοί εἰσιν ἐν ταῖς …', 'these are … at your … (without οἱ)', ['018'], 'εισινενταισ')],
      [('the words of v. 16 (γογγυσταί … πορευόμενοι) also written here', 'the description of v. 16 repeated in v. 12', ['01','04c'], 'γογγυσται')],
      [('συνευωχούμενοι ὑμῖν', 'feasting with you', ['04','1739'], 'συνευωχουμενοιυμιν')],
      [('ὑπὸ ἀνέμων', 'by winds', ['P72','02','03','04','044','018','020','1739'], 'υποανεμων'),
       ('παντὶ ἀνέμῳ', 'by every wind', ['01'], 'παντιανεμω')]],
 13: [[('εἰς αἰῶνα', 'forever', ['P72','01','02','03','04','020','1739'], {'P72':'εισεωνα', '*':'εισαιωνατετηρηται'}),
       ('εἰς αἰῶνας', 'forever (plural)', ['044'], 'εισαιωνασ'),
       ('εἰς τὸν αἰῶνα', 'forever', ['018'], 'ειστοναιωνα')]],
 14: [[('ἐν ἁγίαις μυριάσιν αὐτοῦ', 'with his holy myriads', ['02','03','018','020'], 'αγιαισμυριασιναυτου'),
       ('ἐν μυριάσιν ἁγίαις αὐτοῦ', '(word order only)', ['04','1739'], 'μυριασιναγιαισαυτου'),
       ('ἐν ἁγίων ἀγγέλων μυριάσιν', 'with myriads of holy angels', ['P72'], 'αγιωναγγελωνμυριασιν'),
       ('ἐν μυριάσιν ἁγίων ἀγγέλων', 'with myriads of holy angels', ['01'], 'μυριασιναγιωναγγελων'),
       ('ἐν ἁγίαις μυριάσιν ἀγγέλων', 'with holy myriads of angels', ['044'], 'αγιαισμυριασιναγγελων')]],
 15: [[('πάντας τοὺς ἀσεβεῖς', 'all the impious', ['02','03','04','044'], 'παντασ τουσασεβεισπερι'),
       ('πάντας τοὺς ἀσεβεῖς αὐτῶν', 'all their impious ones', ['018','020'], 'τουσασεβεισαυτων'),
       ('πάντας ἀσεβεῖς', 'all impious people', ['1739'], 'ελεγξαιπαντασασεβεισ'),
       ('πᾶσαν ψυχήν', 'every soul', ['P72','01'], 'πασανψυχην')],
      [('τῶν ἔργων ἀσεβείας αὐτῶν', 'their impious deeds', ['02','03','018','020'], 'εργωνασεβειασαυτων'),
       ('τῶν ἔργων αὐτῶν', 'their deeds', ['04'], 'εργωναυτων'),
       ('τῶν ἔργων', 'the deeds', ['01','1739'], 'εργωνωνησεβησαν'),
       ('the whole clause “concerning all their impious deeds … and” is absent', '', ['P72'], ('πασανψυχην', 'εργων'))],
      [('τῶν σκληρῶν', 'the harsh things', ['P72','02','03','044','018','020'], 'σκληρωνων'),
       ('τῶν σκληρῶν λόγων', 'the harsh words', ['01','04','1739'], 'σκληρωνλογων')]],
 16: [[('κατὰ τὰς ἐπιθυμίας αὐτῶν', 'by their desires', ['01','02','03','044','018'], 'επιθυμιασαυτων'),
       ('κατὰ τὰς ἐπιθυμίας ἑαυτῶν', 'by their own desires', ['P72c','04','020','1739'], {'P72':'επιθυμιασεαυτω', '*':'επιθυμιασεαυτων'})]],
 18: [[('ἔσονται', 'there will be', ['P72','01*','03','04*','018','020'], 'εσονταιεμπ'),
       ('ἐλεύσονται', 'there will come', ['01c','02','04c','1739'], 'ελευσονται'),
       ('ἀναστήσονται', 'there will arise', ['044'], 'αναστησονται')],
      [('ἐπ’ ἐσχάτου χρόνου', 'in the last time', ['P72','03','04','044'], 'επεσχατουχρονου'),
       ('ἐπ’ ἐσχάτου τοῦ χρόνου', 'at the last of the time', ['01','02'], 'επεσχατουτουχρονου'),
       ('ἐπ’ ἐσχάτου τῶν χρόνων', 'at the last of the times', ['1739'], 'εσχατουτωνχρονων'),
       ('ἐν ἐσχάτῳ χρόνῳ', 'in the last time', ['018','020'], 'ενεσχατωχρονω')]],
 19: [[('οἱ ἀποδιορίζοντες', 'those who cause divisions', ['P72','01','02','03','044','018','020','1739*'], 'ψυχικοι'),
       ('οἱ ἀποδιορίζοντες ἑαυτούς', 'those who separate themselves', ['04','1739c'], 'ζοντεσεαυτουσ')]],
 20: [[('ἐποικοδομοῦντες ἑαυτοὺς τῇ ἁγιωτάτῃ ὑμῶν πίστει', 'building yourselves up on your most holy faith', ['01','02','03','044'], ('εποικοδομουντεσεαυτουστηαγι', 'ημωνπιστει')),
       ('ἐποικοδομοῦντες ἑαυτοὺς τῇ ἁγιωτάτῃ ἡμῶν πίστει', '… on our most holy faith', ['04','1739'], 'ημωνπιστει'),
       ('τῇ ἁγιωτάτῃ ὑμῶν πίστει ἐποικοδομοῦντες ἑαυτούς', '(word order only)', ['018','020'], 'πιστειεποικοδομουντεσ'),
       ('τῇ ἑαυτῶν ἁγιότητι πίστει ἀνοικοδομεῖσθε', 'a different wording: ‘be built up by your own holiness, by faith’', ['P72'], 'ανυκοδομεισθαι')]],
 21: [[('τηρήσατε', 'keep (a command)', ['01','02','018','020','1739'], 'τηρησατε'),
       ('τηρήσωμεν', 'let us keep', ['P72','03','04*','044'], 'τηρησωμεν'),
       ('τηρήσητε', '(that) you may keep', ['04c'], 'τηρησητε')]],
 23: [[('καὶ οὓς μὲν ἐλεᾶτε διακρινομένους, οὓς δὲ σῴζετε ἐκ πυρὸς ἁρπάζοντες, οὓς δὲ ἐλεᾶτε ἐν φόβῳ',
        'three clauses: have mercy on some who doubt; save others, snatching them from fire; have mercy on others with fear',
        ['01','044'], 'ουσμενελεατεδιακρινομενουσ|ουσδεσωζετε|ουσδεελεατεενφοβω'),
       ('καὶ οὓς μὲν ἐλέγχετε διακρινομένους, οὓς δὲ σῴζετε …, οὓς δὲ ἐλεᾶτε ἐν φόβῳ',
        'three clauses, the first ‘refute some who dispute’', ['02','1739'], 'ουσμενελεγχ|ουσδεσωζετε|ουσδεελε'),
       ('καὶ οὓς μὲν ἐλεᾶτε διακρινομένους σῴζετε ἐκ πυρὸς ἁρπάζοντες, οὓς δὲ ἐλεᾶτε ἐν φόβῳ',
        'two clauses: have mercy on some who doubt, saving them by snatching them from fire; have mercy on others with fear',
        ['03'], 'ουσμενελεατε|νουσσωζετε|ουσδεελεατεενφοβω'),
       ('καὶ οὓς μὲν ἐλέγχετε διακρινομένους, οὓς δὲ σῴζετε ἐκ πυρὸς ἁρπάζοντες ἐν φόβῳ',
        'two clauses: refute some who dispute; save others with fear, snatching them from fire (a corrector changed ἐλέγχετε to ἐλεᾶτε)',
        ['04'], 'ελεγχετε|αρπαζοντεσενφοβω'),
       ('καὶ οὓς μὲν ἐλεεῖτε διακρινόμενοι, οὓς δὲ ἐν φόβῳ σῴζετε ἐκ πυρὸς ἁρπάζοντες',
        'two clauses: have mercy on some, making a distinction; save others with fear, snatching them from fire',
        ['018','020'], 'ουσμενελεειτε|ουσδεενφοβωσωζετε'),
       ('οὓς μὲν ἐκ πυρὸς ἁρπάσατε, διακρινομένους δὲ ἐλεεῖτε ἐν φόβῳ',
        'two clauses: snatch some from fire; on those who dispute have mercy with fear',
        ['P72'], 'ουσμενεκπυροσαρπασατε|διακρινομενουσδεελεειτεενφοβω')]],
 24: [[('φυλάξαι ὑμᾶς', 'to guard you', ['01','03','04','044','020','1739'], 'υμασ'),
       ('φυλάξαι ἡμᾶς', 'to guard us', ['02'], 'φυλαξαιημασ'),
       ('φυλάξαι αὐτούς', 'to guard them', ['018'], 'λαξαιαυτουσ')],
      [('ἀπταίστους καὶ στῆσαι', 'from stumbling, and to make (you) stand', ['01','02','03','044','018','020'], 'στουσκαιστησαι'),
       ('ἀπταίστους καὶ ἀσπίλους … στῆσαι', 'from stumbling and spotless, … to make (you) stand', ['04','1739'], 'απταιστουσκαιασπιλουσ'),
       ('στηρίξαι ἀσπίλους ἀμώμους ἁγνευομένους ἀπέναντι τῆς δόξης', 'to establish (you) spotless, blameless, purified, before his glory', ['P72'], 'στηριξαιασπειλουσ')],
      [('ἀμώμους', 'without blemish', ['P72','01','03','04','044','018','020','1739'], 'αμωμουσ'),
       ('ἀμέμπτους', 'blameless', ['02'], 'αμεμπτουσ')]],
 25: [[('μόνῳ θεῷ σωτῆρι ἡμῶν', 'to the only God our Savior', ['01','02','03','04','044','1739'], 'μονωθωσ'),
       ('μόνῳ σοφῷ θεῷ σωτῆρι ἡμῶν', 'to the only wise God our Savior', ['018','020'], 'μονωσοφωθω'),
       ('μόνῳ θεῷ ἡμῶν', 'to our only God', ['P72'], 'μονωθωημων')],
      [('διὰ Ἰησοῦ Χριστοῦ τοῦ κυρίου ἡμῶν', 'through Jesus Christ our Lord', ['P72','01','02','03','04','044','020','1739'], 'διαι'),
       ('(absent)', '', ['018'], ('μονω', 'διαι'))],
      [('πρὸ παντὸς τοῦ αἰῶνος', 'before all time', ['01','02','03','04','044','020'], 'προπαντοστουαιωνοσ'),
       ('πρὸ παντὸς αἰῶνος', 'before every age', ['1739'], 'προπαντοσαιωνοσ'),
       ('(absent)', '', ['P72','018'], ('νυν', 'προπαντ'))]],
}
NO_UNITS = {2: 'spelling only', 6: 'A reads δέ for τε; Ψ reads κατοικητήριον for οἰκητήριον',
            10: 'Ψ reads διαφθείρονται for φθείρονται', 11: 'P72 spells Balaam’s name Βαλαάκ',
            17: 'A and 1739 place προειρημένων before ῥημάτων; 1739 reads μνημονεύετε, ‘remember’', 22: None}

def nz(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower().replace('ς', 'σ')
    return ''.join(c for c in s if 'α' <= c <= 'ω')

@functools.lru_cache(maxsize=None)
def ms_data():
    return json.load(open(os.path.join(CACHE, 'ntvmr', 'jude_ms.json'), encoding='utf-8'))

def ms_text(ms, verses):
    d = ms_data()[ms]
    return nz(' '.join(re.sub(r'^Jude 1:\d+', '', d.get(str(v), '')) for v in verses))

def extant(ms, v):
    t = ms_data()[ms].get(str(v), '')
    body = nz(re.sub(r'^Jude 1:\d+', '', t))
    if not body: return 'no'
    return 'partly' if '[---]' in t else 'yes'

def check_unit(v, reading):
    g, e, mss, chk = reading
    verses = [22, 23] if v == 23 else [v]
    for m in mss:
        base = m.rstrip('*c')
        hay = ms_text(base, verses)
        must, must_not = (chk if isinstance(chk, tuple) else (chk, None))
        if isinstance(must, dict):
            must = must.get(base, must.get('*'))
        for piece in must.split('|'):
            if nz(piece) not in hay:
                raise SystemExit(f'Manuscript check failed: Jude {v}, {m} for “{g}”: “{piece}” not in transcription')
        if must_not and nz(must_not) in hay:
            raise SystemExit(f'Manuscript check failed: Jude {v}, {m} for “{g}”: “{must_not}” unexpectedly present')

def sig(m):
    base = m.rstrip('*c'); suf = m[len(base):]
    return SIGLA[base] + ({'*': '*', 'c': '^corr^'}.get(suf, ''))

def ms_table(v1, v2):
    rows = []
    for v in range(v1, v2 + 1):
        for unit in UNITS.get(v, []):
            for r in unit:
                check_unit(v, r)
                g, e, mss, _ = r
                order = sorted(mss, key=lambda m: MS_ORDER.index(m.rstrip('*c')))
                vv = '22–23' if v == 23 else str(v)
                desc = (not e) or e.startswith(('(', '‘', 'a different', 'three clauses', 'two clauses', 'the description'))
                rows.append(f'| {vv} | {g} | {e if desc else "‘" + e + "’"} | {" ".join(sig(m) for m in order)} |')
    out = []
    if rows:
        out += ['| v. | Reading | Meaning | Manuscripts |', '|---|---|---|---|'] + rows + ['']
    notes = []
    for v in range(v1, v2 + 1):
        bits = []
        if NO_UNITS.get(v):
            bits.append(f'no difference that affects translation ({NO_UNITS[v]})')
        missing = [SIGLA[m] for m in MS_ORDER if extant(m, v) == 'no']
        partly = [SIGLA[m] for m in MS_ORDER if extant(m, v) == 'partly']
        if missing: bits.append('not extant in ' + ', '.join(missing))
        if partly: bits.append('only partly extant in ' + ', '.join(partly))
        if bits: notes.append(f'v. {v}: ' + '; '.join(bits))
    if notes:
        out += ['Notes. ' + '. '.join(notes) + '.', '']
    return out

# ----------------------------------------------------------------------------
# Section A assembly
def chapter_verses(base):
    m = re.match(r'\d\d-jude-(\d\d)(?:-(\d\d))?\.md$', base)
    if not m: return None
    v1 = int(m.group(1)); v2 = int(m.group(2) or v1)
    return v1, v2

def esc(s):
    return s.replace('|', '\\|')

def section_a(v1, v2):
    rng = f'{v1}' if v1 == v2 else f'{v1}–{v2}'
    g = greek_nt(('JUD', 1, v1, v2))
    lines = ['<!-- BEGIN GENERATED textA -->', '',
             '### The Greek text', '',
             '> ' + ' '.join(f'**{v}** {t}' for v, t in g), '>',
             f'> — Jude {rng}, SBLGNT', '',
             '### What the earliest manuscripts read', '',
             'Where the manuscripts differ in a way that affects translation, the table gives each reading and the manuscripts that have it. '
             'Readings are taken from the transcriptions in the New Testament Virtual Manuscript Room of the Institute for New Testament '
             'Textual Research (INTF), Münster (CC BY 4.0), and every manuscript listed has been checked against those transcriptions. '
             'Differences of spelling are not listed. An asterisk marks a manuscript’s first hand, and ^corr^ a later corrector. '
             f'Manuscripts: {LEGEND}.', '']
    lines += ms_table(v1, v2)
    lines += ['### The verses in eighteen free English translations', '',
              'No translation is given priority. The translations are listed in order of first publication and quoted exactly from their '
              'eBible.org editions; all are in the public domain or under a free license (see the Copyright and Licensing page).', '']
    for v in range(v1, v2 + 1):
        lines += [f'#### Jude {v}', '', '| Translation | Text |', '|---|---|']
        for abbr, eid, name, year, lic in TRANSLATIONS:
            t = english(abbr, ('JUD', 1, v, v))
            txt = t[0][1] if t else '—'
            lines.append(f'| **{abbr}** {name} ({year}) | {esc(txt)} |')
        lines.append('')
    lines += ['<!-- END GENERATED textA -->', '']
    return '\n'.join(lines)

def replace_section_a(text, v1, v2):
    m = re.search(r'^## A\. The Text\s*\n(.*?)(?=^## B\.)', text, flags=re.M | re.S)
    if not m: raise SystemExit('section A not found')
    return text[:m.start(1)] + '\n' + section_a(v1, v2) + '\n' + text[m.end(1):]

# ----------------------------------------------------------------------------
# Section L: references
@functools.lru_cache(maxsize=None)
def nverses(code, ch):
    if code == '1EN':
        e = enoch_chapter(ch)
        return max(e) if e else 0
    eid = ABBR['BSB'][1] if code not in APOC.values() else 'eng-Brenton'
    b = _usfm(eid, code)
    vs = [int(re.match(r'\d+', v).group()) for (c, v) in b if c == ch and re.match(r'\d+', v)]
    return max(vs) if vs else 0

def enoch_chapter(ch):
    f = os.path.join(CACHE, 'enoch', f'ch{ch:02d}.txt')
    if not os.path.exists(f) or os.path.getsize(f) < 200:
        url = f'https://en.wikisource.org/w/index.php?title=The_Book_of_Enoch_(Charles)/Chapter_{ch:02d}&action=raw'
        subprocess.run(['curl', '-sSfL', '-A', 'jude-unfolded-research-script', '-o', f, url], check=False)
    from sources import _enoch
    _enoch.cache_clear()
    return dict(enoch(ch, 1, 200))

def parse_match(bk, nums):
    """Return list of (code, ch, verses) where verses is a sorted tuple or None (whole chapter),
    or ('RANGE', code, c1, c2) for very long chapter ranges."""
    code = ALLBOOKS[bk]
    out = []
    ch = None
    for sep, piece in re.findall(r'(^|[,;])\s*([^,;]+)', nums):
        piece = piece.strip().replace('-', '–')
        if not piece: continue
        if code in ONE_CHAPTER and ':' not in piece:
            a, _, b = piece.partition('–')
            out.append((code, 1, tuple(range(int(a), int(b or a) + 1)))); ch = 1
            continue
        m = re.match(r'^(\d+):(\d+)(?:–(?:(\d+):)?(\d+))?$', piece)
        if m:
            c, v = int(m.group(1)), int(m.group(2))
            if m.group(3):            # c:v–c2:v2
                c2, v2 = int(m.group(3)), int(m.group(4))
                out.append((code, c, tuple(range(v, (nverses(code, c) or v) + 1))))
                for cc in range(c + 1, c2):
                    out.append((code, cc, None))
                out.append((code, c2, tuple(range(1, v2 + 1))))
                ch = c2
            else:
                v2 = int(m.group(4) or v)
                out.append((code, c, tuple(range(v, v2 + 1)))); ch = c
            continue
        m = re.match(r'^(\d+)(?:–(\d+))?$', piece)
        if not m: continue
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        if ch is None or sep == ';':
            if b - a >= 5:
                out.append(('RANGE', code, a, b))
            else:
                for cc in range(a, b + 1):
                    out.append((code, cc, None))
            ch = None
        else:
            out.append((code, ch, tuple(range(a, b + 1))))
    return out

def collect(text):
    """Find references in text (outside generated regions). Returns list of (start, end, items)."""
    res = []
    for m in REF.finditer(text):
        items = parse_match(m.group(1), m.group(2))
        items = [i for i in items if i[0] != 'JUD' and not (i[0] == 'RANGE' and i[1] == 'JUD')]
        if items:
            res.append((m.start(), m.end(), items))
    return res

def merged(text):
    """Merge references into entries keyed by (code, ch) -> set of verses or None (whole)."""
    ent = {}
    ranges = {}
    for _, _, items in collect(strip_generated(text)):
        for it in items:
            if it[0] == 'RANGE':
                ranges[(it[1], it[2], it[3])] = True
                continue
            code, ch, vs = it
            if (code, ch) in ent and ent[(code, ch)] is None: continue
            if vs is None:
                ent[(code, ch)] = None
            else:
                ent.setdefault((code, ch), set()).update(vs)
    return ent, ranges

def runs(vs):
    vs = sorted(vs); out = []
    for v in vs:
        if out and v == out[-1][1] + 1: out[-1][1] = v
        else: out.append([v, v])
    return out

def label_runs(code, ch, vs):
    name = NAME[code]
    if vs is None:
        return f'{name} {ch}' if code not in ONE_CHAPTER else name
    r = ', '.join(f'{a}' if a == b else f'{a}–{b}' for a, b in runs(vs))
    return f'{name} {r}' if code in ONE_CHAPTER else f'{name} {ch}:{r}'

def slug(code, ch):
    return f'{code.lower()}-{ch}'

ARAMAIC = {('DAN', c) for c in range(3, 8)} | {('EZR', c) for c in range(5, 7)}
def is_aramaic(code, ch, v):
    if code == 'DAN': return (ch == 2 and v >= 4) or 3 <= ch <= 7
    if code == 'JER': return ch == 10 and v == 11
    return False

def fmt_verses(pairs):
    return ' '.join(f'**{v}** {t}' for v, t in pairs)

VERSIFICATION_CHECKED = set()
def entry_body(code, ch, vs):
    """Return markdown lines printing the passage."""
    n = nverses(code, ch)
    verses = list(range(1, n + 1)) if vs is None else sorted(v for v in vs if v <= max(n, 1))
    out = []
    groups = runs(verses)
    def collect_src(fn):
        res = []
        for i, (a, b) in enumerate(groups):
            if i: res.append(('…', None))
            res += [(v, t) for v, t, *rest in fn(a, b)]
        return res
    def joined(pairs):
        bits = []
        for v, t in pairs:
            bits.append('…' if v == '…' else f'**{v}** {t}')
        return ' '.join(bits)
    if code == '1EN':
        pairs = collect_src(lambda a, b: enoch_chapter(ch) and [(v, enoch_chapter(ch)[v]) for v in range(a, b + 1) if v in enoch_chapter(ch)])
        out += ['*R. H. Charles, The Book of Enoch (1917), public domain*', '', joined(pairs) or '(text not available)', '']
        return out
    if code in APOC.values():
        g = collect_src(lambda a, b: lxx((code, ch, a, b)))
        e = collect_src(lambda a, b: english('BRENTON', (code, ch, a, b)))
        out += ['*Greek (Septuagint, as printed in Brenton’s edition, public domain)*', '', '::: {lang=grc}', joined(g), ':::', '',
                '*English (Brenton, 1844)*', '', joined(e), '']
        return out
    if is_nt(code):
        g = collect_src(lambda a, b: greek_nt((code, ch, a, b)))
        out += ['*Greek (SBLGNT)*', '', '::: {lang=grc}', joined(g), ':::', '']
    else:
        h = []
        diff = False
        for i, (a, b) in enumerate(groups):
            if i: h.append(('…', None))
            for v, t, href in hebrew((code, ch, a, b)):
                lab = v if href == f'{ch}:{v}' else f'{v} [{href}]'
                if href != f'{ch}:{v}': diff = True
                h.append((lab, t))
        lang = 'Aramaic' if verses and all(is_aramaic(code, ch, v) for v in verses) else 'Hebrew'
        note = '; verse numbers in brackets are those of the Hebrew Bible' if diff else ''
        out += [f'*{lang} (Westminster Leningrad Codex{note})*', '', '::: {lang=he dir=rtl}', joined(h) if h else '(text not available)', ':::', '']
    b = collect_src(lambda a, b_: english('BSB', (code, ch, a, b_)))
    w = collect_src(lambda a, b_: english('WEB', (code, ch, a, b_)))
    out += ['*English (BSB)*', '', joined(b), '', '*English (WEB)*', '', joined(w), '']
    return out

def section_l(text, prefix, where, printed, heading):
    ent, ranges = merged(text)
    keys = sorted(ent, key=lambda k: (CANON.index(k[0]), k[1]))
    if not keys and not ranges:
        return None, {}
    scope = heading.split(' in ', 1)[-1].lower()
    lines = [f'<!-- BEGIN GENERATED textL -->', '', heading, '',
             f'Every passage cited or alluded to by reference in {scope} is printed here, original language first: '
             'Hebrew or Aramaic from the Westminster Leningrad Codex, Greek from the SBL Greek New Testament (the Septuagint for the Apocrypha), '
             'followed by two public-domain English translations, the Berean Standard Bible (BSB) and the World English Bible (WEB). '
             '1 Enoch is given in R. H. Charles’s translation. A long passage already printed in full earlier in the book is linked rather than repeated.', '']
    anchors = {}
    for code, ch in keys:
        vs = ent[(code, ch)]
        n = nverses(code, ch)
        full = set(range(1, n + 1)) if vs is None else set(vs)
        if not n:
            continue
        lab = label_runs(code, ch, vs)
        anchor = f'hl-{prefix}-{slug(code, ch)}'
        anchors[(code, ch)] = anchor
        lines += [f'### {lab} {{#{anchor}}}', '']
        prev = next((p for p in printed.get((code, ch), []) if full <= p[0]), None)
        if prev and len(full) > 5:
            lines += [f'Printed in full in {prev[2]}: see [{prev[3]}](#{prev[1]}).', '']
            continue
        lines += entry_body(code, ch, vs)
        printed.setdefault((code, ch), []).append((full, anchor, where, lab))
    for code, a, b in sorted(ranges, key=lambda r: (CANON.index(r[0]), r[1])):
        lab = f'{NAME[code]} {a}–{b}'
        anchor = f'hl-{prefix}-{code.lower()}-{a}-{b}'
        anchors[(code, f'{a}-{b}')] = anchor
        what = {('1EN', 1, 36): 'the Book of the Watchers', ('1EN', 72, 82): 'the Astronomical Book'}.get((code, a, b), 'a whole section of the book')
        lines += [f'### {lab} {{#{anchor}}}', '',
                  f'This reference names {what} ({b - a + 1} chapters) as a whole, which is too long to print here. '
                  f'Verses quoted from it in {scope} have their own entries.', '']
    lines += ['<!-- END GENERATED textL -->', '']
    return '\n'.join(lines), anchors

def insert_l(text, block):
    text = re.sub(r'\n*<!-- BEGIN GENERATED textL -->.*?<!-- END GENERATED textL -->\n?', '\n', text, flags=re.S)
    if block is None: return text.rstrip('\n') + '\n'
    m = re.search(r'^\[\^[^\]]+\]:', text, flags=re.M)
    if m:
        return text[:m.start()].rstrip('\n') + '\n\n' + block + '\n' + text[m.start():]
    return text.rstrip('\n') + '\n\n' + block

# ----------------------------------------------------------------------------
FILES = [  # reading order: (path, prefix, where-label, heading)
    (os.path.join(CH, '00b-readers-introduction.md'), 'rintro', 'the Reader’s Introduction', '## Texts Highlighted in This Introduction'),
    (os.path.join(CH, '00c-method.md'), 'method', 'the Method chapter', '## Texts Highlighted in This Chapter'),
    (os.path.join(CH, '00d-historical-introduction.md'), 'hist', 'the Historical Introduction', '## Texts Highlighted in This Introduction'),
    (os.path.join(CH, '00e-overview.md'), 'overview', 'the Overview', '## Texts Highlighted in This Overview'),
] + [(p, 'c' + os.path.basename(p)[:2], f'Chapter {int(os.path.basename(p)[:2])}', '## L. Texts Highlighted in This Chapter')
     for p in sorted(glob.glob(os.path.join(CH, '[01][0-9]-jude-*.md')))] + [
    (os.path.join(CH, '14-afterword.md'), 'after', 'the Afterword', '## Texts Highlighted in the Afterword'),
    (os.path.join(AP, 'A-textual-variants.md'), 'appa', 'Appendix A', '## Texts Highlighted in This Appendix'),
    (os.path.join(AP, 'B-disputed-interpretations.md'), 'appb', 'Appendix B', '## Texts Highlighted in This Appendix'),
    (os.path.join(AP, 'C-jude-and-2-peter.md'), 'appc', 'Appendix C', '## Texts Highlighted in This Appendix'),
]

def anchor_map():
    """Recompute {file basename: {(code, ch): anchor}} without writing (used by build.py for links)."""
    res = {}
    for path, prefix, where, heading in FILES:
        if not os.path.exists(path): continue
        ent, ranges = merged(open(path, encoding='utf-8').read())
        m = {(c, ch): f'hl-{prefix}-{slug(c, ch)}' for (c, ch) in ent if nverses(c, ch)}
        for code, a, b in ranges:
            m[(code, f'{a}-{b}')] = f'hl-{prefix}-{code.lower()}-{a}-{b}'
        res[os.path.basename(path)] = m
    return res

def link_refs(text, amap):
    """Turn references outside generated regions, headings, and footnote definitions into links to section L."""
    if not amap: return text
    out = []
    pos = 0
    # protect generated regions
    spans = [(m.start(), m.end()) for m in GEN_RE.finditer(text)]
    def protected(i):
        if any(a <= i < b for a, b in spans): return True
        ls = text.rfind('\n', 0, i) + 1
        line = text[ls:text.find('\n', i) if text.find('\n', i) != -1 else len(text)]
        return line.startswith('#') or line.startswith('[^') or line.startswith('|')
    for s, e, items in collect(text):
        if protected(s): continue
        it = items[0]
        key = (it[1], f'{it[2]}-{it[3]}') if it[0] == 'RANGE' else (it[0], it[1])
        a = amap.get(key)
        if not a: continue
        if text[max(0, s - 1):s] == '[' or text[e:e + 2] == '](':
            continue
        out.append(text[pos:s]); out.append(f'[{text[s:e]}](#{a})'); pos = e
    out.append(text[pos:])
    return ''.join(out)

# ----------------------------------------------------------------------------
# Overview: the whole letter
PARAS = [(1, 2), (3, 4), (5, 7), (8, 11), (12, 13), (14, 16), (17, 19), (20, 23), (24, 25)]
def overview_block():
    L = ['<!-- BEGIN GENERATED overview -->', '', '## The Epistle of Jude in Greek and in English', '',
         'The letter is printed first in the Greek of the SBL Greek New Testament and then in two public-domain English translations. '
         'The Berean Standard Bible (BSB) generally follows the critical (eclectic) Greek text used by most modern translations, and the World English Bible (WEB) follows the '
         'Byzantine Majority Text, so between them they show both of the main textual traditions; where they differ (for example, '
         '"Jesus" or "the Lord" in v. 5), Appendix A explains why. Section A of each chapter gives every verse in eighteen free translations.', '',
         '### Greek (SBLGNT)', '', '::: {lang=grc}']
    for a, b in PARAS:
        L += [' '.join(f'**{v}** {t}' for v, t in greek_nt(('JUD', 1, a, b))), '']
    L += [':::', '']
    for abbr, name in (('BSB', 'Berean Standard Bible'), ('WEB', 'World English Bible')):
        L += [f'### English ({name}, {abbr})', '']
        for a, b in PARAS:
            L += [' '.join(f'**{v}** {t}' for v, t in english(abbr, ('JUD', 1, a, b))), '']
    L += ['<!-- END GENERATED overview -->', '']
    return '\n'.join(L)

def replace_overview(text):
    if '<!-- BEGIN GENERATED overview -->' in text:
        return re.sub(r'<!-- BEGIN GENERATED overview -->.*?<!-- END GENERATED overview -->\n', overview_block(), text, flags=re.S)
    m = re.search(r'^## The Epistle of Jude in [^\n]*\n.*?(?=^## The shape of the letter)', text, flags=re.M | re.S)
    if not m: raise SystemExit('overview text section not found')
    return text[:m.start()] + overview_block() + '\n' + text[m.end():]

# ----------------------------------------------------------------------------
# Appendix A: how the eighteen translations read the major variants
def _t(abbr, v1, v2=None):
    return ' '.join(t for _, t in english(abbr, ('JUD', 1, v1, v2 or v1)))
THREE_GROUPS = {'DRA': 'And on others have mercy', 'NOY': 'on others have compassion', 'RV': 'and on some have mercy with fear',
                'ASV': 'and on some have mercy with fear', 'T4T': 'Pity those', 'ULB': 'To others be merciful',
                'FBV': 'Show mercy—but', 'LSV': 'show mercy to others in fear', 'BSB': 'to still others show mercy'}
TWO_GROUPS = {'TNT': 'other save with feare', 'GNV': 'other saue with feare', 'WBS': 'others save with fear',
              'DBY': 'others save with fear', 'YLT': 'some in fear save', 'WEB': 'snatching them out of the fire with fear',
              'OEB': 'To others show pity, but with caution', 'MSB': 'save others with fear', 'TCENT': 'others save with fear'}
GOD_V4 = {'YLT': True, 'T4T': False}
def variant_row(abbr):
    t1 = _t(abbr, 1)
    v1 = 'sanctified' if 'sanctif' in t1 else ('loved' if 'loved' in t1 else '?')
    t4 = _t(abbr, 4)
    if abbr in GOD_V4: g4 = GOD_V4[abbr]
    else:
        m = re.search(r'\b(den\w*|disown)\b(.{0,40})', t4)
        g4 = bool(m and 'God' in m.group(2))
    t5 = _t(abbr, 5)
    v5 = 'Jesus' if 'Jesus' in t5 else ('the Lord' if re.search(r'\bLord', t5) else '?')
    t15 = _t(abbr, 15)
    v15 = any(k in t15 for k in ('among them', 'amonge them', 'their impious'))
    t19 = _t(abbr, 19)
    if '[themselves]' in t19:
        v19 = 'set [themselves] apart (word supplied)'
    else:
        v19 = 'separate themselves' if ('themsel' in t19 or 'them selues' in t19) else 'cause divisions'
    t2223 = _t(abbr, 22, 23)
    if abbr in THREE_GROUPS:
        assert THREE_GROUPS[abbr] in t2223, (abbr, 'three')
        g = 'three'
    else:
        assert TWO_GROUPS[abbr] in t2223, (abbr, 'two')
        g = 'two'
    t25 = _t(abbr, 25)
    wise = ('wise' in t25) or ('wyse' in t25)
    thru = 'Jesus Christ' in t25 and 'before' in t25
    yn = lambda b: 'yes' if b else '—'
    return [v1, yn(g4), v5, yn(v15), v19, g, yn(wise), yn(thru)]

def variants_table():
    L = ['<!-- BEGIN GENERATED variants -->', '',
         '## A.2 How the eighteen translations read the major variants', '',
         'Each translation follows a particular form of the Greek (or, for the Douay-Rheims, the Latin Vulgate). The table shows how each one reads the variants that change the English. It is generated from the translations themselves by `tools/make_texts.py`. A dash means the translation does not have the word or phrase.', '',
         '| Translation | v. 1 | v. 4: “God” | v. 5 | v. 15: “their” / “among them” | v. 19 | vv. 22–23: groups | v. 25: “wise” | v. 25: “through Jesus Christ … before all time” |',
         '|---|---|---|---|---|---|---|---|---|']
    for abbr, eid, name, year, lic in TRANSLATIONS:
        L.append(f'| {abbr} ({year}) | ' + ' | '.join(variant_row(abbr)) + ' |')
    L += ['', 'Reading across the rows shows the textual families. Tyndale, the Geneva Bible, Webster, and Young’s Literal Translation follow the Textus Receptus. The World English Bible, the Majority Standard Bible, and the Text-Critical English New Testament follow the Byzantine Majority Text. The Revised Version, Darby, the American Standard Version, the Translation for Translators, the Open English Bible, the Unlocked Literal Bible, the Free Bible Version, and the Berean Standard Bible follow critical texts, and Noyes mostly does. The Douay-Rheims follows the Latin Vulgate, which is why it reads “Jesus” in v. 5 and “reprove” in v. 22. The Literal Standard Version mixes readings from both traditions (see A.4).', '',
          '<!-- END GENERATED variants -->', '']
    return '\n'.join(L)

def replace_variants(text):
    if '<!-- BEGIN GENERATED variants -->' in text:
        return re.sub(r'<!-- BEGIN GENERATED variants -->.*?<!-- END GENERATED variants -->\n', variants_table(), text, flags=re.S)
    i = text.index('## A.3 ')
    return text[:i] + variants_table() + '\n' + text[i:]

def main():
    printed = {}
    total_l = 0
    for path, prefix, where, heading in FILES:
        if not os.path.exists(path): continue
        text = open(path, encoding='utf-8').read()
        base = os.path.basename(path)
        cv = chapter_verses(base)
        if cv:
            text = replace_section_a(text, *cv)
        if base == '00e-overview.md':
            text = replace_overview(text)
        if base == 'A-textual-variants.md':
            text = replace_variants(text)
        block, anchors = section_l(text, prefix, where, printed, heading)
        text = insert_l(text, block)
        open(path, 'w', encoding='utf-8').write(text)
        total_l += len(anchors)
        print(f'{base}: {"section A, " if cv else ""}{len(anchors)} highlighted passages')
    print(f'Total highlighted entries: {total_l}')

if __name__ == '__main__':
    main()
