""" Text Analyzer """

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Analyzer:
    
    """
    The Analyzer class is a toolkit for mining unstructured text. This class includes methods for text data processing, cleaning, word frequency analysis and collocation.
    """
    
    # when initializing Analyzer class, provide file path to .txt file that you want to analyze
    def __init__(self, file_path):
        self.file_path = file_path
    
    
    def read_text(self):
        """" This method reads the .txt that you provide in the Analyzer initialization and stores the data as a string. """

        # open .txt document
        f= open(self.file_path,"r")
        contents =f.read()

        return contents
    
    
    def make_lowercase(self, word_list):
        """
        Helper function that sets every word in a given list of strings to lowercase
        
        INPUT:
            word_list: a list of strings
        
        OUTPUT:
            list of lowercase strings
        """

        i = 0
        for item in word_list:

            # make lowercase   
            word_list[i] = item.lower()

            # next iteration
            i += 1

        return word_list


    def remove_punc(self, word_list):
        """
        Helper function that removes punctuation from each word in a string list
        
        INPUT:
            word_list: a list of strings
        
        OUTPUT:
            list with punctuation removed from each string
        """

        i = 0 
        for word in word_list:

            # remove unneccesary characters
            char_to_remove = (',','.',';',':','(',')','!'," ",'"','&')
            for char in char_to_remove:
                word = word.replace(char, "")

            # update list
            word_list[i] = word

            # next iteration
            i += 1

        return word_list


    def remove_common_words(self, word_list):
        """
        Helper function that removes common words from a list.
        Removes words such as: 'the', 'like', 'an' etc.
        
        INPUT:
            word_list: a list of strings
        
        OUTPUT:
            new list that does not contain common words
        """

        final_set = []
        # remove generic words
        for item in word_list:
            
            # remove blank spaces
            if " " in item:
                item = item.replace(" ", "")

            words_to_disregard = ('the','their','there','that','and','of',
                                  'to','a','in','this','it','be','we','is',
                                  'as','have','--','they','i','on','will',
                                  'our', 'are','for','he','who','has',
                                  'than','but','what','from','by','was',
                                  'if','at','or','so','when','with','you',
                                  'not',"it's",'his','an','those','an','me',
                                  'my','can','get','going','us','your','no',
                                  'been','over','into','every','these','did',
                                  'also','were','any','like','then','while',
                                  'because','here','had','its','more','most',
                                  'â€”','do','am','all','do',"i'm",'which',
                                  'her','them','being', " ", "")
            
            if item in words_to_disregard:
                pass
            else:
                final_set.append(item)

        return final_set


    def word_count(self):

        """
        This method parses the object's .txt file into a list of words,
        removes punctuation and common words, then produces a word count Series.

        INPUT:
            file_name: string containing file path to .txt file you want to analyze

        OUTPUT:
            Series containing value counts for each unique word in text

        """

        # read .txt file
        contents = self.read_text()

        # create parsed list of all words
        parsed_words = contents.split()

        # make all words lowercase
        parsed_words = self.make_lowercase(parsed_words)

        # remove punctuation
        parsed_words = self.remove_punc(parsed_words)

        # remove common words
        parsed_words = self.remove_common_words(parsed_words)

        # create value counts Series
        df = pd.Series(parsed_words).value_counts()

        return df
    
    
    def collocate(self, words_in_phrase):
        
        """
        This method parses the object's .txt file into a list of words,
        removes punctuation and common words, then returns a Series containing a collocated phrase count.

        INPUT:
            words_in_phrase: integer value that determines the number of words in each phrase (either 2 or 3)

        OUTPUT:
            Series containing value counts for each unique word in text

        """
        
        # read .txt file
        contents = self.read_text()

        # create parsed list of all words
        parsed_words = contents.split()

        # make all words lowercase
        parsed_words = self.make_lowercase(parsed_words)

        # remove punctuation
        parsed_words = self.remove_punc(parsed_words)
        
        # remove common words
        parsed_words = self.remove_common_words(parsed_words)
        
        # two-word phrases
        if words_in_phrase == 2:
            
            phrases = []
            i = 0
            for word in parsed_words:

                try:
                    word1 = parsed_words[i]
                    word2 = parsed_words[i + 1]
                    phrases.append((word1, word2))
                    i+=1
                except:
                    pass
        
        # three-word phrases
        elif words_in_phrase == 3:
            
            phrases = []
            i = 0
            for word in parsed_words:

                try:
                    word1 = parsed_words[i]
                    word2 = parsed_words[i + 1]
                    word3 = parsed_words[i + 2]
                    phrases.append((word1, word2, word3))
                    i+=1
                except:
                    pass

        return pd.Series(phrases).value_counts()
    
    
    
    """ 
    Visualization Methods
    
    """
    
    def visual_word_count(self):
        
        """
        Visualize word_count data

        OUTPUT:
            Seaborn bar plot displaying top 10 most common words

        """
        
        # category value counts
        category_value_counts = self.word_count().head(10)

        # create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))

        # barplot for category value counts
        plot = sns.barplot(x=list(category_value_counts),
                         y=category_value_counts.index,
                         palette="Blues_d")

        # set labels
        set_labels = plot.set(title='Top 10 most common words',xlabel="Word Count", ylabel = "Word")
        
        
    def visual_collocate(self, words_in_phrase):
        
        """
        Visualize word_count data
        
        INPUT:
            words_in_phrase: integer value that determines the number of words in each phrase (either 2 or 3)

        OUTPUT:
            Seaborn bar plot displaying top 10 phrases

        """
        
        # category value counts
        category_value_counts = self.collocate(words_in_phrase).head(10)

        # create labels
        new_labels = []

        for words_tuple in list(category_value_counts.index):

            combined_str = words_tuple[0]

            for item in words_tuple[1:]:
                combined_str = combined_str + ", " + item

            new_labels.append(combined_str)

        # create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))

        # barplot for category value counts
        plot = sns.barplot(x=list(category_value_counts),
                         y=new_labels,
                         palette="Blues_d")

        # set labels
        set_labels = plot.set(title='Top 10 most common phrases', xlabel="Word Count", ylabel = "Phrase")