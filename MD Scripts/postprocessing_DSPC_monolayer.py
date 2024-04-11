import os, shutil

def sort_z(filename):
    command = "cat " + filename + " | sort -n -k1 > tmp; mv tmp " + filename
    os.system(command)

def average_monolayers(filename):
    list_to_check = []
    with open(filename, 'r') as f:
         for line in f:
             if '\t' in line:
                linesplit = line.split('\t')
             elif ' ' in line:
                linesplit = line.split(' ')
             z = float(linesplit[0])
             list_to_check.append(z)

    with open(filename, 'r') as f:
         for line in f:
             if '\t' in line:
                linesplit = line.split('\t')
             elif ' ' in line:
                linesplit = line.split(' ')
             z = float(linesplit[0])
             value = float((linesplit[1]).strip('\n'))
             if z > 0:
                z = z*(-1)
                with open(filename, 'r') as f1:
                    for line1 in f1:
                        if '\t' in line1:
                            linesplit1 = line1.split('\t')
                        elif ' ' in line1:
                            linesplit1 = line1.split(' ')
                        z1 = float(linesplit1[0])
                        value1 = float((linesplit1[1]).strip('\n'))
                        if z == z1:
                           newvalue = (value+value1)/2
                           if newvalue < 0:
                              newvalue = 0
                           with open('tmp', 'a') as g:
                               g.write(str(z) + " " + str(newvalue) + "\n")
             elif z == 0:
                        with open('tmp', 'a') as g:
                               g.write(str(z) + " " + str(value) + "\n")
             if z not in list_to_check:
                      with open('tmp', 'a') as g:
                               g.write(str(z) + " " + "0" + "\n")
    shutil.move('tmp', filename)    



#function to calculate density of groups
def calc_density_split(mylist, molecule, outfile, split=None):
    list_atoms = []
    for i in mylist:
        list_atoms.append(i)
    list_z = []
    filename = 'data/atom_types/Number_density_' + molecule + '_' + str(list_atoms[0]) + '.tsv' 
    with open(filename, 'r') as f:
  
      for line in f:
         linesplit = line.split('\t')
         list_z.append(linesplit[0])
    lists = [[] for _ in range(len(list_atoms))]
    list_final = []
    for i in range (0, len(list_atoms)):
         filename = 'data/atom_types/Number_density_' + molecule + '_' + str(list_atoms[i]) + '.tsv'
         with open(filename, 'r') as f:
            for line in f:

               linesplit = line.split('\t')
               lists[i].append(linesplit[1])
    sum = 0 
    for j in range(0, len(lists[0])):
       for i in range (0, len(list_atoms)):
            val = float((lists[i])[j])
            sum = sum + val
       list_final.append(sum)
       sum = 0
    c = [list_z, list_final]
    with open(outfile, 'a') as file:
       for x in zip(*c):
          file.write("{0}\t{1}\n".format(*x))
    if split == 'yes':
       with open(outfile, 'r') as f:
           for line in f:
               if '\t' in line:
                  linesplit = line.split('\t')
               else:
                  linesplit = line.split(' ')
               val = float((linesplit[1]).strip('\n'))
               newval = val/len(list_atoms)
               with open ('tmp', 'a') as g:
                    g.write(str(linesplit[0]) + "\t" + str(newval) + "\n")
       shutil.move('tmp', outfile)
    elif split == 'CH3':
       with open(outfile, 'r') as f:
           for line in f:
               if '\t' in line:
                  linesplit = line.split('\t')
               else:
                  linesplit = line.split(' ')
               val = float((linesplit[1]).strip('\n'))
               newval = val/(len(list_atoms)/2)
               with open ('tmp', 'a') as g:
                    g.write(str(linesplit[0]) + "\t" + str(newval) + "\n")
       shutil.move('tmp', outfile)
    elif split == 'alk':
       with open(outfile, 'r') as f:
           for line in f:
               if '\t' in line:
                  linesplit = line.split('\t')
               else:
                  linesplit = line.split(' ')
               val = float((linesplit[1]).strip('\n'))
               newval = val/3
               with open ('tmp', 'a') as g:
                    g.write(str(linesplit[0]) + "\t" + str(newval) + "\n")
       shutil.move('tmp', outfile)


