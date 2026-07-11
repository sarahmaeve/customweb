"""Project configuration for the KARTAS segment index.

Everything site- or segment-specific lives here, so re-pointing the tools at a
different Ken-and-Robin recurring segment (or another WordPress tag archive with
the same theme) is a config edit, not a code change.
"""

# --- source site --------------------------------------------------------------
SITE = "https://www.kenandrobintalkaboutstuff.com"
SITE_LABEL = "Ken and Robin Talk About Stuff"
TAG_SLUG = "consulting-occultist"
TAG_LABEL = "Consulting Occultist"

# Regex used to find the paragraph that describes the segment. Kept deliberately
# loose ("Occ") so it still matches the show-notes typo "Occulist" and the early
# short form "Consulting Occult".
SEGMENT_MARKER = r"Consulting Occ"

# --- rendered page ------------------------------------------------------------
OUTPUT_HTML = "knrconsulting.html"
PAGE_TITLE = "The Consulting Occultist — a reading record"
KICKER = "Ken and Robin Talk About Stuff · a reading record"
HEADLINE_HTML = "The <em>Consulting Occultist</em>"  # raw HTML; <em> gets the gilt marker
SEARCH_PLACEHOLDER = "Search a subject or title — Dee, geomancy, chess…"

NO_SEGMENT_NOTE = f"[No {TAG_LABEL} segment written up in this episode's show notes.]"

# Episodes whose notes name the segment differently, or omit a write-up entirely.
# Keyed by permalink; the value replaces the auto-extracted segment text.
OVERRIDES = {
    f"{SITE}/index.php/episode-630-live-at-dragonmeet-2024/": NO_SEGMENT_NOTE,
    f"{SITE}/index.php/episode-534-manimal-utopia/": NO_SEGMENT_NOTE,
    f"{SITE}/index.php/episode-320-ghost-rationing-policy/":
        "Our survey of Belle Epoque weirdness ducks into the Eliptony Hut with a "
        "profile of early parapsychologist Albert de Rochas.",
}


def tag_url() -> str:
    return f"{SITE}/index.php/tag/{TAG_SLUG}/"


def page_url(n: int) -> str:
    """Archive page URL. Page 1 has no /page/ suffix on this theme."""
    return tag_url() if n == 1 else f"{tag_url()}page/{n}/"


