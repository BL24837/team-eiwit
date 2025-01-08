State-space

Opdracht 1:

Een student heeft 12 verschillende vakken van 2 uur welke geroosterd moeten worden van maandag t/m vrijdag in tijdsloten 9-11, 11-13, 13-15, 15-17. Hoeveel verschillende roosters zijn er mogelijk voor deze student zonder overlap van vakken?

Antwoord 1:

20! / (12!(20-12))! = 20! / (12! * 8!) = 125970

Opdracht 2:

Je fietst door Manhattan, New York en kunt bij elk kruispunt linksaf, rechtsaf of rechtdoor. Hoeveel verschillende routes kun je rijden vanaf een gegeven beginpunt en richting met daarin 20 kruispunten?

Antwoord 2:

3^20 = 3,486,784,401

Opdracht 3:

Er moeten 50 dozen met flesjes water, 50 dozen fruit, en 30 dozen broodjes worden vervoerd. In de bestelbus passen 25 dozen. Hoeveel verschillende ladingen kun je in het eerste ritje meenemen als je een volle lading meeneemt?

Antwoord 3:

(25 + 3 - 1)! / 25!(3-1)! = 351

Opdracht 4:

Om af te studeren moet een student 30 vakken hebben afgerond, maar een student mag er ook meer doen. Een student kan daarbij kiezen uit 110 verschillende aangeboden vakken. Op hoeveel verschillende manieren kan een student afstuderen met 30, 31 of 32 vakken?

Antwoord 4:

110! / (30! * (110-30)!) + 110! / (31! * (110-31)!) + 110! / (32! * (110-32)!) = 2.5107×10^33


Opdracht 5:

Een loterij heeft balletjes A t/m Z waaruit een notaris op volgorde 7 willekeurige balletjes trekt zonder terugleggen. Wat is de kans dat het lot met DBFAECG wint?

Antwoord 5:

1 / (26! / (26 - 7)!) = 3.02×10^−10

Opdracht 6:

Opnieuw moeten 50 dozen met flesjes water, 50 dozen fruit, en 30 dozen broodjes worden vervoerd. Je hebt nu een vrachtwagen waarin 45 dozen passen. Hoeveel verschillende ladingen kun je nu in het eerste ritje meenemen als je een volle lading meeneemt?

Antwoord 6:

((45 + 3 - 1)! / (45!(3-1)!)) - (((15 + 3 - 1)! / (15!(3-1)!)) - ((15 + 2 - 1)! / (15!(2-1)!))) = 961

Opdracht 7:

Antwoord 1:

Proteïn Pow(d)er

Antwoord 2:

We hebben een string van x beschikbare posities. Bij de eitwit HHPHHHPH, hebben we dus 8 beschikbare posities waarvan er 2 gevuld moeten worden door P en de overige 6 posities door H. De mogelijke eiwitten zijn dus: 8!/2!6!.
Bij de eiwit HHPHHHPHPHHHPH geldt dan 14!/4!10! etc.

Antwoord 3:

De werkelijke state-space grootte kan hier nooit boven liggen omdat ik alle mogelijke eiwitten heb berekend.

Antwoord 4:

n!/a!b!c!. Met n het aantal mogelijke posities, met a het aantal keer voor letter a, met b het aantal keer voor letter b en c het aantal keer voor letter c

Antwoord 5:

Stel we hebben een string van 5 mogelijke posities: ,,,,_ (de kommas worden gebruikt om aan te duiden dat het verschillende posities zijn). En we hebben 2 letters: A en B. Volgens mijn formule zou het aantal mogelijke posities 10 moeten zijn. Dit klopt ook want als ik alle mogelijke posities uitschrijf: AAABB, AABAB, AABBA, ABABA, ABBAA, ABAAB, BAAAB, BAABA, BABAA, BBAAA.

Antwoord 6:

Voor HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH geldt: 
50!/24!26! = 1.21549E14 = 121,549,000,000,000
Voor HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH geldt:
50!/21!6!23! = 3.19819E19 = 31,981,900,000,000,000,000

Vraag 7:

Antwoord 3:
Het eerste aminozuur heeft een ontelbaar aantal keuze om zich ergens op de grid te plaatsen. De tweede heeft door de vrije ruimte hieromheen vier keuzes om zich te plaatsen. Daarna heeft elk van de aminozuren maximaal 3 richtingen die de aminozuur kan kiezen. Dit is een versimpelde aanname, omdat sommige aminozuren maar 2 richtingen hebben. 

Antwoord 4:
De bovengrens van onze state-space kan worden berekend met de volgende formule: 4 * (3^n-2)

Antwoord 5:

Antwoord 6:
Voor HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH geldt:
4 * (3 ^ 50 - 2) = 3.19066 * 10 ^ 23