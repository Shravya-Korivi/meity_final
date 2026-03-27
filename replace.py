import re
from pathlib import Path

def parse_original_file(filepath):
    """
    Parse the original Rajasthani text file
    Format: ( train_rajasthanimale_00001 " मेवाड़ी फागण " )
    Returns: dict mapping file_id to list of words
    """
    original_data = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match: ( file_id " words " )
    pattern = r'\(\s*(\S+)\s+"([^"]+)"\s*\)'
    matches = re.findall(pattern, content)
    
    for file_id, text in matches:
        # Split text into words (remove extra whitespace)
        words = text.strip().split()
        original_data[file_id] = words
    
    return original_data

def parse_sentences_file(filepath):
    """
    Parse sentences.txt file
    Format: train_rajasthanimale_00001: word1 <NSIL> word2 <LSIL>
    Returns: list of (file_id, tokens) tuples
    """
    sentences_data = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Split by first colon to separate file_id from content
        if ':' in line:
            file_id, content = line.split(':', 1)
            file_id = file_id.strip()
            
            # Split content into tokens (words and break labels)
            tokens = content.strip().split()
            
            sentences_data.append((file_id, tokens))
    
    return sentences_data

def replace_words_with_original(sentences_data, original_data):
    """
    Replace transliterated words with original Rajasthani words
    Keep break labels (<NSIL>, <LSIL>, etc.) intact
    """
    replaced_sentences = []
    
    break_labels = {'<NSIL>', '<LSIL>', '<MSIL>', '<SSIL>'}
    
    for file_id, tokens in sentences_data:
        if file_id not in original_data:
            print(f"Warning: {file_id} not found in original data, keeping as is")
            # Keep original tokens if no replacement found
            sentence = f"{file_id}: {' '.join(tokens)}"
            replaced_sentences.append(sentence)
            continue
        
        original_words = original_data[file_id]
        
        # Build new token list with original words and break labels
        new_tokens = []
        word_index = 0
        
        for token in tokens:
            if token in break_labels:
                # Keep break label as is
                new_tokens.append(token)
            else:
                # Replace with original word
                if word_index < len(original_words):
                    new_tokens.append(original_words[word_index])
                    word_index += 1
                else:
                    print(f"Warning: {file_id} has more transliterated words than original words")
                    new_tokens.append(token)  # Keep transliterated if no replacement
        
        # Check if we used all original words
        if word_index < len(original_words):
            print(f"Warning: {file_id} has fewer transliterated words than original words")
            print(f"  Original words remaining: {original_words[word_index:]}")
        
        # Create sentence
        sentence = f"{file_id}: {' '.join(new_tokens)}"
        replaced_sentences.append(sentence)
    
    return replaced_sentences

def replace_transliteration(original_file, sentences_file, output_file='sentences_original.txt'):
    """
    Main function to replace transliterated words with original text
    
    Args:
        original_file: Path to file with original Rajasthani text
        sentences_file: Path to sentences.txt with transliterated words
        output_file: Output filename for replaced sentences
    """
    print("Step 1: Parsing original Rajasthani text file...")
    original_data = parse_original_file(original_file)
    print(f"  Found {len(original_data)} entries")
    
    print("\nStep 2: Parsing sentences file...")
    sentences_data = parse_sentences_file(sentences_file)
    print(f"  Found {len(sentences_data)} sentences")
    
    print("\nStep 3: Replacing transliterated words with original text...")
    replaced_sentences = replace_words_with_original(sentences_data, original_data)
    
    print("\nStep 4: Writing output...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(replaced_sentences))
    
    print(f"\n{'='*70}")
    print("REPLACEMENT COMPLETE")
    print(f"{'='*70}")
    print(f"Input files:")
    print(f"  - Original text: {original_file}")
    print(f"  - Sentences: {sentences_file}")
    print(f"Output file: {output_file}")
    print(f"Total sentences processed: {len(replaced_sentences)}")
    
    # Show sample
    print(f"\n{'='*70}")
    print("SAMPLE OUTPUT (first 3 sentences):")
    print(f"{'='*70}")
    for i, sentence in enumerate(replaced_sentences[:3]):
        print(f"{i+1}. {sentence}\n")
    
    return replaced_sentences

if __name__ == "__main__":
    # Specify your file paths
    original_file = r"/home/speechlab/Desktop/sn try/txt.done.data"  # Change this
    sentences_file = "sentences.txt"
    output_file = "sentences_in_raj.txt"
    
    # Run replacement
    replaced = replace_transliteration(
        original_file=original_file,
        sentences_file=sentences_file,
        output_file=output_file
    )