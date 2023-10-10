from nltk.ccg import lexicon

__all__ = ["generate"]

def generate(lex: lexicon.CCGLexicon, max_len: int):
    # tab[lenght-1][category]{instance: str}
    tab = [dict()]

    for text, tokens in lex._entries.items():
        for token in tokens:
            cat = token.categ()
            tab[0].setdefault(cat, set())
            tab[0][cat].add(text)

    for k in range(1, max_len):
        tab.append(dict())
        for a in range(k):
            b = k-a-1 # (a+1) + (b+1) == (k+1)
            for a_cat, a_set in tab[a].items():
                if a_cat.is_primitive(): continue
                assert a_cat.dir().is_forward() or a_cat.dir().is_backward(), f"Unhandled direction '{a_cat.dir()}'"
                forward = a_cat.dir().is_forward()
                b_cat = a_cat.arg()
                k_cat = a_cat.res()
                b_set = tab[b].get(b_cat, set())
                for a_text in a_set:
                    for b_text in b_set:
                        k_text = a_text+" "+b_text if forward else b_text+" "+a_text
                        tab[k].setdefault(k_cat, set())
                        tab[k][k_cat].add(k_text)

    ret = []
    for x in tab:
        ret += list(x.get(lex.start(), []))

    return ret
