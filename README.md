# AnkiGenerator

Takes in a list of words I don't know from books read in a foreign language (generated from my highlights on my Kindle), looks them up on Linguee (for phrases) or DeepL (for single words), and outputs pairs which can be exported into my Anki decks. Code is kind of messy but works (provided I keep it up-to-date with DeepL's changing HTML). N.B. I wrote this before DeepL released their API.

To Do:
- Implement unit testing (that is called on a schedule)
- Combine `GermanSingleWords.py` and `FrenchSingleWords.py` into a single file
