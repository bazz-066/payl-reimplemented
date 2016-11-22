import math
import os


class PaylModel(object):
    DIRNAME = "models"
    FILENAME_TPL = ".payl"

    def __init__(self, port, length):
        self.port = port
        self.length = length
        self.grams = {}
        self.filename = self.DIRNAME + "/" + str(self.port) + "-" + str(self.length) + self.FILENAME_TPL

    def add_grams(self, grams):
        for key, value in grams.items():
            self.add_gram(key, value)

    def add_gram(self, gram, gram_freq):
        if gram in self.grams:
            self.grams[gram].add_item(gram_freq)
        else:
            self.grams[gram] = ByteFrequency()
            self.grams[gram].add_item(gram_freq)

    def distance(self, new_model):
        dist = 0
        alpha = 0.001

        for i in range(0, 256):
            if str(i) in self.grams:
                old_mean = self.grams[str(i)].mean
                old_stddev = self.grams[str(i)].stddev
            elif i in self.grams:
                old_mean = self.grams[i].mean
                old_stddev = self.grams[i].stddev
            else:
                old_mean = 0
                old_stddev = 0

            if i in new_model:
                new_gram = new_model[i]
            elif str(i) in new_model:
                new_gram = new_model[str(i)]
            else:
                new_gram = 0


            substracted_mean = float(old_mean) - float(new_gram)
            if substracted_mean < 0:
                substracted_mean *= -1

            tmp = (substracted_mean / (float(old_stddev) + alpha))
            # print str(i) + " --> |" + str(old_mean) + "-" + str(new_gram) + "| / " + str(old_stddev) + " + 0.001 = " + str(tmp)
            dist += tmp

        return dist

    def save(self):
        if not os.path.isdir(self.DIRNAME): #path exists
            os.mkdir(self.DIRNAME)

        fmodel = open(self.filename, "w")
        if not fmodel:
            print "Failed to save model"
            return

        for key, value in self.grams.items():
            fmodel.write(str(key) + ";" + str(value.mean) + ";" + str(value.stddev) + ";" + str(value.count) + "\n")

        fmodel.close()
        print "Model " + str(self.port) + "-" + str(self.length) + " was successfully saved."

    def load(self):
        if not os.path.exists(self.filename):
            print "No file for model " + str(self.port) + "-" + str(self.length)
            return

        fmodel = open(self.filename, "r")

        for line in fmodel.readlines():
            splitted = line.split(";")
            b_freq = ByteFrequency()
            b_freq.mean = splitted[1]
            b_freq.stddev = splitted[2]
            b_freq.count = splitted[3]
            self.grams[splitted[0]] = b_freq

        fmodel.close()

    def __str__(self):
        retval = "Port : " + str(self.port) + "; Length : " + str(self.length) + "\n"

        for key, value in self.grams.items():
            retval += str(key) + " : " + str(value)

        return retval


class ByteFrequency(object):
    def __init__(self):
        self.mean = 0
        self.stddev = 0
        self.count = 0

    def add_item(self, gram_freq):
        old_count = self.count
        self.count += 1
        old_mean = self.mean
        self.mean = ((self.mean * old_count) + gram_freq) / float(self.count)

        old_var = math.pow(self.stddev, 2)
        old_stdddev = self.stddev
        if self.count > 1:
            self.stddev = math.sqrt((((self.count - 2) / float(self.count - 1)) * old_var) + ((pow(gram_freq - old_mean, 2)) / float(self.count)))
        else:
            self.stddev = 0

    def __str__(self):
        return "Mean : " + str(self.mean) + "; Stddev : " + str(self.stddev) + "\n"