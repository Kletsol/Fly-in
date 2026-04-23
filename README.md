

regle le graph impossiblement accessible

creer un dict contenant pour chaque tour, chaque drone et sa position :
    {
    Tour_1: {D1: position, D2: position, D3: position, ...}
    Tour_2: {D1: position, D2: position, D3: position, ...}
    Tour_2: {D1: position, D2: position, D3: position, ...}
    }
update le dictionnaire a chaque tour

Tour 1: n(next_zone_capacity, next_connection_capacity) drones partent du start
    dict.update(positions)

reutiliser le dictionnaire pour visualisation

