import pandas as pd
import ast
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import csv


"""
Below are a set of options to set. All of them need to be set before the script will run correctly
LAST_FM_RAW: Raw Last.fm data
LAST_FM_CLEAN: Full Last.fm data with clean tags
LAST_FM_CLEAN_TAGS: Last.fm with clean tags (Top 50 most common). Will have empty transactions
LAST_FM_CLEAN_REDUCED: Last.fm with clean tags (Top 50 most common). No empty transactions

DIRTY_TAGS: Dirty tags file. Needs to have .pkl extension
CLEAN_TAGS: Clean tags fils. Needs to have .pkl extension

CREATE_DIRTY_TAGS: Set to True if DIRTY_TAGS file does not exist or you want to replace it. Otherwise False
CREATE_CLEAN_TAGS: Set to True if CLEAN_TAGS file does not exist or you want to replace it. Otherwise False
"""
# Set the options here
LAST_FM_RAW = "../unsynced-data/lastfm.csv"
LAST_FM_CLEAN = "../unsynced-data/lastfm-clean.csv"
LAST_FM_CLEAN_TAGS = "../unsynced-data/lastfm-clean-tags.csv"
LAST_FM_CLEAN_REDUCED = "../unsynced-data/lastfm-clean-tags-reduced.csv"

DIRTY_TAGS = "../unsynced-data/dirty-tag-list.pkl"
CLEAN_TAGS = "../unsynced-data/clean-tag-list.pkl"

CREATE_DIRTY_TAGS = False
CREATE_CLEAN_TAGS = False

if CREATE_DIRTY_TAGS:
    print("Creating dirty tags file...")
    df = pd.read_csv(LAST_FM_RAW, index_col=0)
    lfm_tags = df["lfm_tags"]

    full_tag_list = []
    for entry in df["lfm_tags"]:
        entry_list = ast.literal_eval(entry)
        entry_list = [n.strip() for n in entry_list]
        full_tag_list.append(entry_list)

    with open(DIRTY_TAGS, "wb") as f:
        pickle.dump(full_tag_list, f)
    print("Dirty tags file created!")


