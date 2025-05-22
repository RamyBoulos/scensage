from annotator import analyze_scene

# Use a short scene transcript for testing
test_transcript = """
Greetings, my friend. We are all interested in the future,
for that is where you and I are going to spend the rest of our lives.
"""

# Call the analyzer
result = analyze_scene(test_transcript)

# Print the results
print("LLM Annotation Output:")
print(result)