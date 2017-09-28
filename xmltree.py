import xml.etree.ElementTree as ET

tree = ET.parse('youtubeComments.xml')
root = tree.getroot()
total_utterances = 0
for head in root:
	total_utterances += len(head)

avg_utterances = total_utterances / len(root)
print('average number of utterances per dialogue: {} avg_utterances'.format(avg_utterances))

total_words = 0
size = 0
sentences = 0
for head in root:
	sentences += len(head)
	for child in head:
		total_words += len(child.text)
		size += 1



avg_words = total_words / size
print('average number of words per utterance: {} avg_words'.format(avg_words))

print(sentences)
print(total_utterances)
