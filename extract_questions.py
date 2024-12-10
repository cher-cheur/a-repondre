import json
import os
from pathlib import Path
from collections import Counter

def extract_questions_from_json(json_file):
    """Extract all questions from a JSON response file."""
    questions = []
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Get questions from main related_questions
        if 'related_questions' in data:
            for qa in data['related_questions']:
                questions.append(qa['question'])
                # Check for nested related questions
                if 'related_questions' in qa:
                    for nested_qa in qa['related_questions']:
                        questions.append(nested_qa['question'])
    except Exception as e:
        print(f"Error processing {json_file}: {str(e)}")
    
    return questions

def main():
    # Get the data directory path
    data_dir = Path(__file__).parent / 'data'
    
    # Store all questions (including duplicates)
    all_questions = []
    
    # Process all JSON files in the data directory
    for json_file in data_dir.glob('*.json'):
        questions = extract_questions_from_json(json_file)
        all_questions.extend(questions)
    
    # Count total questions (including duplicates)
    print(f"\nTotal number of questions found (including duplicates): {len(all_questions)}")
    
    # Count unique questions and their frequencies
    question_counter = Counter(all_questions)
    unique_questions = list(question_counter.keys())
    
    print(f"Number of unique questions: {len(unique_questions)}\n")
    
    # Print all questions with their counts
    print("Questions and their frequencies:")
    print("-" * 50)
    for question, count in question_counter.most_common():
        print(f"[{count}x] {question}")
    
    # Save detailed results to output file
    output_file = Path(__file__).parent / 'questions_analysis.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Total questions found: {len(all_questions)}\n")
        f.write(f"Unique questions: {len(unique_questions)}\n\n")
        f.write("Questions and their frequencies:\n")
        f.write("-" * 50 + "\n")
        for question, count in question_counter.most_common():
            f.write(f"[{count}x] {question}\n")
    
    print(f"\nDetailed analysis saved to {output_file}")

if __name__ == '__main__':
    main()
