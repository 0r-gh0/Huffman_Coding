import heapq # Importing heapq module for heap operations
from collections import defaultdict # Importing defaultdict for convenient initialization of dictionary
import traceback # Importing traceback module to print detailed error information

file_path = 'D2.txt' # Your File name here
output_file_path = 'encode.bin' # Update the file path for the encoded output file

class Node:
    def __init__(self, char, freq):
        self.char = char # Character stored in the node
        self.freq = freq # Frequency of the character
        self.left = None # Pointer to the left child node
        self.right = None # Pointer to the right child node

    def __lt__(self, other):
        return self.freq < other.freq # Comparison method for heap ordering

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()] # Creating a list of nodes from character frequencies
    heapq.heapify(heap) # Heapifying the list
    
    while len(heap) > 1: # While there are more than one node in the heap
        left = heapq.heappop(heap) # Pop the smallest node
        right = heapq.heappop(heap) # Pop the second smallest node
        merged = Node(None, left.freq + right.freq) # Create a merged node with the sum of frequencies
        merged.left = left # Assign left node as left child
        merged.right = right # Assign right node as right child
        heapq.heappush(heap, merged) # Push the merged node back to the heap
    
    return heap[0] # Return the root node of the Huffman tree

def generate_huffman_codes(root, current_code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code # Assign Huffman code to character
        return
    generate_huffman_codes(root.left, current_code + '0', codes)
    generate_huffman_codes(root.right, current_code + '1', codes)

def huffman_encoding(frequencies):
    root = build_huffman_tree(frequencies) # Build Huffman tree
    codes = {} # Dictionary to store Huffman codes
    generate_huffman_codes(root, '', codes) # Generate Huffman codes
    return codes # Return the Huffman codes dictionary

try:
    with open(file_path, 'rb') as file:
        binary_data = file.read()
        
        character_count = defaultdict(int)
        for byte in binary_data:
            character_count[byte] += 1
        
        sorted_character_count = dict(sorted(character_count.items(), key=lambda item: item[1], reverse=True))
        for char, count in sorted_character_count.items():
            print(f"Byte '{char}': {count} appearances")

    print("\nHuffman Encoding :")
    huffman_codes = huffman_encoding(sorted_character_count)
    for char, code in huffman_codes.items():
        print(f"Byte '{char}': Huffman Code '{code}'")
    
    # Encode the text using Huffman codes
    encoded_text = ''.join(huffman_codes[byte] for byte in binary_data)

    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding

    # Write the encoded text to the output file
    with open(output_file_path, 'wb') as output_file:
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            output_file.write(bytes([int(byte, 2)]))

    print(f"Encoded text written to '{output_file_path}'")

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc() # Print detailed error traceback