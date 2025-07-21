import streamlit as st
import spacy
from spellchecker import SpellChecker

#model
nlp = spacy.load("en_core_web_sm")

#set of subject and object pronouns
subject_pronouns = {"I", "you", "he", "she", "it", "we", "they"}
object_pronouns = {"me", "you", "him", "her", "it", "us", "them"}

object_to_subject = {
    "me": "I", "you": "you", "him": "he", "her": "she", "it": "it", "us": "we", "them": "they"
}

subject_to_object = {
    "I": "me", "you": "you", "he": "him", "she": "her", "it": "it", "we": "us", "they": "them"
}

# Streamlit UI
st.set_page_config(page_title="Pronoun Grammar Checker", page_icon="📚")
st.title("Subject vs. Object Pronoun Checker")
st.markdown("Type a sentence !")

sentence = st.text_area("Enter your sentence here:")

def get_pronoun_suggestion(token):
    # Suggest the correct pronoun based on the role of the word (subject or object)
    if token.text.lower() in object_pronouns and token.dep_ in {"nsubj", "nsubjpass"}:
        # Object pronoun used in a subject position
        return object_to_subject.get(token.text.lower(), None), "Object pronoun used incorrectly"
    elif token.text.lower() in subject_pronouns and token.dep_ in {"dobj", "pobj"}:
        # Subject pronoun used in an object position
        return subject_to_object.get(token.text.lower(), None), "Subject pronoun used incorrectly"
    return None, None


spell = SpellChecker()

if st.button("Check Grammar"):
    if not sentence.strip():
        st.warning("Please enter a sentence to check.")
    else:
        doc = nlp(sentence)
        errors = []

        for token in doc:
            if token.pos_ == "PRON":
                suggestion, error_type = get_pronoun_suggestion(token)
                if suggestion:
                    errors.append((token.text, error_type, suggestion))

        # Check for basic spelling
    
        for token in doc:
            if token.is_alpha and token.text.lower() not in spell:
                errors.append((token.text, "Possibly misspelled word", spell.correction(token.text.lower())))

        if errors:
            st.error(" Issues found:")
            for word, reason, suggestion in errors:
                if suggestion:
                    st.markdown(f"- **{word}** — {reason} (Suggested: **{suggestion}**) ")
                else:
                    st.markdown(f"- **{word}** — {reason}")
        else:
            st.success("✅ No pronoun and spelling errors detected.")
