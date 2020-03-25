## Etap 1 - pobranie składowych pojedynczej opinii
- opinia li.review-box
- identyfikator li.review-box["data-entry-id"]
- autor li.reviewer-name-line
- rekomendacja div.product-review-summary > em
- gwiazdki span.review-score-count
- potwierdzona zakupem div.product-review-pz
- data wystawienia span.review-time > time["datetime"] - pierwszy element listy
- data zakupu span.review-time > time["datetime"] - drugi element listy
- przydatna span["id=votes-yes"]
    button.vote-yes["data-total-vote"]
    button.vote-yes > span
- nieprzydatna span["id=votes-no"]
    button.vote-no["data-total-vote"]
    button.vote-no > span
- treść p.product-review-body
- wady div.cons-cell > ul
- zalety div.pros-cell > ul
- opinia: li.review-box
- identyfikator: li.review-box["data-entry-id"]
- autor: div.reviewer-name-line
- rekomendacja: div.product-review-summary > em
- gwiazdki: span.review-score-count
- potwierdzona zakupem: div.product-review-pz
- data wystawienia: span.review-time > time["datetime"] - pierwszy element listy
- data zakupu: span.review-time > time["datetime"] - drugi element listy
- przydatna: span[id=^votes-yes]
             button.vote-yes["data-total-vote"]
             button.vote-yes > span
- nieprzydatna: span[id=^votes-no]
                button.vote-no["data-total-vote"]
                button.vote-no > span
- treść: p.product-review-body
- wady: div.cons-cell > ul
- zalety: div.pros-cell > ul
## Etap 2 - pobranie składowych wszystkich opinii z poedynczej strony
- zapisanie składowych opinii w złożonej strukturze danych
## Etap 3 - pobranie wszystkich opinii o pojedynczym produkcie
- przechodzenie po stronach z opiniami
- eksport opinii do pliku (.csv. lub .xlsx lub .json)
