from collections import defaultdict, deque

# Build graph from input files

# tt-id = title, rating
movie_dict = {}

# movies
file = open("movies.tsv", "r")
for row in file:
    movie = row.strip().split("\t")
    if len(movie) < 4:
        continue

    movie_id = movie[0]
    movie_title = movie[1]
    movie_rating = float(movie[2])
    movie_dict[movie_id] = (movie_title, movie_rating)

file.close()


# nm-id = tt-id list
actor_dict = {}

# Actors
file = open("actors.tsv", "r")
for row in file:
    actor = row.strip().split("\t")
    if len(actor) < 2:
        continue
    
    actor_id = actor[0]
    actor_name = actor[1]
    actor_movies = []
    for movie in actor[2:]:
        if movie in movie_dict:
            actor_movies.append(movie)
    actor_dict[actor_id] = {"name":actor_name, "movies":actor_movies}

file.close()


# Graph using neighbor list

# nm_id = {neighbor_nm_id : [(title, rating), more movies...]}
graph = defaultdict(dict)

movie_cast = defaultdict(set)

for nm_id, actor_info in actor_dict.items():
    for tt_id in actor_info["movies"]:
        movie_cast[tt_id].add(nm_id)

for tt_id, actors in movie_cast.items():
    actors = list(actors)
    title, rating = movie_dict[tt_id]
    
    for i in range(len(actors)):
        for j in range(i+1, len(actors)):
            actor1 = actors[i]
            actor2 = actors[j]

            graph[actor1].setdefault(actor2, []).append((title, rating))
            graph[actor2].setdefault(actor1, []).append((title, rating))

# Count nodes and edges

def count_graph(graph):
    print(f"Nodes: {len(graph)}")

    total_neighbors = 0
    for neighbors in graph.values():
        total_neighbors += len(neighbors)
    edges = total_neighbors // 2

    print(f"Edges: {edges}")

count_graph(graph)


# Shortest path between actors

# Weight not relevant for shortest path in our graph
# BFS guarantees shortest path in unweighted graph
def BFS_shortest_path(graph, start, target):
    visited = set()
    queue = deque()
    parent = {}

    visited.add(start)
    queue.append(start)

    while queue:
        u = queue.popleft()
        if u == target:
            path = []
            while u != start:
                path.append(u)
                u = parent[u]
            path.append(start)
            path.reverse()
            return path
            
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                queue.append(v)


pairs = [
    ("nm2255973", "nm0000460", "Donald Glover", "Jeremy Irons"),
    ("nm0424060", "nm8076281", "Scarlett Johansson", "Emma Mackey"),    
    ("nm4689420", "nm0000365", "Carrie Coon", "Julie Delpy"),
    ("nm0000288", "nm2143282", "Christian Bale", "Lupita Nyong’o"),
    ("nm0637259", "nm0931324", "Tuva Novotny", "Michael K. Williams")
]

for start, target, start_name, target_name in pairs:
    path = BFS_shortest_path(graph, start, target)

    print(f"\n{start_name}")
    for i in range(len(path) - 1):
        nm_id_1 = path[i]
        nm_id_2 = path[i+1]
        actor1 = actor_dict[nm_id_1]["name"]
        actor2 = actor_dict[nm_id_2]["name"]
        mutual = graph[nm_id_1][nm_id_2]

        description = []
        if mutual:
            for title, rating in mutual:
                details = f"{title} ({rating})"
                description.append(details)
        
        movies = ", ".join(description)

        print(f"===[ {movies} ] ===> {actor2}")

        

















     














