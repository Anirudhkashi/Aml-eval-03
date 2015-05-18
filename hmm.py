from myhmm_log import *

def getData(file):
	fp= open(file, 'r')
	j= 1
	obs= []
	seq= []
	for line in fp:
		if(j== 10):
			seq= []
			obs.append(seq)
			j=0
		j+=1
		seq.append(line.strip('\n'))
	return obs

def genModel(obslist):
	mod= MyHmmLog('debate_initial.json')
	mod.forward_backward_multi(obslist)
	return mod

def testVals(file):
	tstFile=open(file,'r')
	tstVec=tstFile.read().split('\n')
	i=0
	k=1
	vecVec=[[]]
	for j in range(len(tstVec)-1):	
		vecVec[i].append(tstVec[j])
		k+=1
		if(k==10):
			k=0
			i+=1
			vecVec.append([])
	yVec=yVals(vecVec[:-1])
	return yVec

def yVals(vecVec):
	yVec=[]
	for i in vecVec:
		yVec.append(argMax(i))
	return yVec

def argMax(vec):
	val= silent_model.forward(vec)
	clss="silent"
	if(single_model.forward(vec)>val):
		val=single_model.forward(vec)
		clss="single"
	if(multi_model.forward(vec)>val):
		val=multi_model.forward(vec)
		clss="multi"
	return clss

obs= []

#output.txt
def genVariable(var, stri):
	op= []
	fp= open(stri+ '_output.txt', 'w')
	s= ''
	i= 0
	for val in var:
		d= {}
		d[i]= val
		op.append(d)
		i+= 50

	i= 0
	for dic in op:
		fp.write("At time "+str(i)+"ms, the model is- "+dic[i]+"\n")
		i+= 50

	fp.close()


def cState(li):
	count1=0
	count2=0
	count3=0
	for i in li:
		if(i=="silent"):
				count1+= 1
		elif(i=="single"):
				count2+= 1
		elif(i=="multi"):
				count3+= 1
		di={"silent":count1,"single":count2,"multi":count3}
	return di


def qIndex(vec):
	stDic=cState(vec)
	qInd=10*stDic['silent']+10*stDic['single']-10*stDic['multi']
	qInd= (float)(qInd)/(float)(len(vec))
	return qInd




single_model= genModel(getData('single_output.txt'))
multi_model= genModel(getData('multi_output.txt'))
silent_model= genModel(getData('silent_output.txt'))

# var1= testVals('single_2_trg_vq.txt')
# var2= testVals('multi_2_trg_vq.txt')

# genVariable(var1, 'single')
# genVariable(var2, 'multi')

# print(qIndex(var1))
# print(qIndex(var2))

var= []
for i in range(1, 11):
	var.append(testVals('c'+str(i)+'_output.txt'))

j=1
for i in var:
	genVariable(i, 'output2/c'+str(j))
	j+=1

j=1
for i in var:
	print '\nCount Of States In File c',j, '=', cState(i)
	print 'Quality index for test file c',j, ' =', qIndex(i)
	print ''
	j+=1