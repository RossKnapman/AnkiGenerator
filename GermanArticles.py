import sqlite3
import csv

anki_collection = 'collection.anki2'

# Found by examining the database
# Unfortunately cannot do it by deck name, as you get the error "no such collation sequence: unicase"
deck_id = 1498107408337

# Connection object which represents database
conn = sqlite3.connect(anki_collection)
cursor = conn.execute("SELECT DISTINCT did, nid, flds FROM cards INNER JOIN notes ON notes.id = cards.nid WHERE did = " + str(deck_id))

# Set up writer
csv_file = open('articles.csv', 'w+')

for row in cursor:

    # Fields split by 0x1f
    question_field = row[2].split('\x1f')[0].split(' ')

    # Exclude sentences
    if len(question_field) == 2:
        if question_field[0].lower() == 'der' or question_field[0].lower() == 'die' or question_field[0].lower() == 'das':
            csv_file.write('{{c1::' + question_field[0].lower() + '}} ' + question_field[1] + '\n')

csv_file.close()
