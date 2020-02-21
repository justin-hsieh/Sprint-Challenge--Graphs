from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/test_loop_fork2.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Store entire map as graph dictionary
map_graph = {}

# create dictionary entry for each room when visited
def current_room_entry():
    room = {}
    # for exits in the current room
    for exit in player.current_room.get_exits():
        # assign "?" to exits
        room[exit] = "?"
        # create key/value pair with current room and exits
        map_graph[player.current_room.id] = room


# find random exit that hasn't been explored yet in the current room
def random_exit():
    # track the unexplored exits
    unexplored = []
    # find the exits in a current room
    for exit in player.current_room.get_exits():
        # check whether given exit has '?" for being unexplored
        if map_graph[player.current_room.id][exit] == "?":
            # append exit if found
            unexplored.append(exit)

    # return a randomized choice from unexplored exits
    return random.choice(unexplored)

# BFS function to find nearest '?' unexplored exit
# return a list of room ids needed to get to first room with unexplored exits
def nearest_unexplored_exit(room_id):

    queue = Queue()
    queue.enqueue([room_id])
    visited = set()

    while queue.size() > 0:
        path = queue.dequeue()
        current_room = path[-1]
        # check first after dequeue whether this room has unexplored exits, return path immediately if so
        if list(map_graph[current_room].values()).count('?') != 0:
            return path
        # if current room has not been visited
        if current_room not in visited:
            # add it to the visited set
            visited.add(current_room)
            # After current room added to visited, need to queue rooms that need to be checked for unexplored exits
            for new_room in map_graph[current_room].values():
                new_path = path.copy()
                new_path.append(new_room)
                queue.enqueue(new_path)


# initialize the map graph at starting location
current_room_entry()
# loop through map and build a graph, check against size of room_graph
while len(map_graph) < len(room_graph):

    # for current room, check if it still has '?' exits remaining
    if list(map_graph[player.current_room.id].values()).count('?') != 0:
        # assign room IDs
        room_id = player.current_room.id
        # travere to exit with '?' in random direction
        random_direction = random_exit()
        # move in that random direction to an unexplored room
        player.travel(random_direction)
        # add direction to Traversal-Path
        traversal_path.append(random_direction)
        # check if the room is already in map_graph, otherwise create a new room entry to be added
        if player.current_room.id not in map_graph:
            current_room_entry()
        # assign room number to previous room exit values
        map_graph[room_id][random_direction] = player.current_room.id
        # assign previous room id to current room exit value with flipped direction
        flipped_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        map_graph[player.current_room.id][flipped_direction[random_direction]] = room_id
    else:
        # use BFS to find nearest room with unexplored exit(s)
        backward_path = nearest_unexplored_exit(player.current_room.id)
        # use backward_path to move the player back
        # path needs to be converted to traversal_path directions
        for room_id in backward_path:
            # for each of the directions in a room
            for direction in map_graph[player.current_room.id]:
                # match which room id matches
                if map_graph[player.current_room.id][direction] == room_id:
                    # move the player and add to traversal_path
                    player.travel(direction)
                    traversal_path.append(direction)
                    # break out the inner loop as it just moved the player
                    break
                # check for next room location

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
'''
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''