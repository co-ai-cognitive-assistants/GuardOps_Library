from tqdm import tqdm
from evaluation.BaseEvaluationFramework import BaseEvaluationFramework
from evaluation.evaluation import Evaluation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as pairwise_cosine_similarity
from spacy.lang.en.stop_words import STOP_WORDS
from rouge import Rouge
import spacy
from typing import List, Set, Union, Dict
from bert_score import score as bert_score
from jinja2 import Template
import pandas as pd
import numpy as np
from transformers import logging
logging.set_verbosity_error()
from summac.model_summac import SummaCZS, SummaCConv
import time

class SUMEvalFramework(BaseEvaluationFramework):
    def __init__(self, device='cpu') -> None:
        self.nlp = spacy.load("de_core_news_sm")
        super().__init__()
        self.eval_details = []
        self.eval_total = {}
        self.prompt_template = """Erstelle eine umfassende Zusammenfassung des nachstehenden Textes.\n
        Die Zusammenfassung sollte alle wichtigen Punkte und Hauptgedanken des Originaltextes abdecken\n 
        und gleichzeitig die Informationen in einem prägnanten und leicht verständlichen Format zusammenfassen.\n
        Achten  darauf, dass die Zusammenfassung relevante Details und Beispiele enthält,\n
        die die Hauptgedanken unterstützen, und vermeide unnötige Informationen oder Wiederholungen.\n
        Die Länge der Zusammenfassung sollte der Länge und Komplexität des Originaltextes angemessen sein\n
        und einen klaren und genauen Überblick geben, ohne wichtige Informationen auszulassen.\n\n
        Originaltext:\n
        {{input}}"""
        self.device = device

    def evaluate(self, model, dataset, eval_name, **kwargs):
        evaluation = Evaluation(name=eval_name, framework=self.__class__.__name__)
        custom_prompt = kwargs.get('custom_prompt_template',None)

        if custom_prompt:
            self.prompt_template = custom_prompt
        # Calculate runtime for evaluation
        start_time = time.time() 
                
        ## Generate Summaries add tqdm:
        with tqdm(total=len(dataset), desc="Generating Evaluation") as progress_bar:
            for index,row in dataset.iterrows():
                tmp_row = {}
                original_text = row["text"]
                # Create prompt
                prompt = self.create_prompt(original_text)
                generated_text = model.predict(input_text=prompt)
                tmp_row["original_text"] = original_text
                tmp_row["generated_text"] = generated_text
                tmp_row['prompt'] = self.prompt_template
                # Calculate New Words in Summary
                tmp_row["new_words_in_summary"] = list(self.new_words_in_summary(original_text, generated_text))
                # Calculate Word Overlap
                tmp_row["word_overlap"] = self.word_overlap(original_text, generated_text)
                # Number of New Words in Summary
                tmp_row["number_of_new_words_in_summary"] = len(tmp_row["new_words_in_summary"])
                # Word Count of Orignal and Generated Text
                tmp_row["word_count_original"] = len(original_text.split())
                tmp_row["word_count_generated"] = len(generated_text.split())
                tmp_row["word_count_difference"] = tmp_row["word_count_original"] - tmp_row["word_count_generated"]
                # Calculate Jacard Similarity
                words_original = self.process_text(original_text)
                words_summary = self.process_text(generated_text)
                tmp_row["jaccard_similarity"] = self.jaccard_similarity(words_original, words_summary)
                # Calculate Cosine Similarity
                tmp_row["cosine_similarity"] = self.cosine_similarity_tf_idf(original_text, generated_text)
                # Calculate BERTScore
                tmp_row["bert_p1"], tmp_row["bert_r1"], tmp_row["bert_f1"] = self.calculate_bert_score(generated_text, original_text)
                # Calculate Rouge at split the values of the dict to tmp_row
                bert_scores = self.calculate_rouge_c(generated_text, original_text)
                tmp_row.update(bert_scores)
                # Calculate SummaC
                tmp_row["summac_zs"], tmp_row["summac_conv"] = self.summac_calculator(original_text, generated_text)
                

                self.eval_details.append(tmp_row)
                progress_bar.update(1)
        
        # Calculate mean, min, max, std for word_count_difference
        word_count_difference = [row["word_count_difference"] for row in self.eval_details]
        
        min_dif = float(np.min(word_count_difference))
        max_dif = float(np.max(word_count_difference))
        std_dif = float(np.std(word_count_difference))

        self.eval_total["word_count_difference_min"] = min_dif
        self.eval_total["word_count_difference_max"] = max_dif
        self.eval_total["word_count_difference_std"] = std_dif

        # Emd time calculation
        end_time = time.time()  # Step 3: Capture end time
        runtime_seconds = end_time - start_time 

        # Consolidate all figures of the dictionary to mean values and add to eval_total
        # only if value of key is a number (float or int)
        with tqdm(total=len(self.eval_details), desc="Consolidating Evaluation") as progress_bar:
            for key in self.eval_details[0].keys():
                if isinstance(self.eval_details[0][key], (float, int)):
                    self.eval_total[key] = sum(d[key] for d in self.eval_details) / len(self.eval_details)
                progress_bar.update(1) 

        total_tests = len(self.eval_details)

        ## Standard return
        evaluation.data = {'total_score': self.eval_total['summac_conv'], 'runtime': runtime_seconds, 'total_tests': total_tests,  'scores': self.eval_total, 'details': self.eval_details}
        return evaluation

    def get_details(self):
        # return as pandas dataframe
        return pd.DataFrame(self.eval_details)
    
    def get_total(self):
        # return as pandas dataframe
        return pd.DataFrame(self.eval_total, index=[0])

    def help(self):
        explanation = """
        **New Words in Summary**: Measures the number of unique words in the summary that are not present in the original text. Ideally, this figure should be low, as a good summary should primarily consist of key terms from the original text. High values may indicate the summary is introducing irrelevant or new content.

        **Word Overlap**:" This metric calculates the overlap in words between the original text and the summary. A higher overlap is generally better, as it suggests the summary effectively captures the main terms and concepts from the original text.

        **Number of New Words in Summary**: Similar to 'New Words in Summary', but quantifies the count. A lower number is preferable, indicating that the summary is closely aligned with the original content.

        **Word Count of Original and Generated Text**: These metrics compare the length of the original text with the summary. Ideally, the summary should be significantly shorter than the original text while still capturing the main points, indicating efficiency in summarization.

        **Word Count Difference**: Reflects the difference in word count between the original text and the summary. A larger difference (without loss of key content) is typically better, as it indicates a more concise summary.

        **Jaccard Similarity**: Measures the similarity between the sets of unique words in the original text and the summary. Higher values are better, as they indicate a greater overlap in content, suggesting that the summary is representative of the original text.

        **Cosine Similarity (TF-IDF)**: Uses TF-IDF to compute the cosine similarity between the original text and the summary. Higher values are preferable, as they suggest that the summary and the original text are similar in terms of content and meaning.

        **BERTScore**: Evaluates the semantic similarity between the summary and the original text using BERT embeddings. Higher scores (precision, recall, F1) are desirable, indicating a summary that closely matches the semantics of the original text.

        **ROUGE Scores**: Include ROUGE-1, ROUGE-2, and ROUGE-L, measuring the overlap of unigrams, bigrams, and the longest common subsequence, respectively, between the summary and the original text. Higher scores are better, indicating more effective capturing of the content and structure of the original text.

        **SummaC**: Based on the paeper "SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization" (https://paperswithcode.com/paper/summac-re-visiting-nli-based-models-for). SummaC is a metric that measures the consistency between the summary and the original text. Higher values are better, as they indicate that the summary is consistent with the original text.
        **SummaCZS**:The SummaCzs metric is a measure of summary consistency proposed by Laban et al. (2021). It is defined as:
            Pass sentence pairs from the document (D) and summary (S) through an NLI model to generate an M x N entailment score matrix E, where M is the number of document sentences and N is the number of summary sentences. Eij refers to the entailment score between the ith document sentence and jth summary sentence.
            Take the maximum entailment score for each summary sentence by column: max(E, axis='col')[j] = max(Ei1, Ei2,..., EiM)
            This produces a 1 x N vector containing the maximum entailment score for each summary sentence.
            Take the mean of this 1 x N vector to produce the final scalar SummaCzs consistency score.
            A higher SummaCzs score indicates greater predicted consistency between the document and summary. The maximum value of 1.0 indicates the model predicts the summary is fully entailed by the document, while lower values indicate more inconsistency detected.
            The limitation of SummaCzs is its reliance on only the maximum entailment scores, rather than the full distribution of scores for each summary sentence.

        **SummaCConv**:The SummaCConv metric is a measure of summary consistency proposed by Laban et al. (2021) that addresses limitations with SummaCzs. It is defined as:
            Same first step as SummaCzs - pass sentence pairs from the document (D) and summary (S) through an NLI model to generate an M x N entailment score matrix E.
            Bin the scores for each summary sentence into H histograms, each with Prob(score is in bin h). This captures the distribution of entailment scores from the document sentences for each summary sentence.
            Pass the H x N binned score matrix through a 1D convolution layer to compile the score distributions for each summary sentence into N scalar scores, one per summary sentence.
            Take the mean of the N summary sentence scores to produce the final scalar SummaCConv consistency score.
            As with SummaCzs, a higher SummaCConv score indicates greater predicted consistency between the document and summary. The convolution layer addresses limitations with SummaCzs by considering the full distribution of entailment scores rather than just maximum values.
            The convolution layer parameters are trained on a dataset of document-summary pairs labeled as consistent or inconsistent to learn effective compilation of the per-sentence score distributions.

        **ToDo**: Further Implementation possible https://arxiv.org/abs/2103.12693
                    https://eugeneyan.com/writing/abstractive/
                    """
        formatted_lines = [line.lstrip() for line in explanation.split('\n')]
        return '\n'.join(formatted_lines)
    
    ## Helper functions

    def create_prompt(self, input : str):
        template = Template(self.prompt_template)
        return template.render(input=input)


    def calculate_bert_score(self, summary: str, document: str):
        """
        Calculates BERTScore comparing a summary with the source document.

        Args:
            summary (str): The generated summary text.
            document (str): The original source document text.

        Returns:
            dict: A dictionary with precision, recall, and F1 BERTScore.
        """
        P, R, F1 = bert_score([summary], [document], lang="en", rescale_with_baseline=True)
        return P.item(), R.item(), F1.item()
    def calculate_rouge_c(self, summary: str, document: str):
        """
        Calculates ROUGE scores comparing a summary with the source document.

        Args:
            summary (str): The generated summary text.
            document (str): The original source document text.

        Returns:
            dict: A dictionary containing ROUGE-1, ROUGE-2, and ROUGE-L scores.
        """
        rouge = Rouge()
        scores = rouge.get_scores(summary, document)
        flattened_dict = {f"{outer_key}_{inner_key}": value 
                  for outer_key, inner_dict in scores[0].items() 
                  for inner_key, value in inner_dict.items()}
        return flattened_dict


    def cosine_similarity_tf_idf(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts using TF-IDF.

        Args:
        - text1 (str): First text.
        - text2 (str): Second text.

        Returns:
        - float: Cosine similarity score.
        """
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        return pairwise_cosine_similarity(vectors)[0][1]

    def process_text(self, text: str) -> Set[str]:
        """
        Process a given text, tokenizing, lemmatizing, and extracting named entities.

        Args:
        - text (str): Text to be processed.

        Returns:
        - Set[str]: A set of processed words and named entities.
        """
        # Process the text using spaCy
        doc = self.nlp(text)

        # Extract words and named entities
        words = {
            token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha
        }
        named_entities = {ent.text.lower() for ent in doc.ents}

        # Combine words and named entities
        return words.union(named_entities)
    
    def jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """
        Calculate Jaccard Similarity between two sets.

        Args:
        - set1 (Set[str]): First set.
        - set2 (Set[str]): Second set.

        Returns:
        - float: Jaccard similarity score.
        """
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    def word_overlap(self, text1: str, text2: str) -> float:
        """
        Compute the word overlap between two texts.

        Args:
        - text1 (str): First text.
        - text2 (str): Second text.

        Returns:
        - float: Overlap ratio.
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        overlap = words1.intersection(words2)
        return len(overlap) / (len(words1) + len(words2) - len(overlap))

    def new_words_in_summary(self, original_text: str, summary: str) -> Set[str]:
        """
        Identify new words present in the summary that were not in the original text.

        Args:
        - original_text (str): Original text.
        - summary (str): Generated summary.

        Returns:
        - set: Set of new words in the summary.
        """
        nlp = spacy.load("de_core_news_sm")
        original_words = set(
            self.filter_words([token.text for token in nlp(original_text.lower())])
        )
        summary_words = set(self.filter_words([token.text for token in nlp(summary.lower())]))

        # Find the new words in the summary
        new_words = summary_words - original_words
        return new_words


    def filter_words(self, word_list: List[str]) -> Set[str]:
        """
        Filters out stop words, numbers, and short words from a list of words.

        Args:
        - word_list (List[str]): List of words.

        Returns:
        - Set[str]: Filtered set of words.
        """
        return {
            word
            for word in word_list
            if word not in STOP_WORDS and word.isalpha() and len(word) > 2
        }

    def summac_calculator(self, document: str, summary: str):
        """
        Calculates SummaC scores comparing a summary with the source document.
        
        Args:
            document (str): The original source document text.
            summary (str): The generated summary text.
        
        Returns:
            score_zs1 (float): SummaCZS score.
            score_conv1 (float): SummaCConv score.

        Citation: https://github.com/tingofurro/summac
        """
        model_zs = SummaCZS(granularity="sentence", model_name="vitc", device=self.device) # If you have a GPU: switch to: device="cuda"
        model_conv = SummaCConv(models=["vitc"], bins='percentile', granularity="sentence", nli_labels="e", device=self.device, start_file="default", agg="mean")
        score_zs1 = model_zs.score([document], [summary])
        score_conv1 = model_conv.score([document], [summary])

        return score_zs1["scores"][0], score_conv1["scores"][0]