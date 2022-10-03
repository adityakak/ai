import sys


def heappush(heap, item):
    heap.append(item)  # Adds the item to the heap
    heapify(heap,
            int((heap.index(item) - 1) / 2))  # Runs the heapify function onto the parent of the newly inserted item


def heappop(heap):
    save = heap[0]  # Saves the value of the item being removed
    rPos = 0
    while rightChild(rPos) < len(heap) - 1:  # Finds the rightmost item in the heap and replaces the root with it
        rPos = rightChild(rPos)
    heap[0] = heap[rPos]
    heap.pop(rPos)
    heapify(heap, 0)  # Runs heapify function on the root
    return save


def heapify(arr, pos):
    if not leaf(arr, pos):  # Checks if the item is a leaf or not
        if rightChild(pos) > len(arr) - 1:  # Checks for either two children or one
            if arr[leftChild(pos)] < arr[pos]:  # Finds if the item is smaller than its left child
                swap(arr, leftChild(pos),
                     pos)  # Swaps the parent and child and reruns on the child's old location
                heapify(arr, leftChild(pos))
            if pos != 0:  # If we are not at the root re-run heapify on the next item up the list
                heapify(arr, pos - 1)
        else:
            minPos = minimum(arr, leftChild(pos), rightChild(pos))  # Returns position of the lower of the two children
            if arr[minPos] < arr[pos]:  # Swaps the parent and child and reruns on the child's old location
                swap(arr, minPos, pos)
                heapify(arr, minPos)
            if pos != 0:  # If we are not at the root re-run heapify on the next item up the list
                heapify(arr, pos - 1)


def swap(arr, pos, pos2):
    temp = arr[pos]  # Creates a temporary holding variable and then uses it to swap values
    arr[pos] = arr[pos2]
    arr[pos2] = temp


def leftChild(pos):  # Returns the hypothetical position of the left child
    return (2 * pos) + 1


def rightChild(pos):  # Returns the hypothetical position of the right child
    return (2 * pos) + 2


def minimum(arr, pos, pos2):  # Returns the position of the lower value of two spots in the list
    if arr[pos] < arr[pos2]:
        return pos
    else:
        return pos2


def leaf(arr, pos):  # Checks for the existence of children to determine whether the position is a leaf or not
    if (2 * pos) + 1 > len(arr) - 1 and (2 * pos) + 2 > len(arr) - 1:
        return True
    return False


i = 0
initial = []
while sys.argv[i + 1] != 'A' and sys.argv[i + 1] != 'R':
    i += 1
    initial.append(int(sys.argv[i]))
print("Initial list: ", initial)
heapify(initial, int((len(initial) - 1) / 2) - 1)
print("Heapified list: ", initial)
while i <= len(sys.argv) - 1:
    if sys.argv[i] == 'A':
        heappush(initial, int(sys.argv[i + 1]))
        print("Added", int(sys.argv[i + 1]), "to heap: ", initial)
    elif sys.argv[i] == 'R':
        popped = heappop(initial)
        print("Popped", popped, "from heap: ", initial)
    i += 1