#correct double counting of 0.0 in atom_types
for file in os.listdir('data/atom_types'):
   filename = 'data/atom_types/' + file
   with open (filename, 'r') as f:
       count = 0
       for line in f:
           count = count + 1
           if (count == 1):
              linesplit = line.split('\t')
              half = float(linesplit[1])/2
              with open ('tmp', 'a') as g:
                   g.write(str(linesplit[0]) + "\t" + str(half) + "\n")
           else:
              with open ('tmp', 'a') as g:
                   g.write(line)
   shutil.move('tmp', filename)


#correct double counting of 0.0 in elements
for file in os.listdir('data/elements'):
   filename = 'data/elements/' + file
   with open (filename, 'r') as f:
       count = 0
       for line in f:
           count = count + 1
           if (count == 1):
              linesplit = line.split('\t')
              half = float(linesplit[1])/2
              with open ('tmp', 'a') as g:
                   g.write(str(linesplit[0]) + "\t" + str(half) + "\n")
           else:
              with open ('tmp', 'a') as g:
                   g.write(line)
   shutil.move('tmp', filename)


#correct z(x) axis in atom_types:
for file in os.listdir('data/atom_types'):
  filename = 'data/atom_types/' + file
  
  with open (filename, 'r') as f:
    for line in f:
        pass
    last_line = line
    last_line_split = last_line.split('\t')
    max_z = float(last_line_split[0])

#find max value when centering on 0
if ((2*max_z) + 1 ) % 2 != 0:
    half = max_z/2
else:
    half = (max_z-0.5)/2 
print ("maxz, half=", max_z, half)


for file in os.listdir('data/atom_types'):
  filename = 'data/atom_types/' + file

  with open (filename, 'r') as f:
   
    count = 0
    for line in f:
      
        #writing corrected first column
        linesplit = line.split('\t')
        newline = str(float(linesplit[0]) - half - 1)
        with open('firstcolumn', 'a') as g:
               g.write(newline + "\n")


        count = count + 1 
        #swapping y values before and after 0
        if count > max_z:
           newline = str(linesplit[1])
           with open('secondcolumn1', 'a') as g:
               g.write(newline)
        else:
           newline = str(linesplit[1])
           with open('secondcolumn2', 'a') as g:
               g.write(newline)
#cleaning
  os.system('cat secondcolumn1 secondcolumn2 > secondcolumn')
  os.system ('paste firstcolumn secondcolumn > tmp')
    

  os.remove('firstcolumn')
  os.remove('secondcolumn')
  os.remove('secondcolumn1')
  os.remove('secondcolumn2')
  shutil.move('tmp', filename)

   

#correct z(x) axis in elements:
for file in os.listdir('data/elements'):
  filename = 'data/elements/' + file
  with open (filename, 'r') as f:
    for line in f:
        pass
    last_line = line
    last_line_split = last_line.split('\t')
    max_z = float(last_line_split[0])

#find max value when centering on 0
if ((2*max_z) + 1 ) % 2 != 0:
    half = max_z/2
else:
    half = (max_z-0.5)/2 

print ("element=", max_z, half)

for file in os.listdir('data/elements'):
  filename = 'data/elements/' + file
  with open (filename, 'r') as f:


    count = 0
    for line in f:
        #writing corrected first column
        linesplit = line.split('\t')
        newline = str(float(linesplit[0]) - half - 1)
        with open('firstcolumn', 'a') as g:
               g.write(newline + "\n")


        count = count + 1 
        #swapping y values before and after 0
        if count > max_z:
           newline = str(linesplit[1])
           with open('secondcolumn1', 'a') as g:
               g.write(newline)
        else:
           newline = str(linesplit[1])
           with open('secondcolumn2', 'a') as g:
               g.write(newline)
