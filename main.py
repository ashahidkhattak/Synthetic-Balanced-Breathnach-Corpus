import glob
import os
import music21

# converting everything into the key of C major or A minor

# major conversions
from music21 import interval, pitch

stack = {
            "F": 480,
            "G": 66,
            "A": 300,
            "E": 355,
            "C": 467,
            "B": 475,
}

for ele in stack:
    counter = 0
    total_files_to_be_generated = stack[ele]
    for file in glob.glob("./midi/*.mid"):
        if(counter == total_files_to_be_generated):
            break

        filename = os.path.basename(file)
        score = music21.converter.parse(file)
        key = score.analyze('key')
        #print(key.tonic.name, key.mode)
        old_key = key.tonic.name
        # we dont want to create synthtic music of a key from the same key
        if(old_key == ele):
            continue
        counter += 1

        if key.mode == 'minor':
            i = interval.Interval(key.parallel.tonic, pitch.Pitch(ele))
        else:
            i = interval.Interval(key.tonic, pitch.Pitch(ele))

        # print(halfSteps)
        newscore = score.transpose(i)
        newFileName = key.tonic.name + " to "+ ele +"_" + filename
        key = newscore.analyze('key')
        print("From key: ",old_key, "to key: ", key.tonic.name)
        newscore.write('midi', "./synthetic/" + newFileName)