from nltk.corpus import wordnet
import nltk
import xlrd

length = 0
stop_words = ["number", "Number", "percent", "Percent", "percentage", "Percentage", "%", "rate", "Rate", "of", "for", "with", "in", "the", "The", "-", "an", "a"]

def meaningGenerator(list_of_words):
    global length
    listt = []
    listtt = []
    for i in list_of_words:
        if (i not in stop_words):
            length +=1
            for j in wordnet.synsets(i):
                for k in j.lemmas():
                    listt.append(k.name())
            listtt.append(listt)
            listt = []
    return listtt


def generateBigListOfAllSynomys(string_array):
    #dct = {}
    #c = 0
    big_list = string_array
    for i in meaningGenerator(string_array):
    ##    dct[string[c]] = i
    ##    c+=1
        for j in i:
            if (j not in big_list):
                big_list.append(j)
    #print(data_dct)
    return big_list


def openFileIntoADict(location):
    sheet = xlrd.open_workbook(location).sheet_by_index(0)

    data_dct = {}
    for r in range(1, sheet.nrows):
        data_dct[sheet.cell_value(r, 0)] = sheet.cell_value(r, 1).split(" ")
    return data_dct


def findBestMatchedRecords(data_dct, big_list):
    global length
    p = nltk.PorterStemmer()
    final_list = []
    matches = []
    for k, v in data_dct.items():
        ct = 0
        for i in v:
            if (i not in stop_words):
                if ((i in big_list) or (p.stem(i) in big_list)) :
                    ct+=1
                    matches.append(i)
            
        if (ct/length*100 > 50):
            final_list.append(k)
            final_list.append(ct)
    return [final_list, matches]



def main():
    location = "file2.xlsx"
    data_dct = openFileIntoADict(location)

    string = input("ENTER YOUR SEARCH PHRASE: ")
    string_array = string.split(" ")
    #length = len(string_array)

    big_list = generateBigListOfAllSynomys(string_array)

    final_list = findBestMatchedRecords(data_dct, big_list)

    print("\n\nPotential matches are: \n")
    for i in final_list[0]:
        print(i)
    
    print("\n\n\n")
    for i in final_list[1]:
        print(i)

    
main()
