from pynlpl.formats import folia # version -> 1.2.5
import re
import sys

# Input folia.xml file
folia_filename_full_path = sys.argv[1]

# Class lists
trigger_list = ["etype", "emention"]
tsemantic_type_list = ["demonst", "ind_act", "group_clash", "arm_mil", "elec_pol", "other"]
psemantic_type_list = ["peasant", "worker", "producer", "employer", "professional", "student", "people", "activist", "politician", "militant", "ps_other"]
osemantic_type_list = ["pol_party", "ngo", "trade_union", "arm_org", "chamber_profs", "os_other"]
fname_list = ["loc", "fname"]
actor_list = ["pname", "name", "type"]
other_class_list = ["place", "etime"]

# Alpha-numerical sorting
def sorted_nicely(l):
	# Copied from this post -> https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
	def convert(text): return int(text) if text.isdigit() else text
	def alphanum_key(key): return [convert(c) for c in re.split('([0-9]+)', key)]

	return sorted(l, key=alphanum_key)

def nonrelative_or_negative(doc):
	if ("RelevantCountry" in doc.metadata.order and doc.metadata["RelevantCountry"] == "No") or ("Event" in doc.metadata.order and doc.metadata["Event"] == "No"):
		return True
	return False

# returns events which the entity belongs to
def get_current_events(entity):
	comment = "event1"

	# If the last element of entity is a comment.
	# TODO: Check for a function like entity.hasComment()
	if type(entity[-1]) == folia.Comment:
		comment = entity[-1].value
		comment = comment.lower().strip().replace(" ", "")
		if comment == "":
			comment = "event1"

	curr_events = sorted_nicely(re.split(",|\n", comment)) # returns a list
	if len(curr_events) > 1: # multi-event
		pass

	return curr_events

def get_word_indexes(word_ids):
	return [int(re.search("w\.(\d+)$", word_id).group(1)) - 1 for word_id in word_ids]

def is_continuous(a_list):
	if len(a_list) <= 1:
		return True

	for x, y in zip(a_list, a_list[1:]):
		if y - x != 1:
			return False

	return True

if __name__ == "__main__":
	doc = folia.Document(file=folia_filename_full_path)

	if not nonrelative_or_negative(doc):
		sentences = []
		sent_idx = 0
		events = {}


		for paragraph in doc.paragraphs():
			for sentence in paragraph.sentences():
				curr_words = [word.text() for word in sentence.words()]
				sentences.append(curr_words)

				for layer in sentence.select(folia.EntitiesLayer):
					for entity in layer.select(folia.Entity):
						# You can do different stuff with semantic types or arguments if you like.
						if entity.cls in trigger_list:
							pass
						elif entity.cls in tsemantic_type_list:
							pass
						elif entity.cls in psemantic_type_list:
							pass
						elif entity.cls in osemantic_type_list:
							pass
						elif entity.cls in fname_list:
							pass
						elif entity.cls in actor_list:
							pass
						elif entity.cls in other_class_list:
							pass
						else:
							continue

						# For all classes
						entity_word_ids = sorted_nicely([word.id for word in entity.wrefs()])
						entity_word_idxs = get_word_indexes(entity_word_ids)
						if not is_continuous(entity_word_idxs):
							print("This annotation is not continuous")
							print(entity_word_ids)
							continue

						curr_events = get_current_events(entity)
						for event in curr_events:
							# an example entry is -> ["trigger", (0, 5, 5)] -> (sentence id, starting word id, inclusive ending word id)
							events.setdefault(event, []).append([entity.cls, (sent_idx, entity_word_idxs[0], entity_word_idxs[-1])])


				sent_idx += 1

	else:
		print("Sorry, this article does not contain any protest that is relative to the source country.")

	print(sentences)
	print(events)