# --- Wikipedia links ----------------------------------------------------------
# Hand-curated links to the specific person, work, group, or named event each
# episode's segment covers. Keyed by episode number; the value is a list of
# (label, url) pairs, rendered as chips beneath the segment (see kartas.refs_html
# and build_html.entry_li). Only specific, named subjects are linked -- broad
# practices (tarot, ley lines, chaos magick, geomancy) are deliberately left
# bare. URLs were resolved against the Wikipedia API (redirects followed, canonical
# titles kept). Re-scraping posts.json never touches this table.
WIKI = {
    695: [("Simon Forman", "https://en.wikipedia.org/wiki/Simon_Forman")],
    691: [("Pythagoras", "https://en.wikipedia.org/wiki/Pythagoras")],
    679: [("Douglas MacArthur", "https://en.wikipedia.org/wiki/Douglas_MacArthur")],
    674: [("Alejandro Jodorowsky", "https://en.wikipedia.org/wiki/Alejandro_Jodorowsky")],
    668: [("Walter Russell", "https://en.wikipedia.org/wiki/Walter_Russell")],
    661: [("Alexandra David-Néel", "https://en.wikipedia.org/wiki/Alexandra_David-N%C3%A9el")],
    655: [("Graham Bond", "https://en.wikipedia.org/wiki/Graham_Bond")],
    648: [("Florence Farr", "https://en.wikipedia.org/wiki/Florence_Farr")],
    643: [("Albin Grau", "https://en.wikipedia.org/wiki/Albin_Grau")],
    639: [("William Lyon Mackenzie King", "https://en.wikipedia.org/wiki/William_Lyon_Mackenzie_King")],
    635: [("Aby Warburg", "https://en.wikipedia.org/wiki/Aby_Warburg")],
    629: [("William Stainton Moses", "https://en.wikipedia.org/wiki/William_Stainton_Moses")],
    626: [("Anna Kingsford", "https://en.wikipedia.org/wiki/Anna_Kingsford")],
    622: [("Gan De", "https://en.wikipedia.org/wiki/Gan_De")],
    619: [("William Wynn Westcott", "https://en.wikipedia.org/wiki/William_Wynn_Westcott")],
    615: [("Johannes Trithemius", "https://en.wikipedia.org/wiki/Johannes_Trithemius")],
    608: [("Grand Albert", "https://en.wikipedia.org/wiki/Petit_Albert"), ("The Long Lost Friend", "https://en.wikipedia.org/wiki/The_Long_Lost_Friend")],
    604: [("Evangeline Adams", "https://en.wikipedia.org/wiki/Evangeline_Adams")],
    601: [("Nostradamus", "https://en.wikipedia.org/wiki/Nostradamus")],
    596: [("Indriði Indriðason", "https://en.wikipedia.org/wiki/Indri%C3%B0i_Indri%C3%B0ason")],
    594: [("Maria de Naglowska", "https://en.wikipedia.org/wiki/Maria_de_Naglowska")],
    591: [("Robert Fludd", "https://en.wikipedia.org/wiki/Robert_Fludd")],
    580: [("Isaac Bickerstaff", "https://en.wikipedia.org/wiki/Isaac_Bickerstaff"), ("John Partridge", "https://en.wikipedia.org/wiki/John_Partridge_(astrologer)")],
    575: [("Hélène Smith", "https://en.wikipedia.org/wiki/H%C3%A9l%C3%A8ne_Smith")],
    572: [("Ophiuchus", "https://en.wikipedia.org/wiki/Ophiuchus_(astrology)")],
    564: [("Durek Verrett", "https://en.wikipedia.org/wiki/Durek_Verrett")],
    562: [("Isaac Newton", "https://en.wikipedia.org/wiki/Isaac_Newton")],
    558: [("Mother Shipton", "https://en.wikipedia.org/wiki/Mother_Shipton")],
    555: [("Edward II", "https://en.wikipedia.org/wiki/Edward_II")],
    547: [("Nicholas Hawksmoor", "https://en.wikipedia.org/wiki/Nicholas_Hawksmoor")],
    542: [("Alexander of Abonoteichus", "https://en.wikipedia.org/wiki/Alexander_of_Abonoteichus")],
    539: [("Yves Klein", "https://en.wikipedia.org/wiki/Yves_Klein")],
    526: [("Happy Science", "https://en.wikipedia.org/wiki/Happy_Science")],
    523: [("Suzanne Treister", "https://en.wikipedia.org/wiki/Suzanne_Treister")],
    518: [("Cotton Mather", "https://en.wikipedia.org/wiki/Cotton_Mather")],
    514: [("Jeremy Bentham", "https://en.wikipedia.org/wiki/Jeremy_Bentham")],
    506: [("Gerald Gardner", "https://en.wikipedia.org/wiki/Gerald_Gardner")],
    494: [("Roger Bacon", "https://en.wikipedia.org/wiki/Roger_Bacon")],
    490: [("Swami Vivekananda", "https://en.wikipedia.org/wiki/Swami_Vivekananda")],
    487: [("Gospel of Jesus's Wife", "https://en.wikipedia.org/wiki/Gospel_of_Jesus%27_Wife")],
    482: [("P. L. Travers", "https://en.wikipedia.org/wiki/P._L._Travers"), ("George Gurdjieff", "https://en.wikipedia.org/wiki/George_Gurdjieff")],
    478: [("Montague Summers", "https://en.wikipedia.org/wiki/Montague_Summers")],
    473: [("Wild Bill Hickok", "https://en.wikipedia.org/wiki/Wild_Bill_Hickok"), ("Dead man's hand", "https://en.wikipedia.org/wiki/Dead_man%27s_hand")],
    468: [("Krotona", "https://en.wikipedia.org/wiki/Krotona")],
    463: [("Claudio Naranjo", "https://en.wikipedia.org/wiki/Claudio_Naranjo")],
    458: [("Seal of Chicago", "https://en.wikipedia.org/wiki/Seal_of_Chicago")],
    455: [("Grigori Grabovoi", "https://en.wikipedia.org/wiki/Grigori_Grabovoi")],
    449: [("José López Rega", "https://en.wikipedia.org/wiki/Jos%C3%A9_L%C3%B3pez_Rega")],
    442: [("Austin Osman Spare", "https://en.wikipedia.org/wiki/Austin_Osman_Spare")],
    438: [("Baird T. Spalding", "https://en.wikipedia.org/wiki/Baird_T._Spalding")],
    435: [("John Joseph Merlin", "https://en.wikipedia.org/wiki/John_Joseph_Merlin")],
    431: [("Michael Scot", "https://en.wikipedia.org/wiki/Michael_Scot")],
    428: [("Timothy Leary", "https://en.wikipedia.org/wiki/Timothy_Leary")],
    425: [("Israel Regardie", "https://en.wikipedia.org/wiki/Israel_Regardie")],
    422: [("Herbie Brennan", "https://en.wikipedia.org/wiki/James_Herbert_Brennan")],
    419: [("Fernando Pessoa", "https://en.wikipedia.org/wiki/Fernando_Pessoa")],
    416: [("Pamela Colman Smith", "https://en.wikipedia.org/wiki/Pamela_Colman_Smith")],
    411: [("Ouija", "https://en.wikipedia.org/wiki/Ouija"), ("Elijah Bond", "https://en.wikipedia.org/wiki/Elijah_Bond")],
    404: [("Battle of Kursk", "https://en.wikipedia.org/wiki/Battle_of_Kursk")],
    398: [("Nicholas Roerich", "https://en.wikipedia.org/wiki/Nicholas_Roerich")],
    390: [("George William Russell", "https://en.wikipedia.org/wiki/George_William_Russell")],
    385: [("Oswald Wirth", "https://en.wikipedia.org/wiki/Oswald_Wirth"), ("Stanislas de Guaita", "https://en.wikipedia.org/wiki/Stanislas_de_Guaita")],
    383: [("Samuel Liddell MacGregor Mathers", "https://en.wikipedia.org/wiki/Samuel_Liddell_MacGregor_Mathers"), ("Moina Mathers", "https://en.wikipedia.org/wiki/Moina_Mathers")],
    381: [("Papus", "https://en.wikipedia.org/wiki/G%C3%A9rard_Encausse")],
    380: [("Christian Rosenkreuz", "https://en.wikipedia.org/wiki/Christian_Rosenkreuz")],
    369: [("Cornelius Agrippa", "https://en.wikipedia.org/wiki/Heinrich_Cornelius_Agrippa")],
    367: [("Brother XII", "https://en.wikipedia.org/wiki/Brother_XII")],
    355: [("Marianne Williamson", "https://en.wikipedia.org/wiki/Marianne_Williamson")],
    352: [("Thiess of Kaltenbrun", "https://en.wikipedia.org/wiki/Thiess_of_Kaltenbrun")],
    335: [("J. F. C. Fuller", "https://en.wikipedia.org/wiki/J._F._C._Fuller")],
    329: [("Carlos Castaneda", "https://en.wikipedia.org/wiki/Carlos_Castaneda")],
    326: [("Cock Lane ghost", "https://en.wikipedia.org/wiki/Cock_Lane_ghost"), ("Samuel Johnson", "https://en.wikipedia.org/wiki/Samuel_Johnson")],
    321: [("Jules Doinel", "https://en.wikipedia.org/wiki/Jules_Doinel")],
    320: [("Albert de Rochas", "https://en.wikipedia.org/wiki/Albert_de_Rochas")],
    319: [("Léo Taxil", "https://en.wikipedia.org/wiki/L%C3%A9o_Taxil")],
    310: [("James Bridle", "https://en.wikipedia.org/wiki/James_Bridle")],
    307: [("Rosaleen Norton", "https://en.wikipedia.org/wiki/Rosaleen_Norton")],
    304: [("Alexander Dugin", "https://en.wikipedia.org/wiki/Aleksandr_Dugin")],
    301: [("Julius Evola", "https://en.wikipedia.org/wiki/Julius_Evola")],
    298: [("Reginald Scot", "https://en.wikipedia.org/wiki/Reginald_Scot"), ("The Discoverie of Witchcraft", "https://en.wikipedia.org/wiki/The_Discoverie_of_Witchcraft")],
    290: [("Isaac Newton", "https://en.wikipedia.org/wiki/Isaac_Newton")],
    284: [("Savitri Devi", "https://en.wikipedia.org/wiki/Savitri_Devi")],
    282: [("Ritman Library", "https://en.wikipedia.org/wiki/Bibliotheca_Philosophica_Hermetica")],
    270: [("Warlocks of Chiloé", "https://en.wikipedia.org/wiki/Warlocks_of_Chilo%C3%A9")],
    267: [("Joséphin Péladan", "https://en.wikipedia.org/wiki/Jos%C3%A9phin_P%C3%A9ladan")],
    263: [("William Blake", "https://en.wikipedia.org/wiki/William_Blake")],
    255: [("Posadism", "https://en.wikipedia.org/wiki/Fourth_International%E2%80%93Posadist")],
    247: [("Harry Houdini", "https://en.wikipedia.org/wiki/Harry_Houdini")],
    244: [("Harry Chandler", "https://en.wikipedia.org/wiki/Harry_Chandler")],
    240: [("Robert Moses", "https://en.wikipedia.org/wiki/Robert_Moses"), ("Jane Jacobs", "https://en.wikipedia.org/wiki/Jane_Jacobs")],
    231: [("Denver International Airport", "https://en.wikipedia.org/wiki/Denver_International_Airport")],
    227: [("Ripley Scroll", "https://en.wikipedia.org/wiki/George_Ripley_(alchemist)")],
    225: [("Ralstonism", "https://en.wikipedia.org/wiki/Ralstonism")],
    223: [("Éliphas Lévi", "https://en.wikipedia.org/wiki/%C3%89liphas_L%C3%A9vi")],
    213: [("Jakob Böhme", "https://en.wikipedia.org/wiki/Jakob_B%C3%B6hme")],
    202: [("Rudolf II", "https://en.wikipedia.org/wiki/Rudolf_II,_Holy_Roman_Emperor")],
    192: [("Alan Moore", "https://en.wikipedia.org/wiki/Alan_Moore")],
    186: [("Black Dragon Society", "https://en.wikipedia.org/wiki/Black_Dragon_Society")],
    181: [("Kenelm Digby", "https://en.wikipedia.org/wiki/Kenelm_Digby")],
    177: [("Paracelsus", "https://en.wikipedia.org/wiki/Paracelsus")],
    175: [("Tom Driberg", "https://en.wikipedia.org/wiki/Tom_Driberg")],
    172: [("John Dee", "https://en.wikipedia.org/wiki/John_Dee")],
    168: [("Le Corbusier", "https://en.wikipedia.org/wiki/Le_Corbusier")],
    164: [("North Berwick witch trials", "https://en.wikipedia.org/wiki/North_Berwick_witch_trials")],
    157: [("Priory of Sion", "https://en.wikipedia.org/wiki/Priory_of_Sion")],
    154: [("Roger Bacon", "https://en.wikipedia.org/wiki/Roger_Bacon")],
    149: [("Dion Fortune", "https://en.wikipedia.org/wiki/Dion_Fortune")],
    144: [("Elias Ashmole", "https://en.wikipedia.org/wiki/Elias_Ashmole")],
    137: [("Rudolf Steiner", "https://en.wikipedia.org/wiki/Rudolf_Steiner")],
    135: [("John Murray Spear", "https://en.wikipedia.org/wiki/John_Murray_Spear")],
    133: [("Benandanti", "https://en.wikipedia.org/wiki/Benandanti")],
    131: [("Goetia", "https://en.wikipedia.org/wiki/Goetia")],
    119: [("George Gurdjieff", "https://en.wikipedia.org/wiki/George_Gurdjieff")],
    118: [("Nicolas Flamel", "https://en.wikipedia.org/wiki/Nicolas_Flamel")],
    117: [("Papus", "https://en.wikipedia.org/wiki/G%C3%A9rard_Encausse")],
    116: [("Charles Richet", "https://en.wikipedia.org/wiki/Charles_Richet")],
    112: [("Margaret Murray", "https://en.wikipedia.org/wiki/Margaret_Murray")],
    109: [("Synarchism", "https://en.wikipedia.org/wiki/Synarchism")],
    105: [("Sarah Helen Whitman", "https://en.wikipedia.org/wiki/Sarah_Helen_Whitman")],
    102: [("Catharism", "https://en.wikipedia.org/wiki/Catharism")],
    99: [("Father Yod", "https://en.wikipedia.org/wiki/Father_Yod")],
    97: [("London Stone", "https://en.wikipedia.org/wiki/London_Stone")],
    94: [("Ed and Lorraine Warren", "https://en.wikipedia.org/wiki/Ed_and_Lorraine_Warren")],
    89: [("Count of St. Germain", "https://en.wikipedia.org/wiki/Count_of_St._Germain")],
    87: [("Cagliostro", "https://en.wikipedia.org/wiki/Alessandro_Cagliostro")],
    84: [("Franz Anton Mesmer", "https://en.wikipedia.org/wiki/Franz_Mesmer")],
    81: [("Ioan Culianu", "https://en.wikipedia.org/wiki/Ioan_Petru_Culianu")],
    79: [("Voynich Manuscript", "https://en.wikipedia.org/wiki/Voynich_manuscript")],
    73: [("Andrew Jackson Davis", "https://en.wikipedia.org/wiki/Andrew_Jackson_Davis")],
    65: [("Voynich Manuscript", "https://en.wikipedia.org/wiki/Voynich_manuscript")],
    62: [("Ralph Waldo Emerson", "https://en.wikipedia.org/wiki/Ralph_Waldo_Emerson")],
    56: [("Rosicrucianism", "https://en.wikipedia.org/wiki/Rosicrucianism")],
    48: [("Ahnenerbe", "https://en.wikipedia.org/wiki/Ahnenerbe")],
    47: [("Thule Society", "https://en.wikipedia.org/wiki/Thule_Society")],
    46: [("Spear of Destiny", "https://en.wikipedia.org/wiki/Holy_Lance")],
    45: [("Karl-Maria Wiligut", "https://en.wikipedia.org/wiki/Karl_Maria_Wiligut")],
    44: [("Guido von List", "https://en.wikipedia.org/wiki/Guido_von_List")],
    39: [("Elizabeth Clare Prophet", "https://en.wikipedia.org/wiki/Elizabeth_Clare_Prophet")],
    37: [("Paschal Beverly Randolph", "https://en.wikipedia.org/wiki/Paschal_Beverly_Randolph")],
    32: [("Christopher Marlowe", "https://en.wikipedia.org/wiki/Christopher_Marlowe")],
    30: [("Atlantis", "https://en.wikipedia.org/wiki/Atlantis"), ("Hyperborea", "https://en.wikipedia.org/wiki/Hyperborea")],
    27: [("Black Herman", "https://en.wikipedia.org/wiki/Black_Herman")],
    25: [("William Dudley Pelley", "https://en.wikipedia.org/wiki/William_Dudley_Pelley")],
    22: [("Fox sisters", "https://en.wikipedia.org/wiki/Fox_sisters")],
    20: [("Affair of the Poisons", "https://en.wikipedia.org/wiki/Affair_of_the_Poisons")],
    15: [("Anton LaVey", "https://en.wikipedia.org/wiki/Anton_LaVey")],
    13: [("Kenneth Grant", "https://en.wikipedia.org/wiki/Kenneth_Grant_(occultist)")],
    11: [("John Dee", "https://en.wikipedia.org/wiki/John_Dee")],
    8: [("Aleister Crowley", "https://en.wikipedia.org/wiki/Aleister_Crowley")],
    6: [("Helena Blavatsky", "https://en.wikipedia.org/wiki/Helena_Blavatsky")],
    3: [("Johnny Appleseed", "https://en.wikipedia.org/wiki/Johnny_Appleseed"), ("Emanuel Swedenborg", "https://en.wikipedia.org/wiki/Emanuel_Swedenborg")],
    1: [("Hermetic Order of the Golden Dawn", "https://en.wikipedia.org/wiki/Hermetic_Order_of_the_Golden_Dawn"), ("W. B. Yeats", "https://en.wikipedia.org/wiki/W._B._Yeats"), ("Bram Stoker", "https://en.wikipedia.org/wiki/Bram_Stoker"), ("Aleister Crowley", "https://en.wikipedia.org/wiki/Aleister_Crowley")],
}

