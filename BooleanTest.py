import nltk
import BooleanModel

EN_PATH = './testdata_en/'

if __name__ == '__main__':

    bm = BooleanModel.BooleanModel()
    path = EN_PATH + 'basic.txt'

    with open(path, "r") as f:
        documents = f.readlines()

    line = 0
    for document in documents:
        for term in nltk.word_tokenize(document):
            bm.add_term_occurrence(term, line)
        line += 1

    dict_info = bm.items()

    #dictionary output
    print("dictionary count : ", len(dict_info))
    for key in dict_info.keys():
        print(key, ' : ', end='')
        print(dict_info[key].keys())

    #document vector output
    for document in bm.documents():
        print('doc#', document, '.', end='')
        print(documents[document].strip(), ' : ', end='')
        print(bm.generate_document_vector(document))