import gurobipy as gp

def solve_tsp(city_distances, cities):
    print('start solving TSP...')
    model = gp.Model("TSP")
    
    vars = gp.tupledict()
    for city_distance in city_distances.keys():
        vars[city_distance] = model.addVar(obj=city_distances[city_distance], vtype=gp.GRB.BINARY, name='x'+str(city_distance))
    
    for city in cities:
        model.addConstr(gp.quicksum(vars.select(city, '*')) == 1)
        model.addConstr(gp.quicksum(vars.select('*', city)) == 1)
    
    #Die Variablen sind durch den obj = city_distances[city_distance] schon in der Zielfunktion und es muss
    #nur die Art des Zielfunktion (minimize) definiert werden; alternativ muss die Variable noch mit ihrer Distanz
    #gewichtet werden. model.setObjective überschreibt alle vorherigen Zielfunktionswerte.
    #Alternativ geht also auch:
    #model.setObjective(gp.quicksum(vars[(from_city, to_city)] *city_distances[(from_city, to_city)] for from_city, to_city in vars.keys() ), gp.GRB.MINIMIZE)
    model.modelSense = gp.GRB.MINIMIZE
    model.optimize()
    
    route = []
    for key in vars.keys():
        if vars[key].x > 0.1: 
            route.append(key)
    
    def find_next_arc(route,city):
        for city_tuple in route:
            if city == city_tuple[0]:
                return city_tuple
        raise Exception('City not found in route')
    
    def get_sub_tour(route):
        possible_sub_tour = []
        possible_sub_tour.append(route[0])
        next_tuple = find_next_arc(route,route[0][1])
        possible_sub_tour.append(next_tuple)
        while True:
            next_tuple = find_next_arc(route, possible_sub_tour[-1][1])
            if next_tuple in possible_sub_tour:
                return possible_sub_tour
            possible_sub_tour.append(next_tuple)
            if len(possible_sub_tour) == len(route):
                return route
        
    sub_tour = get_sub_tour(route)
    while sub_tour != len(route):
        model.addConstr(gp.quicksum(vars[from_city, to_city] for from_city, to_city in sub_tour) <= len(sub_tour) - 1)
        model.update()
        model.optimize()
        route = []
        for key in vars.keys():
            if vars[key].x > 0.1: 
                route.append(key)
        sub_tour = get_sub_tour(route)
        


    print('Done...')
    return route
    