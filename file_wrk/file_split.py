#! /usr/bin/env python
import os, re

#========== Programme principal =============
if __name__ == "__main__":

    #fichier = "notes_light.txt"
    fichier = "notes.txt"
    line = 0
    creat_file = ""
    print "starting script"
    nb_line = sum(1 for _ in open(fichier))
    print "number of line = ",nb_line
    os.popen( 'rm -rf Note' )
    os.popen( 'mkdir Note' )
    stream = open(fichier,"r").read().splitlines()

    while  line < nb_line:
       if stream[line] != "":
         line_split = stream[line].split()
         if line_split[0] == "Categories":
            creat_file = line_split[1]
            test=os.popen( 'mkdir Note/%s' % line_split[1])
         else:
            if creat_file != "":
              titre_split = re.findall(r'\w+', stream[line])
              titre_fichier = ""
              size_title = 0
              for i in titre_split:
                 size_title += 1
                 if size_title == 1:
                   titre_fichier = i
                 else:
                   titre_fichier = titre_fichier+" "+i
                 if size_title > 10: break
              print "titre_fichier = ",titre_fichier
              os.popen( 'touch Note/%s/%s.txt' % (creat_file,titre_fichier))
              title_file = open('Note/%s/%s.txt' % (creat_file,titre_fichier), "w+")
              creat_file = ""
            title_file.write('%s\n' % stream[line])
       else:
          if creat_file == "":
            title_file.write('\n')
       line += 1
    print "script ended"
# 144 categories