#cleaning
  os.system('cat secondcolumn1 secondcolumn2 > secondcolumn')
  os.system ('paste firstcolumn secondcolumn > tmp')
  os.remove('secondcolumn')
  os.remove('secondcolumn1')
  os.remove('secondcolumn2')
  os.remove('firstcolumn')
  shutil.move('tmp', filename)




#correct double counting of 0.0 in atom_types
for file in os.listdir('data/atom_types'):
   filename = 'data/atom_types/' + file
   with open (filename, 'r') as f:
       count = 0
       for line in f:
           count = count + 1
           if (count == 1):
              linesplit = line.split('\t')
              half = float(linesplit[1])/2
              with open ('tmp', 'a') as g:
                   g.write(str(linesplit[0]) + "\t" + str(half) + "\n")
           else:
              with open ('tmp', 'a') as g:
                   g.write(line)
   shutil.move('tmp', filename)


#correct double counting of 0.0 in elements
for file in os.listdir('data/elements'):
   filename = 'data/elements/' + file
   with open (filename, 'r') as f:
       count = 0
       for line in f:
           count = count + 1
           if (count == 1):
              linesplit = line.split('\t')
              half = float(linesplit[1])/2
              with open ('tmp', 'a') as g:
                   g.write(str(linesplit[0]) + "\t" + str(half) + "\n")
           else:
              with open ('tmp', 'a') as g:
                   g.write(line)
   shutil.move('tmp', filename)

#density water
mylist = ["H1", "H2", "O"]
print ('calculating density water')
calc_density_split(mylist, 'HOH', 'water.dat', split='yes')
print ('done')

shutil.move('data/elements/Number_density_carbon.tsv', 'carbon.dat')
shutil.move('data/elements/Number_density_nitrogen.tsv', 'nitrogen.dat')
shutil.move('data/elements/Number_density_phosphorus.tsv', 'phosphorus.dat')

os.system("paste data/elements/Number_density_hydrogen.tsv data/atom_types/Number_density_HOH_H1.tsv data/atom_types/Number_density_HOH_H2.tsv | awk '{print $1, $2-$4-$6}' > hydrogen.dat")
os.system("paste data/elements/Number_density_oxygen.tsv data/atom_types/Number_density_HOH_O.tsv | awk '{print $1, $2-$4}' > oxygen.dat")

average_monolayers('carbon.dat')
average_monolayers('oxygen.dat')
average_monolayers('hydrogen.dat')
average_monolayers('phosphorus.dat')
average_monolayers('nitrogen.dat')
average_monolayers('water.dat')


#density chol
mylist = ["C13", "H13A", "H13B", "H13C", "C15", "H15A", "H15B", "H15C", "C14", "H14A", "H14B", "H14C", "N", "C12", "C11", "H12A", "H12B", "H11A", "H11B"]
calc_density_split(mylist, 'DPPC', 'chol.dat', split='yes')

average_monolayers('chol.dat')

#density methyl
mylist = ["C318", "H18X", "H18Y", "H18Z", "C218", "H18R", "H18S", "H18T"]
calc_density_split(mylist, 'DPPC', 'CH3.dat', split='CH3')

average_monolayers('CH3.dat')


mylist = ["C1", "HA", "HB", "C2", "C3", "HY", "HX", "HS"]
calc_density_split(mylist, 'DPPC', 'gly.dat', split='yes')

average_monolayers('gly.dat')

mylist = ["C21", "O21", "O22", "C31", "O31", "O32"]
calc_density_split(mylist, 'DPPC', 'coo.dat', split='yes')

