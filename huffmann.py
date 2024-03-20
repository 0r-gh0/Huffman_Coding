import heapq
from collections import defaultdict
import traceback

file_path = 'D2.txt'
output_file_path = 'encode.bin'

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_huffman_codes(root, current_code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
        return
    generate_huffman_codes(root.left, current_code + '0', codes)
    generate_huffman_codes(root.right, current_code + '1', codes)

def huffman_encoding(frequencies):
    root = build_huffman_tree(frequencies)
    codes = {}
    generate_huffman_codes(root, '', codes)
    return codes

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
    
    encoded_text = ''.join(huffman_codes[byte] for byte in binary_data)

    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding

    with open(output_file_path, 'wb') as output_file:
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            output_file.write(bytes([int(byte, 2)]))

    print(f"Encoded text written to '{output_file_path}'")

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()