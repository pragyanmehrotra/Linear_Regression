f = open('journal_data.csv','r') #journal data
g = f.readlines()
y = []

def regression(final):
	'''
	accepts a list of [title,H-index,Impact Factor] 
	,calculates the regression of H-Index and Impact Factor, 
	an equation of that line is produced. which is then used to predict the Impact factor of unkown values
	'''
	#80% of total data
	t = len(final)*80//100
	ybar = 0.0
	xbar = 0.0
	varx = 0.0
	vary = 0.0
	covxy =  0.0
	#adding all the values
	for i in final[:t]:
		xbar += float(i[1])
		ybar += float(i[2])
	#calculating the mean
	xbar /= t
	ybar /= t
	x = 0
	y = 0
	#calculating the covaraince
	for i in final[:t]:
		covxy+= float(i[1])*float(i[2])
		x += float(i[1])**2
		y += float(i[2])**2
	covxy /= t
	covxy -= (xbar*ybar)
	x/=t
	y/=t
	varx = x-(xbar**2)
	vary = y-(ybar**2)
	m = covxy/varx
	#printing the final equation of the line
	print ("equation of the line: y = " + str(ybar) + " + " + str(m) + "(x - " + str(xbar) + ")")
	#printing the correlation coefficient
	cor_coeff = covxy/((varx*vary)**0.5) 
	print ("correlation coefficient: "+ str(cor_coeff))
	#testing on the remaining 20%
	mean_squared_error = 0
	#predicting Impact factor on the remaining 20% data and storing the output in output_journal.csv
	g2 = open('output_journal.csv','w')
	for i in final[t:]:
		y = ybar + m*(float(i[1])-xbar)
		g2.write(str(i[0])+";"+str(i[1])+";"+str(y))
		mean_squared_error +=  (y-float(i[2]))**2
	mean_squared_error /= len(final[t:])
	print ("mean squared error: " + str(mean_squared_error))
	print ("output saved in output_journal.csv")
	
	##creating an impact factor list of conferences 
	f2 = open('conference_data.csv','r')
	lines = f2.readlines()
	table = []
	#cleaning the data
	for line in lines:
		field = ''
		row = []
		toggle = 0
		for ch in line:
			if ch=='"' and toggle == 0:
				toggle = 1
				field += '"'
				continue
			if ch=='"' and toggle == 1:
				toggle = 0
				field += '"'
				continue
			if ch==';' and toggle == 0:
				row.append(field)
				field = ''
				continue
			field += ch
		row.append(field)
		table.append(row)
	#storing the result in output_conference.csv 
	f3 = open('output_conference.csv','w')
	for i in table[1:]:
		f3.write(str(i[2])+";"+str(i[7])+";"+str(ybar + m*(float(i[7])-xbar))+"\n")
	f3.close()
	print ("Output saved in output_conference.csv")
	

	
		 
		
	
	
	
#cleaning the journal file and extracting index number,title and H-index from it.
for i in g:	
	s=''
	x=[]
	t=0
	for j in i:
		if j=='"' and t==0:
			t=1
			s += '"'
			continue
		if j=='"' and t==1:
			t=0
			s+= '"'
			continue
		if j==';' and t==0:
			x.append(s)
			s = ''
			continue
		s+=j
	x.append(s)
	y.append([x[0],x[2],x[7]])


p = open('found.txt','r') #impact factor list
c= p.readlines()
n = []
#cleaning found.txt
for i in c:
	n.append(i.split(';'))
final = []
b=0
#finding each title and extracting impact factor from it
for i in y:
	flag=1
	for j in n:
		if '"' + j[0] + '"' ==  i[1]:
			final.append([i[1],i[2],j[2]])
			flag=0
			break
#final function call
regression(final)
