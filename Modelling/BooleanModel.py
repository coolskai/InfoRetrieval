__original_author__ = 'Michael Aquilina'
__modify__ = 'bksun'
__email__ = 'michaelaquilina@gmail.com'
__version__ = '0.5.0'
__github__ = 'https://github.com/MichaelAquilina/hashedindex'
__name__ = 'booleanmodel'
import collections

DOCUMENT_DOES_NOT_EXIST = 'The specified document does not exist'
TERM_DOES_NOT_EXIST = 'The specified term does not exist'


class BooleanModel:
    """
    BooleanModel structure in the form of a hash list implementation.
    """

    def __init__(self, initial_terms=None):
        """
        Construct a new HashedIndex. An optional list of initial terms
        may be passed which will be automatically added to the new HashedIndex.
        """
        self._documents = collections.Counter()
        self._terms = {}
        self._freeze = False
        if initial_terms is not None:
            for term in initial_terms:
                self._terms[term] = {}

    def __getitem__(self, term):
        return self._terms[term]

    def __contains__(self, term):
        return term in self._terms

    def __repr__(self):
        return '<Booleanmodel: {} terms, {} documents>'.format(
            len(self._terms), len(self._documents)
        )

    def __eq__(self, other):
        return self._terms == other._terms and self._documents == other._documents

    def clear(self):
        """
        Resets the HashedIndex to a clean state without any terms or documents.
        """
        self._terms = {}
        self._documents = collections.Counter()

    def freeze(self):
        """
        Freezes the HashedIndex, preventing any new terms from being added
        when calling add_term_occurrence.
        """
        self._freeze = True

    def unfreeze(self):
        """
        Unfreezes (thaws) the HashedIndex, allowing new terms to be added
        when calling add_term_occurrence.
        """
        self._freeze = False

    def add_term_occurrence(self, term, document):
        """
        Adds an occurrence of the term in the specified document.
        """
        if document not in self._documents:
            self._documents[document] = 0

        if term not in self._terms:
            if self._freeze:
                return
            else:
                self._terms[term] = collections.Counter()

        if document not in self._terms[term]:
            self._terms[term][document] = 0

        self._documents[document] = 1
        self._terms[term][document] = 1


    def get_term_exist(self, term, document):
        if document not in self._documents:
            raise IndexError(DOCUMENT_DOES_NOT_EXIST)

        if term not in self._terms:
            raise IndexError(TERM_DOES_NOT_EXIST)

        result = self._terms[term].get(document, 0)

        return result

    def get_document_frequency(self, term):
        """
        Returns the number of documents the specified term appears in.
        """
        if term not in self._terms:
            raise IndexError(TERM_DOES_NOT_EXIST)
        else:
            return len(self._terms[term])

    def get_document_length(self, document):
        """
        Returns the number of terms found within the specified document.
        """
        if document in self._documents:
            return self._documents[document]
        else:
            raise IndexError(DOCUMENT_DOES_NOT_EXIST)

    def get_documents(self, term):
        """
        Returns all documents related to the specified term in the
        form of a Counter object.
        """
        if term not in self._terms:
            raise IndexError(TERM_DOES_NOT_EXIST)
        else:
            return self._terms[term]

    def terms(self):
        return list(self._terms)

    def documents(self):
        return list(self._documents)

    def items(self):
        return self._terms


    def generate_document_vector(self, doc):
        result = []
        for term in self._terms:
            result.append(self.get_term_exist(term, doc))

        return result

    def generate_feature_matrix(self):
        """
        Returns a feature matrix in the form of a list of lists which
        represents the terms and documents in this Inverted Index using
        the tf-idf weighting by default. The term counts in each
        document can alternatively be used by specifying scheme='count'.
        A custom weighting function can also be passed which receives a term
        and document as parameters.
        The size of the matrix is equal to m x n where m is
        the number of documents and n is the number of terms.
        The list-of-lists format returned by this function can be very easily
        converted to a numpy matrix if required using the `np.as_matrix`
        method.
        """
        result = []

        for doc in self._documents:
            result.append(self.generate_document_vector(doc))

        return result

    def prune(self, min_value=None, max_value=None, use_percentile=False):
        n_documents = len(self._documents)

        garbage = []
        for term in self.terms():
            freq = self.get_document_frequency(term)
            if use_percentile:
                freq /= n_documents

            if min_value is not None and freq < min_value:
                garbage.append(term)

            if max_value is not None and freq > max_value:
                garbage.append(term)

        for term in garbage:
            del(self._terms[term])

    def to_dict(self):
        return {
            'documents': self._documents,
            'terms': self._terms,
        }

    def from_dict(self, data):
        self._documents = collections.Counter(data['documents'])
        self._terms = {}
        for term in data['terms']:
            self._terms[term] = collections.Counter(data['terms'][term])


def merge(index_list):
    result = BooleanModel()

    for index in index_list:
        first_index = result
        second_index = index

        assert isinstance(second_index, BooleanModel)

        for term in second_index.terms():
            if term in first_index._terms and term in second_index._terms:
                result._terms[term] = first_index._terms[term] + second_index._terms[term]
            elif term in second_index._terms:
                result._terms[term] = second_index._terms[term]
            else:  # pragma: nocover
                raise ValueError("I dont know how the hell you managed to get here")

        result._documents = first_index._documents + second_index._documents

    return result