average_monolayers('coo.dat')
mylist = ["C210", "C211", "C212", "C213", "C214", "C215", "C22", "C23", "C24", "C25", "C26", "C27", "C28", "C29", "C310", "C311", "C312", "C313", "C314", "C315", "C32", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "H10R", "H10S", "H10X", "H10Y", "H11R", "H11S", "H11X", "H11Y", "H12R", "H12S", "H12X", "H12Y", "H13R", "H13S", "H13X", "H13Y", "H14R", "H14S", "H14X", "H14Y", "H15R", "H15S", "H15X", "H15Y", "H16R", "H16S", "H16X", "H16Y", "H17R", "H17S", "H17X", "H17Y",  "H2R", "H2S", "H2X", "H2Y", "H3R", "H3S", "H3X", "H3Y", "H4R", "H4S", "H4X", "H4Y", "H5R", "H5S", "H5X", "H5Y", "H6R", "H6S", "H6X", "H6Y", "H7R", "H7S", "H7X", "H7Y", "H8R", "H8S", "H8X", "H8Y", "H9R", "H9S", "H9X", "H9Y"]
calc_density_split(mylist, 'DPPC', 'alk.dat', split='alk')

average_monolayers('alk.dat')
mylist = ["P", "O11", "O12", "O13", "O14"]
calc_density_split(mylist, 'DPPC', 'PO4.dat', split='yes')

average_monolayers('PO4.dat')
#split C and H


mylist = ["H15A", "H15B", "H15C", "H13A", "H13B", "H13C", "H14A", "H14B", "H14C", "H11A", "H11B", "H12A", "H12B"]
calc_density_split(mylist, 'DPPC', 'hydrogen_heads.dat', split='no')

average_monolayers('hydrogen_heads.dat')

mylist = ["C11", "C12", "C13", "C14", "C15"]
calc_density_split(mylist, 'DPPC', 'carbon_heads.dat', split='no')

average_monolayers('carbon_heads.dat')

mylist = ["HA", "HB", "HS", "HX", "HY"]
calc_density_split(mylist, 'DPPC', 'hydrogen_linker.dat', split='no')

average_monolayers('hydrogen_linker.dat')

mylist = ["C1", "C2", "C3"]
calc_density_split(mylist, 'DPPC', 'carbon_linker.dat', split='no')

average_monolayers('carbon_linker.dat')

mylist = ["C210", "C211", "C212", "C213", "C214", "C215", "C21", "C31", "C22", "C23", "C24", "C25", "C26", "C27", "C28", "C29", "C310", "C311", "C313", "C312", "C314", "C315", "C216", "C217", "C316", "C317", "C32", "C33", "C34", "C35", "C36", "C37", "C38", "C39"]
calc_density_split(mylist, 'DPPC', 'carbon_tails.dat', split='no')

average_monolayers('carbon_tails.dat')

mylist = ["H2S", "H2R", "H3S", "H3R", "H4S", "H4R", "H5S", "H5R", "H6S", "H6R", "H7S", "H7R", "H8S", "H8R", "H9S", "H9R", "H10S", "H10R", "H11S", "H11R", "H12S", "H12R", "H13S", "H13R", "H14S", "H14R", "H15S", "H15R", "H16R", "H16S", "H2Y", "H2X", "H3Y", "H3X", "H4Y", "H16Y", "H16X", "H17R", "H17S", "H17Y", "H17X", "H4X", "H5Y", "H5X", "H6Y", "H6X", "H7Y", "H7X", "H8Y", "H8X", "H9Y", "H9X", "H10Y", "H10X", "H11Y", "H11X", "H12Y", "H12X", "H13Y", "H13X", "H14Y", "H14X", "H15Y", "H15X"]
calc_density_split(mylist, 'DPPC', 'hydrogen_tails.dat', split='no')

average_monolayers('hydrogen_tails.dat')

mylist = ["C218", "C318"]
calc_density_split(mylist, 'DPPC', 'carbon_methyl.dat', split='no')

average_monolayers('carbon_methyl.dat')

mylist = ["H18R", "H18S", "H18T", "H18X", "H18Y", "H18Z"]
calc_density_split(mylist, 'DPPC', 'hydrogen_methyl.dat', split='no')

average_monolayers('hydrogen_methyl.dat')

for file in os.listdir('data/atom_types'):
    if '.dat' in file:
       sort_z(file)


