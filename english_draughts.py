# Grupa: 231   Nume: Cirstea Natasa Alexandra
import time
import copy


class Joc:
    """
    Clasa care defineste jocul
    """
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JUC = ['n', 'a']
    JMIN = None
    JMAX = None
    GOL = '.'
    # consideram ca jmax are piesele in partea de sus, iar jmin in partea de jos
    DIRECTII_JMAX = [(1, -1), (1, 1)]
    DIRECTII_JMIN = [(-1, -1), (-1, 1)]
    TIMP_INCEPERE = 0
    MUTARI_JMIN = 0
    MUTARI_JMAX = 0
    ADANCIME_INCEPATOR = 1
    ADANCIME_MEDIU = 2
    ADANCIME_AVANSAT = 3
    NR_PIESE_JUCATOR = 12

    def __init__(self, tabla=None, pozitii_JMAX=None, pozitii_JMIN=None):
        if tabla is not None:
            self.matr = copy.deepcopy(tabla)

            if pozitii_JMAX is None or pozitii_JMIN is None:
                self.pozitii_JMAX, self.pozitii_JMIN = self.pozitii_piese()
            else:
                self.pozitii_JMAX = copy.deepcopy(pozitii_JMAX)
                self.pozitii_JMIN = copy.deepcopy(pozitii_JMIN)
        else:
            self.matr = []
            for i in range(Joc.NR_LINII):
                aux = []
                char_matr = [Joc.GOL, ' ']
                for j in range(Joc.NR_COLOANE):
                    if i % 2 == 0:
                        aux.append(char_matr[(i * Joc.NR_LINII + j + 1) % 2])
                    else:
                        aux.append(char_matr[(i * Joc.NR_LINII + j) % 2])
                self.matr.append(aux)

            self.pozitii_JMAX = set()
            self.pozitii_JMIN = set()

            # consideram ca jmax are piesele in partea de sus, iar jmin in partea de jos
            # asezam piesele pe tabla si, in acelasi timp, adaugam pozitiile pieselor in listele de pozitii ale celor 2 jucatori
            for i in range(3):
                if(i % 2 == 0):
                    for j in range(1, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = Joc.JMAX
                        self.pozitii_JMAX.add((i, j))
                else:
                    for j in range(0, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = Joc.JMAX
                        self.pozitii_JMAX.add((i, j))

            for i in range(Joc.NR_LINII - 3, Joc.NR_LINII):
                if(i % 2 == 0):
                    for j in range(1, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = Joc.JMIN
                        self.pozitii_JMIN.add((i, j))
                else:
                    for j in range(0, Joc.NR_COLOANE, 2):
                        self.matr[i][j] = Joc.JMIN
                        self.pozitii_JMIN.add((i, j))

    def pozitii_piese(self):
        # returnam pozitiile pieselor celor 2 jucatori
        pozitii_JMIN = set()
        pozitii_JMAX = set()

        for i in range(Joc.NR_LINII):
            for j in range(Joc.NR_COLOANE):
                if self.matr[i][j].lower() == Joc.JMIN.lower():
                    pozitii_JMIN.add((i, j))
                elif self.matr[i][j].lower() == Joc.JMAX.lower():
                    pozitii_JMAX.add((i, j))

        return [pozitii_JMAX, pozitii_JMIN]

    def final(self):
        # returnam simbolul jucatorului castigator daca jucator nu mai are piese
        # sau returnam 'remiza' cand un jucator nu mai poate face nicio miscare
        # sau 'False' daca nu s-a terminat jocul

        # jocul se termina cand un jucator ia toate piesele jucatorului opus sau cand un jucator nu mai poate face nicio miscare, caz in care este remiza
        # numarul de piese este egal cu numarul de pozitii pe care avem asezate piese

        if len(self.pozitii_JMAX) == 0:
            return Joc.JMIN
        elif len(self.pozitii_JMIN) == 0:
            return Joc.JMAX

        # daca nu mai putem face nicio miscare, avem remiza
        if(len(self.mutari(Joc.JMAX)) == 0 or len(self.mutari(Joc.JMIN)) == 0):
            return 'remiza'

        return False

    def jucator_opus(self, jucator):
        if jucator == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutare_obisnuita(self, pozitie, directie, jucator):
        # incercam sa efectuam o miscare simpla de la 'pozitie' in directia 'directie'
        # linie si coloana reprezinta pozitia pe care trebuie mutata piesa
        linie = pozitie[0] + directie[0]
        coloana = pozitie[1] + directie[1]

        if 0 <= linie and linie < Joc.NR_LINII and 0 <= coloana and coloana < Joc.NR_COLOANE:
            if self.matr[linie][coloana] == Joc.GOL:
                joc_nou = Joc(self.matr, self.pozitii_JMAX,
                              self.pozitii_JMIN)
                joc_nou.matr[linie][coloana] = joc_nou.matr[pozitie[0]][pozitie[1]]
                joc_nou.matr[pozitie[0]][pozitie[1]] = Joc.GOL

                # actualizam lista pozitiilor pe care se afla piesele fiecarui jucator
                if jucator == Joc.JMAX:
                    joc_nou.pozitii_JMAX.discard((pozitie[0], pozitie[1]))
                    joc_nou.pozitii_JMAX.add((linie, coloana))
                else:
                    joc_nou.pozitii_JMIN.discard((pozitie[0], pozitie[1]))
                    joc_nou.pozitii_JMIN.add((linie, coloana))

                # daca o piesa obisnuita ajunge pe randul din capatul opus, piesa devine rege
                if joc_nou.matr[linie][coloana] == joc_nou.matr[linie][coloana].lower():
                    if ((jucator == Joc.JMAX and linie == Joc.NR_LINII - 1) or
                            (jucator == Joc.JMIN and linie == 0)):
                        joc_nou.matr[linie][coloana] = joc_nou.matr[linie][coloana].upper(
                        )

                # returnam noua tabla de joc si numarul de miscari care au fost efectuate
                return (joc_nou, 1)

        return False

    def mutare_cu_saritura(self, pozitie, directie, jucator, nr_mutari):
        # incercam sa efectuam o miscare cu saritura de la 'pozitie' in directia 'directie'
        j_opus = self.jucator_opus(jucator)
        # linia si coloana pozitiei curente
        linie = pozitie[0]
        coloana = pozitie[1]

        # coordonatele pozitiei peste care trebuie sa sarim si ale pozitiei in care trebuie sa ajungem
        p1_l, p1_c = linie + directie[0], coloana + directie[1]
        p2_l, p2_c = linie + 2*directie[0], coloana + 2*directie[1]

        if (0 <= p2_l and p2_l < Joc.NR_LINII and
            0 <= p2_c and p2_c < Joc.NR_COLOANE and
                self.matr[p1_l][p1_c].lower() == j_opus.lower() and self.matr[p2_l][p2_c] == Joc.GOL):
            joc_nou = Joc(self.matr, self.pozitii_JMAX, self.pozitii_JMIN)
            joc_nou.matr[p2_l][p2_c] = joc_nou.matr[linie][coloana]
            joc_nou.matr[p1_l][p1_c] = Joc.GOL
            joc_nou.matr[linie][coloana] = Joc.GOL

            # actualizam lista pozitiilor pe care se afla piesele fiecarui jucator
            if jucator == Joc.JMAX:
                joc_nou.pozitii_JMIN.discard((p1_l, p1_c))
                joc_nou.pozitii_JMAX.discard((linie, coloana))
                joc_nou.pozitii_JMAX.add((p2_l, p2_c))
            else:
                joc_nou.pozitii_JMAX.discard((p1_l, p1_c))
                joc_nou.pozitii_JMIN.discard((linie, coloana))
                joc_nou.pozitii_JMIN.add((p2_l, p2_c))

            piesa_poate_continua = True

            # daca o piesa obisnuita ajunge pe randul din capatul opus, piesa devine rege si se opreste
            if joc_nou.matr[p2_l][p2_c] == joc_nou.matr[p2_l][p2_c].lower():
                if ((jucator == Joc.JMAX and p2_l == Joc.NR_LINII - 1) or
                        (jucator == Joc.JMIN and p2_l == 0)):
                    piesa_poate_continua = False
                    joc_nou.matr[p2_l][p2_c] = joc_nou.matr[p2_l][p2_c].upper()

            # returnam noua tabla de joc, pozitia pe care se afla acum piesa, daca poate continua si numarul de miscari care au fost efectuate
            return [joc_nou, (p2_l, p2_c), piesa_poate_continua, nr_mutari + 1]

        return False

    def lista_mutari_pozitie(self, pozitie, l_directii, jucator):
        # returneaza o lista cu elemente de tip joc ce rezulta in urma mutarii
        # sau o lista goala daca nu se poate face nicio mutare

        mutari = []

        # daca piesa curenta este rege, poate sa se miste si inapoi, deci trebuie sa adaugam si directiile de intoarcere
        directii = copy.deepcopy(l_directii)
        if self.matr[pozitie[0]][pozitie[1]] == self.matr[pozitie[0]][pozitie[1]].upper():
            for directie in l_directii:
                directii.append((-directie[0], -directie[1]))

        # incercam sa mutam piesa in directiile date folosind o miscare obisnuita
        for directie in directii:
            # mutare obisnuita
            mutare = self.mutare_obisnuita(pozitie, directie, jucator)
            if mutare is not False:
                mutari.append(mutare)

        # incercam sa mutam piesa in directiile date folosind o miscare cu saritura
        # retinem miscarile obtinute intr-o lista auxiliara de miscari intrucat,
        # daca dupa o miscare cu saritura se poate face o alta miscare cu saritura, jucatorul este obligat sa o faca
        mutari_auxiliare = []
        for directie in directii:
            # mutare cu saritura
            m_nou = self.mutare_cu_saritura(pozitie, directie, jucator, 0)
            if m_nou is not False:
                mutari_auxiliare.append(m_nou)

        # cum suntem obligati sa facem sarituri atat timp cat este posibil,
        # vom efectua sarituri pana cand piesa nu mai poate continua
        while len(mutari_auxiliare) > 0:
            m = mutari_auxiliare.pop(0)
            joc = m[0]
            pozitie = m[1]
            piesa_poate_continua = m[2]
            nr_mutari = m[3]

            if piesa_poate_continua:
                for directie in directii:
                    # mutare cu saritura
                    m_nou = joc.mutare_cu_saritura(
                        pozitie, directie, jucator, nr_mutari)
                    if m_nou is not False:
                        mutari_auxiliare.append(m_nou)
            else:
                # piesa nu mai poate continua, deci miscarea curenta este finala si valida, asa ca o adaugam in lista de mutari
                mutari.append((joc, m[3]))

        return mutari

    def mutari(self, jucator):
        l_mutari = []

        # stabilim pozitiile pieselor jucatorului curent, precum si directiile in care poate muta piesele
        if jucator == Joc.JMAX:
            pozitii_piese = self.pozitii_JMAX
            l_directii = Joc.DIRECTII_JMAX
        else:
            pozitii_piese = self.pozitii_JMIN
            l_directii = Joc.DIRECTII_JMIN

        # generam toate mutarile pe care le poate face jucatorul
        for pozitie in pozitii_piese:
            mutari = self.lista_mutari_pozitie(pozitie, l_directii, jucator)
            for mutare in mutari:
                l_mutari.append(mutare)

        return l_mutari

    def mutare_simpla_de_la_pozitie(self, jucator, l_1, c_1, l_2, c_2):
        # daca putem efectua o miscare de la pozitia (l_1, c_1) la pozitia (l_2, c_2), returnam tabla de joc obtinuta prin efectuarea miscarii
        #       si False intrucat, dupa efectuarea unei miscari simple, piesa nu mai poate continua
        # altfel returnam False cu specificatia ca piesa nu poate fi mutata de la pozitia (l_1, c_1) la pozitia (l_2, c_2) printr-o miscare simpla
        if self.matr[l_2][c_2] != Joc.GOL:
            return False

        if jucator == Joc.JMAX:
            pozitii_piese = self.pozitii_JMAX
            l_directii = Joc.DIRECTII_JMAX
        else:
            pozitii_piese = self.pozitii_JMIN
            l_directii = Joc.DIRECTII_JMIN

        directii = copy.deepcopy(l_directii)
        # daca piesa este rege, adaugam si miscarile pentru intoarcere
        if self.matr[l_1][c_1] == self.matr[l_1][c_1].upper():
            for directie in l_directii:
                directii.append((-directie[0], -directie[1]))

        # incercam sa mutam piesa pe toate directiile posibile si verififam daca in urma mutarii am obtinut coordonatele celei de-a doua pozitii
        for directie in directii:
            if l_1 + directie[0] == l_2 and c_1 + directie[1] == c_2:
                joc_nou = Joc(self.matr, self.pozitii_JMAX,
                              self.pozitii_JMIN)
                joc_nou.matr[l_2][c_2] = joc_nou.matr[l_1][c_1]
                joc_nou.matr[l_1][c_1] = Joc.GOL

                # actualizam lista pozitiilor pe care se afla piesele fiecarui jucator
                if jucator == Joc.JMAX:
                    joc_nou.pozitii_JMAX.discard((l_1, c_1))
                    joc_nou.pozitii_JMAX.add((l_2, c_2))
                else:
                    joc_nou.pozitii_JMIN.discard((l_1, c_1))
                    joc_nou.pozitii_JMIN.add((l_2, c_2))

                # daca o piesa obisnuita ajunge pe randul din capatul opus, piesa devine rege
                if joc_nou.matr[l_2][c_2] == joc_nou.matr[l_2][c_2].lower():
                    if ((jucator == Joc.JMAX and l_2 == Joc.NR_LINII - 1) or
                            (jucator == Joc.JMIN and l_2 == 0)):
                        joc_nou.matr[l_2][c_2] = joc_nou.matr[l_2][c_2].upper(
                        )

                # returnam o lista pentru a avea aceeasi structura ca in cazul mutarii cu saritura in scopul evitarii unor comparatii suplimentare
                return [joc_nou, False]

        return False

    def mutare_cu_saritura_de_la_pozitie(self, jucator, l_1, c_1, l_2, c_2):
        # daca putem efectua o miscare de la pozitia (l_1, c_1) la pozitia (l_2, c_2), returnam tabla de joc obtinuta prin efectuarea miscarii
        #       si 'piesa_trebuie_sa_continue' intrucat, dupa efectuarea unei miscari cu saritura, piesa poate fi obligata sa mai execute o miscare cu saritura
        # altfel returnam False cu specificatia ca piesa nu poate fi mutata de la pozitia (l_1, c_1) la pozitia (l_2, c_2) printr-o miscare cu saritura
        if self.matr[l_2][c_2] != Joc.GOL:
            return False

        j_opus = self.jucator_opus(jucator)

        if jucator == Joc.JMAX:
            pozitii_piese = self.pozitii_JMAX
            l_directii = Joc.DIRECTII_JMAX
        else:
            pozitii_piese = self.pozitii_JMIN
            l_directii = Joc.DIRECTII_JMIN

        directii = copy.deepcopy(l_directii)
        # daca piesa este rege, adaugam si miscarile pentru intoarcere
        if self.matr[l_1][c_1] == self.matr[l_1][c_1].upper():
            for directie in l_directii:
                directii.append((-directie[0], -directie[1]))

        for directie in directii:
            if l_1 + 2*directie[0] == l_2 and c_1 + 2*directie[1] == c_2 and self.matr[l_1 + directie[0]][c_1 + directie[1]].lower() == j_opus.lower():
                joc_nou = Joc(self.matr, self.pozitii_JMAX, self.pozitii_JMIN)
                joc_nou.matr[l_2][c_2] = joc_nou.matr[l_1][c_1]
                joc_nou.matr[l_1][c_1] = Joc.GOL
                joc_nou.matr[l_1 + directie[0]][c_1 + directie[1]] = Joc.GOL

                # actualizam lista pozitiilor pe care se afla piesele fiecarui jucator
                if jucator == Joc.JMAX:
                    joc_nou.pozitii_JMIN.discard(
                        (l_1 + directie[0], c_1 + directie[1]))
                    joc_nou.pozitii_JMAX.discard((l_1, c_1))
                    joc_nou.pozitii_JMAX.add((l_2, c_2))
                else:
                    joc_nou.pozitii_JMAX.discard(
                        (l_1 + directie[0], c_1 + directie[1]))
                    joc_nou.pozitii_JMIN.discard((l_1, c_1))
                    joc_nou.pozitii_JMIN.add((l_2, c_2))

                piesa_trebuie_sa_continue = True

                # daca o piesa obisnuita ajunge pe randul din capatul opus, piesa devine rege si se opreste
                if joc_nou.matr[l_2][c_2] == joc_nou.matr[l_2][c_2].lower():
                    if ((jucator == Joc.JMAX and l_2 == Joc.NR_LINII - 1) or
                            (jucator == Joc.JMIN and l_2 == 0)):
                        piesa_trebuie_sa_continue = False
                        joc_nou.matr[l_2][c_2] = joc_nou.matr[l_2][c_2].upper()

                if piesa_trebuie_sa_continue == True:
                    piesa_trebuie_sa_continue = False
                    for d2 in directii:
                        if joc_nou.mutare_cu_saritura((l_2, c_2), d2, jucator, 0) != False:
                            piesa_trebuie_sa_continue = True
                            break

                return [joc_nou, piesa_trebuie_sa_continue]

        return False

    def fct_euristica_1(self):
        # 1 varianta: returnam diferenta dintre numarul de piese al jucatorului JMAX si numarul de piese al jucatorului JMIN
        # cu cat diferenta este mai mare, cu atat JMIN are mai putine piese pe tabla si, deci, cu atat JMAX este mai aproape de a castiga
        return len(self.pozitii_JMAX) - len(self.pozitii_JMIN)

    def fct_euristica_2(self):
        # 2 varianta: returnam diferenta dintre numarul de piese gata de atac al jucatorului JMAX si numarul de piese gata de atac al jucatorului JMIN
        # o piesa este gata de atac daca poate realiza o miscare care sa ia cel putin o piesa a celuilalt jucator
        # cu cat un jucator are mai multe piese in pozitie de atac, cu atat are mai multe sanse sa reduca numarul pieselor jucatorului opus

        nr_piese_JMAX = 0
        nr_piese_JMIN = 0

        for pozitie in self.pozitii_JMAX:
            directii = self.DIRECTII_JMAX
            if self.matr[pozitie[0]][pozitie[1]].isupper():
                for dir in self.DIRECTII_JMAX:
                    directii.append((-dir[0], -dir[1]))

            for dir in directii:
                if self.mutare_cu_saritura(pozitie, dir, Joc.JMAX, 0) is not False:
                    nr_piese_JMAX += 1
                    break

        for pozitie in self.pozitii_JMIN:
            directii = self.DIRECTII_JMIN
            if self.matr[pozitie[0]][pozitie[1]].isupper():
                for dir in self.DIRECTII_JMIN:
                    directii.append((-dir[0], -dir[1]))

            for dir in directii:
                if self.mutare_cu_saritura(pozitie, dir, Joc.JMAX, 0) is not False:
                    nr_piese_JMIN += 1
                    break

        return nr_piese_JMAX - nr_piese_JMIN

    def get_e1(self):
        return self.fct_euristica_1()

    def get_e2(self):
        return self.fct_euristica_2()

    def number_to_euristica(self, euristica):
        switcher = {
            1: self.get_e1,
            2: self.get_e2
        }
        # Get the function from switcher dictionary
        func = switcher.get(euristica, lambda: 1)
        # Execute the function
        return func()

    def estimeaza_scor(self, adancime, euristica):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (999+adancime)
        elif t_final == Joc.JMIN:
            return (-999-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.number_to_euristica(euristica)

    def __str__(self):
        sir = '    '
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + '   '

        sir += '\n   '
        for nr_col in range(self.NR_COLOANE):
            sir += '____'
        sir += '\n'

        for index in range(self.NR_LINII):
            sir += "  |"
            sir += ("  |".join([' '
                                for x in self.matr[index][0: self.NR_COLOANE]])+"  |\n")

            sir += str(index)

            sir += " | "
            sir += (" | ".join([str(x)
                                for x in self.matr[index][0: self.NR_COLOANE]])+" |\n")
            sir += "  |"
            sir += ("__|".join(['_'
                                for x in self.matr[index][0: self.NR_COLOANE]])+"__|\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        # vom lua mutarile posibile pornind de la tabla de joc actuala. structura unei mutari este mutare = [tabla_joc, nr_mutari_efectuate]
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [
            (Stare(mutare[0], juc_opus, self.adancime-1, parinte=self), mutare[1]) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + \
            "  (Jucator curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare, euristica):
    # nu mai expandam daca am ajus la adancimea maxima sau daca suntem intr-o stare finala
    if stare.adancime == 0 or stare.tabla_joc.final() or len(stare.mutari()) == 0:
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, euristica)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    if len(stare.mutari_posibile) == 0:
        # nu mai putem face nicio miscare din starea in care suntem
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, euristica)
        return stare

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [(min_max(mutare[0], euristica), mutare[1])
                   for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        mutare_aleasa = max(mutari_scor, key=lambda x: x[0].scor)
        stare.stare_aleasa = mutare_aleasa[0]
        if stare.adancime == stare.ADANCIME_MAX:
            Joc.MUTARI_JMAX += mutare_aleasa[1]
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        mutare_aleasa = min(mutari_scor, key=lambda x: x[0].scor)
        stare.stare_aleasa = mutare_aleasa[0]

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare, euristica):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, euristica)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    if len(stare.mutari_posibile) == 0:
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, euristica)
        return stare

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        nr_mutari = 0
        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare[0], euristica)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
                nr_mutari = mutare[1]
            if(alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

        if stare.adancime == stare.ADANCIME_MAX:
            Joc.MUTARI_JMAX += nr_mutari

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare[0], euristica)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if(beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if(final):
        if (final == "remiza"):
            print(
                "Remiza!\n" + f'SCOR: {Joc.JMAX}: {len(stare_curenta.tabla_joc.pozitii_JMAX)}, {Joc.JMIN}: {len(stare_curenta.tabla_joc.pozitii_JMIN)}\n')
        else:
            print("A castigat " + final +
                  f'\nSCOR: {Joc.JMAX}: {len(stare_curenta.tabla_joc.pozitii_JMAX)}, {Joc.JMIN}: {len(stare_curenta.tabla_joc.pozitii_JMIN)}\n')

        return True

    return False


def main():
    Joc.TIMP_INCEPERE = int(round(time.time() * 1000))
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input(
            "Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\nOptiune: ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX in functie de nivelul ales de jucator: incepator, mediu, avansat
    raspuns_valid = False
    while not raspuns_valid:
        n = input(
            "\nAlegeti dificultatea jocului: 1. incepator, 2. mediu, 3. avansat\nOptiune: ")
        if n.isdigit():
            dificultate = int(n)
            if 1 <= dificultate and dificultate <= 3:
                if dificultate == 1:
                    Stare.ADANCIME_MAX = Joc.ADANCIME_INCEPATOR
                elif dificultate == 2:
                    Stare.ADANCIME_MAX = Joc.ADANCIME_MEDIU
                else:
                    Stare.ADANCIME_MAX = Joc.ADANCIME_AVANSAT
                raspuns_valid = True
            else:
                print("Trebuie sa introduceti un numar cuprins intre 1 si 3.")
        else:
            print("Trebuie sa introduceti un numar cuprins intre 1 si 3.")

    # setam euristica aleasa
    raspuns_valid = False
    euristica = 1
    while not raspuns_valid:
        n = input(
            "\nExista doua euristici disponibile: 1. diferenta de pisese, 2. diferenta de piese gata de atac\nOptiune: ")
        if n.isdigit():
            euristica = int(n)
            if 1 <= euristica and euristica <= 2:
                raspuns_valid = True
            else:
                print("Trebuie sa introduceti un numar cuprins intre 1 si 2.")
        else:
            print("Trebuie sa introduceti un numar cuprins intre 1 si 2.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(
            input("\nDoriti sa jucati cu {} sau cu {}?\nOptiune: ".format(s1, s2))).lower()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    # initializare tabla
    tabla_curenta = Joc()
    print("______________________________________________________________")
    print("\nTabla initiala\n")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(
        tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True:
        print("______________________________________________________________")
        print(
            f'\nTIMP RULARE PROGRAM: { int(round(time.time() * 1000)) - Joc.TIMP_INCEPERE} milisecunde')
        print(
            f'MUTARI: {Joc.JMAX}: {Joc.MUTARI_JMAX}, {Joc.JMIN}: {Joc.MUTARI_JMIN}')
        print(
            f'SCOR/NUMAR PIESE CAPTURATE: {Joc.JMAX}: {Joc.NR_PIESE_JUCATOR - len(stare_curenta.tabla_joc.pozitii_JMIN)}, {Joc.JMIN}: {Joc.NR_PIESE_JUCATOR - len(stare_curenta.tabla_joc.pozitii_JMAX)}')
        print(
            f'MISCARI DISPONIBILE: {Joc.JMAX}: {len(stare_curenta.tabla_joc.mutari(Joc.JMAX))}, {Joc.JMIN}: {len(stare_curenta.tabla_joc.mutari(Joc.JMIN))}')
        print("______________________________________________________________")

        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            print(
                f'\nACUM ESTE RANDUL JUCATORULUI: {Joc.JMIN}')

            exit = str(input(
                '\nDaca doriti sa incheiati jocul, tastati "exit", altfel apasati orice tasta.\n'))
            if exit == 'exit':
                print(
                    f'REMIZA\nSCOR/NUMAR PIESE CAPTURATE: {Joc.JMAX}: {Joc.NR_PIESE_JUCATOR - len(stare_curenta.tabla_joc.pozitii_JMIN)}, {Joc.JMIN}: {Joc.NR_PIESE_JUCATOR - len(stare_curenta.tabla_joc.pozitii_JMAX)}')
                break

            # -------------------------------- inceput preluare date jucator ------------------------
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))

            l_1, c_1, l_2, c_2 = 0, 0, 0, 0
            raspuns_valid = False
            print("\nIntroduceti linia si coloana piesei de mutat:")
            while not raspuns_valid:
                try:
                    l_1 = int(input("linie = "))
                    if 0 <= l_1 and l_1 < Joc.NR_LINII:
                        try:
                            c_1 = int(input("coloana = "))
                            if 0 <= c_1 and c_1 < Joc.NR_COLOANE:
                                # linia si coloana se afla in matrice.
                                # ramane de verificat la aceasta pozitie sa se afle o piesa apartinand jucatorului curent
                                if stare_curenta.tabla_joc.matr[l_1][c_1].lower() == (Joc.JMIN).lower():
                                    raspuns_valid = True
                                else:
                                    print("In pozitia ({},{}) nu se afla o piesa care va apartine.".format(
                                        l_1, c_1))
                            else:
                                print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(
                                    Joc.NR_COLOANE - 1))
                        except ValueError:
                            print("Coloana trebuie sa fie un numar intreg.")
                    else:
                        print("Linia invalida (trebuie sa fie un numar intre 0 si {}).".format(
                            Joc.NR_LINII - 1))
                except ValueError:
                    print("Linia trebuie sa fie un numar intreg.")

            raspuns_valid = False
            mutari = []
            print(
                "\nIntroduceti linia si coloana pozitiei in care doriti sa mutati piesa:")
            while not raspuns_valid:
                try:
                    l_2 = int(input("linie = "))
                    if 0 <= l_2 and l_2 < Joc.NR_LINII:
                        try:
                            c_2 = int(input("coloana = "))
                            if 0 <= c_2 and c_2 < Joc.NR_COLOANE:
                                # linia si coloana se afla in matrice.
                                # ramane de verificat ca pozitia este goala si ca se poate realiza o mutare in aceasta pozitie

                                if stare_curenta.tabla_joc.matr[l_2][c_2] != Joc.GOL:
                                    print("In pozitia ({},{}) se afla deja o piesa.".format(
                                        l_2, c_2))
                                else:
                                    mutari = stare_curenta.tabla_joc.mutare_simpla_de_la_pozitie(
                                        stare_curenta.j_curent, l_1, c_1, l_2, c_2)

                                    if mutari == False:
                                        mutari = stare_curenta.tabla_joc.mutare_cu_saritura_de_la_pozitie(
                                            stare_curenta.j_curent, l_1, c_1, l_2, c_2)

                                        if mutari == False:
                                            print("Piesa nu poate fi mutata in pozitia ({},{}).".format(
                                                l_2, c_2))
                                        else:
                                            raspuns_valid = True
                                    else:
                                        raspuns_valid = True
                            else:
                                print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(
                                    Joc.NR_COLOANE - 1))
                        except ValueError:
                            print("Coloana trebuie sa fie un numar intreg.")
                    else:
                        print("Linia invalida (trebuie sa fie un numar intre 0 si {}).".format(
                            Joc.NR_LINII - 1))
                except ValueError:
                    print("Linia trebuie sa fie un numar intreg.")

            # -------------------------------- sfarsit preluare date jucator ------------------------

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))

            stare_curenta = Stare(
                mutari[0], stare_curenta.j_curent, stare_curenta.adancime, parinte=stare_curenta)

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            print("Jucatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")
            Joc.MUTARI_JMIN += 1

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            mai_efectuam_o_miscare = mutari[1]
            while mai_efectuam_o_miscare == True:
                print("In urma mutarii se mai poate efectua o miscare cu saritura.")

                mutari = []
                l_directii = Joc.DIRECTII_JMIN
                directii = copy.deepcopy(l_directii)
                # daca piesa este rege, adaugam si miscarile pentru intoarcere
                if stare_curenta.tabla_joc.matr[l_2][c_2] == stare_curenta.tabla_joc.matr[l_2][c_2].upper():
                    for directie in l_directii:
                        directii.append((-directie[0], -directie[1]))

                for directie in directii:
                    mutare = stare_curenta.tabla_joc.mutare_cu_saritura(
                        (l_2, c_2), directie, stare_curenta.j_curent, 0)
                    if mutare != False:
                        mutari.append(mutare)

                # [joc_nou, (p2_l, p2_c), piesa_poate_continua]
                if len(mutari) == 1:
                    mutare = mutari[0]
                    stare_curenta = Stare(
                        mutare[0], stare_curenta.j_curent, stare_curenta.adancime, parinte=stare_curenta)
                    l_2, c_2 = mutare[1][0], mutare[1][1]
                    mai_efectuam_o_miscare = mutare[2]

                elif len(mutari) > 1:
                    raspuns_valid = False
                    while not raspuns_valid:
                        print(
                            "Exista mai multe variante de miscari posibile din pozitia actuala. \nIntroduceti numarul variantei dorite.")

                        for index in range(len(mutari)):
                            print(f"Varianta {index}:")
                            print(mutari[index][0])

                        try:
                            varianta = int(input("varianta = "))
                            if 0 <= varianta and varianta < len(mutari):
                                mutare = mutari[varianta]
                                stare_curenta = Stare(
                                    mutare[0], stare_curenta.j_curent, stare_curenta.adancime, parinte=stare_curenta)
                                l_2, c_2 = mutare[1][0], mutare[1][1]
                                mai_efectuam_o_miscare = mutare[2]
                                raspuns_valid = True
                            else:
                                print("Varianta invalida (trebuie sa fie un numar intre 0 si {}).".format(
                                    len(mutari) - 1))
                        except ValueError:
                            print("Varianta trebuie sa fie un numar intreg.")

                    else:
                        mai_efectuam_o_miscare == False
                        break

                # afisarea starii jocului in urma mutarii utilizatorului
                print("\nTabla dupa mutarea jucatorului")
                print(str(stare_curenta))

                Joc.MUTARI_JMIN += 1

                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                if (afis_daca_final(stare_curenta)):
                    break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            print(
                f'\nACUM ESTE RANDUL CALCULATORULUI: {Joc.JMAX}')

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta, euristica)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000,
                                               5000, stare_curenta, euristica)

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            time.sleep(1)
            print("\nTabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            print("Calculatorul a \"gandit\" timp de " +
                  str(t_dupa-t_inainte)+" milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