if CREATE_CLEAN_TAGS:
    print("Creating clean tags file...")
    with open(DIRTY_TAGS, "rb") as f:
        full_tag_list = pickle.load(f)

    """
    This code was decided on through an iterative process of plotting and deciding which keys to get delete. Any tags 
    based on subjectivity or a vague genre like "rock" (e.g. What kind of rock?) were deleted. Below there are tags that
    seemed to be duplicates of others. For example, male vocalist and male vocalists are the same thing.
    """
    for idx, _ in enumerate(full_tag_list):
        # Delete tags
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "rock"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "favorites"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Favourites"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "seen live"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Favorite"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Favourite"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "favourite"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Favourite Songs"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "favorite songs"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Awesome"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "catchy"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "beautiful"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "cool"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "loved"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "guitar"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "fun"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Soundtrack"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "alternative"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "dance"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "party"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "sexy"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "happy"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "sad"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "amazing"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "piano"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "cover"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "melancholy"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "classic"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Mellow"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "relax"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "relaxing"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "heard on Pandora"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "american"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "british"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "easy listening"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "epic"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "good"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "upbeat"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Love"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "romantic"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "melancholic"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "chill"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "chillout"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "down"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "downtempo"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "USA"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "UK"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "drjazzmrfunkmusic"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Love it"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "indie"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "summer"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "german"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "lounge"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "britpop"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "rock n roll"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "great"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "nice"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "smooth"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "oldies"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "world"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "sweet"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "77davez-all-tracks"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Progressive"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "dark"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "love songs"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "memories"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "live"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "best"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "Dreamy"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "love at first listen"]
        full_tag_list[idx] = [i for i in full_tag_list[idx] if i != "FUCKING AWESOME"]

        # Edit, merge, and modify
        full_tag_list[idx] = ["RNB" if i == "rnb" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["electronic" if i.lower() == "electronica" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["electronic" if i.lower() == "electro" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["female vocalist" if i.lower() == "female vocalists" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["female vocalist" if i.lower() == "female" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["female vocalist" if i.lower() == "female vocals" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["male vocalist" if i.lower() == "male vocalists" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["psychedelic" if i.lower() == "trance" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["hip hop" if i == "Hip-Hop" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["metal" if i == "death metal" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["metal" if i == "heavy metal" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["00s" if i == "2000s" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["funk" if i == "funky" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["ambient" if i == "atmospheric" else i for i in full_tag_list[idx]]
        full_tag_list[idx] = ["blues" if i == "rhythm and blues" else i for i in full_tag_list[idx]]

    with open(CLEAN_TAGS, "wb") as f:
        pickle.dump(full_tag_list, f)

    print("Clean tags file created!")

print("Creating cleaned dataframes")
with open(CLEAN_TAGS, "rb") as f:
    full_tag_list = pickle.load(f)

# Create a flattened list of all the tags
flatlist = [item for sublist in full_tag_list for item in sublist]

# Count the occurrences of each tag
counts = dict(Counter(flatlist))
reduced_counts = counts.copy()

low_limit = 6562  # Chosen through trial and error so that the below for look will produce a total of 50 keys to keep
for key, value in counts.items():
    if value < low_limit:
            del reduced_counts[key]

# Create a list of the keys to keep and iterate through, deleting any keys that are not in that list
keys = list(reduced_counts.keys())
reduced_tag_list = full_tag_list.copy()
for idx, _ in enumerate(full_tag_list):
    reduced_tag_list[idx] = [i for i in full_tag_list[idx] if i in keys]
    reduced_tag_list[idx] = list(set(reduced_tag_list[idx]))

df = pd.read_csv(LAST_FM_RAW)
df["lfm_tags"] = pd.Series(reduced_tag_list)
df.to_csv(LAST_FM_CLEAN)

# Remove empty transactions from the reduced_tag_list
shrunk_reduced_tag_list = [i for i in reduced_tag_list if len(i) > 0]

# Write to files
with open(LAST_FM_CLEAN_TAGS, "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(reduced_tag_list)
with open(LAST_FM_CLEAN_REDUCED, "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(shrunk_reduced_tag_list)


print("Creating plots of dirty and cleaned data file")
with open(DIRTY_TAGS, "rb") as f:
    dirty_tag_list = pickle.load(f)

# Create a flattened list of all the tags
dirty_flat = [item for sublist in dirty_tag_list for item in sublist]

# Count the occurrences of each tag
dirty_counts = dict(Counter(dirty_flat))
dirty_reduced = dirty_counts.copy()

low_limit = 14500  # Chosen through trial and error so that the below for look will produce a total of 50 keys to keep
for key, value in dirty_counts.items():
    if value < low_limit:
            del dirty_reduced[key]

# Create a list of the keys to keep and iterate through, deleting any keys that are not in that list
dirty_keys = list(dirty_reduced.keys())
dirty_reduced_tag_list = dirty_tag_list.copy()
for idx, _ in enumerate(full_tag_list):
    dirty_reduced_tag_list[idx] = [i for i in dirty_tag_list[idx] if i in dirty_keys]
    dirty_reduced_tag_list[idx] = list(set(dirty_reduced_tag_list[idx]))


vals = [dirty_reduced[k] for k in dirty_keys]
sns.barplot(x=dirty_keys, y=vals)
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
plt.title("50 Most Common Last.Fm Tags (Raw)")
plt.xlabel("Last.Fm Tags")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

vals = [reduced_counts[k] for k in keys]
sns.barplot(x=keys, y=vals)
plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
plt.title("50 Most Common Last.Fm Tags (Cleaned)")
plt.xlabel("Last.Fm Tags")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
