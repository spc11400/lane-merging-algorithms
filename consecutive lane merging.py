import numpy as np


def main():
    a=[int(x) for x in input("{a_i}:").split()]
    b=[int(x) for x in input("{b_j}:").split()]
    c=[int(x) for x in input("{c_k}:").split()]
    w11=int(input("W_1^=:"))  #first merging point 的 waiting time from the same incoming lane
    w12=int(input("W_1^+:"))  #first merging point 的 waiting time from different incoming lane
    w21=int(input("W_2^=:"))  #second merging point 的 waiting time from the same incoming lane
    w22=int(input("W_2^+:"))  #second merging point 的 waiting time from different incoming lane
    T_f=int(input("T_f:"))
    # a=[1,3]
    # b=[2,4]
    # c=[5]
    # w11=1
    # w12=3
    # w21=1
    # w22=3
    # T_f=3

    alpha=len(a)
    beta=len(b)
    gamma=len(c)

    L_1A=np.zeros((alpha+1,beta+1),dtype=int)
    L_1B=np.zeros((alpha+1,beta+1),dtype=int)

    L_2A=np.zeros((alpha+1,beta+1,gamma+1),dtype=int)
    L_2B=np.zeros((alpha+1,beta+1,gamma+1),dtype=int)
    L_2C_A=np.zeros((alpha+1,beta+1,gamma+1),dtype=int)
    L_2C_B=np.zeros((alpha+1,beta+1,gamma+1),dtype=int)

    L_record=np.ones((4,alpha+1,beta+1,gamma+1))

    #initialization L1
    L_1A[1,0]=a[0]
    L_1B[0,1]=b[0]
    for i in range(1,L_1B.shape[0]):
       L_1B[i,0]=10000
    for j in range(1,L_1A.shape[1]):
       L_1A[0,j]=10000

    for i in range(2,L_1A.shape[0]):
        L_1A[i,0]=max(a[i-1],L_1A[i-1,0]+w11)
          
    for j in range(2,L_1A.shape[1]):
        L_1B[0,j]=max(b[j-1],L_1B[0,j-1]+w11)

    for i in range(1,L_1A.shape[0]):
        for j in range(1,L_1A.shape[1]):
            L_1A[i,j]=min(max(a[i-1],L_1A[i-1,j]+w11),max(a[i-1],L_1B[i-1,j]+w12))
            L_1B[i,j]=min(max(b[j-1],L_1A[i,j-1]+w12),max(b[j-1],L_1B[i,j-1]+w11))
   
    #initialization #L2
    for i in range(L_2B.shape[0]):
        for k in range(L_2B.shape[2]):
            L_2B[i,0,k]=10000
    for j in range(L_2A.shape[1]):   
        for k in range(L_2A.shape[2]):
            L_2A[0,j,k]=10000
    for i in range(L_2C_A.shape[0]):
        for j in range(L_2C_A.shape[1]):
            L_2C_A[i,j,0]=10000
            L_2C_B[i,j,0]=10000
    for k in range(L_2C_A.shape[2]):
        for j in range(L_2C_A.shape[1]):
            L_2C_A[0,j,k]=10000
        for i in range(L_2C_A.shape[0]):
            L_2C_B[i,0,k]=10000

    L_2A[1,0,0]=L_1A[1,0]+T_f
    L_2B[0,1,0]=L_1B[0,1]+T_f
    L_2C_A[0,0,1]=c[0]
    L_2C_B[0,0,1]=c[0]
    for i in range(2,L_2A.shape[0]):
        L_2A[i,0,0]=max(L_1A[i,0]+T_f,L_2A[i-1,0,0]+w21)
        L_record[0,i,0,0]=L_record[0,i-1,0,0]*10
    for j in range(2,L_2B.shape[1]):
        L_2B[0,j,0]=max(L_1B[0,j]+T_f,L_2B[0,j-1,0]+w21)
        L_record[1,0,j,0]=L_record[1,0,j-1,0]*10+1
    for k in range(2,L_2C_A.shape[2]):
        L_2C_A[0,0,k]=max(c[k-1],L_2C_A[0,0,k-1]+w21)
        L_record[2,0,0,k]=L_record[2,0,0,k-1]*10+2
    for k in range(2,L_2C_B.shape[2]):
        L_2C_B[0,0,k]=max(c[k-1],L_2C_B[0,0,k-1]+w21)
        L_record[3,0,0,k]=L_record[3,0,0,k-1]*10+3
    for i in range(1,L_2A.shape[0]):
        for k in range(1,L_2A.shape[2]):
            L_2A[i,0,k]=min(max(L_1A[i,0]+T_f,L_2A[i-1,0,k]+w21),
                        max(L_1A[i,0]+T_f,L_2C_A[i-1,0,k]+w22))
            if L_2A[i,0,k]==max(L_1A[i,0]+T_f,L_2A[i-1,0,k]+w21):
                L_record[0,i,0,k]=L_record[0,i-1,0,k]*10
            else:
                L_record[0,i,0,k]=L_record[2,i-1,0,k]*10+2
            L_2C_A[i,0,k]=min(max(c[k-1],L_2A[i,0,k-1]+w22),
                            max(c[k-1],L_2C_A[i,0,k-1]+w21))
            if L_2C_A[i,0,k]==max(c[k-1],L_2A[i,0,k-1]+w22):
                L_record[2,i,0,k]=L_record[0,i,0,k-1]*10
            else:
                L_record[2,i,0,k]=L_record[2,i,0,k-1]*10+2
    for j in range(1,L_2B.shape[1]):
        for k in range(1,L_2B.shape[2]):
            L_2B[0,j,k]=min(max(L_1B[0,j]+T_f,L_2B[0,j-1,k]+w21),
                        max(L_1B[0,j]+T_f,L_2C_B[0,j-1,k]+w22))
            if L_2B[0,j,k]==max(L_1B[0,j]+T_f,L_2B[0,j-1,k]+w21):
                L_record[1,0,j,k]=L_record[1,0,j-1,k]*10+1
            else:
                L_record[1,0,j,k]=L_record[3,0,j-1,k]*10+3
            L_2C_B[0,j,k]=min(max(c[k-1],L_2B[0,j,k-1]+w22),
                            max(c[k-1],L_2C_B[i,0,k-1]+w21))
            if L_2C_B[0,j,k]==max(c[k-1],L_2B[0,j,k-1]+w22):
                L_record[3,0,j,k]=L_record[1,0,j,k-1]*10+1
            else:
                L_record[3,0,j,k]=L_record[3,0,j,k-1]*10+3
    for i in range(1,L_2A.shape[0]):
        for j in range(1,L_2A.shape[1]):
            L_2A[i,j,0]=min(max(L_1A[i,j]+T_f,L_2A[i-1,j,0]+w21),
                        max(L_1A[i,j]+T_f,L_2B[i-1,j,0]+w21))
            if L_2A[i,j,0]==max(L_1A[i,j]+T_f,L_2A[i-1,j,0]+w21):
                L_record[0,i,j,0]=L_record[0,i-1,j,0]*10
            else:
                L_record[0,i,j,0]=L_record[1,i-1,j,0]*10+1
            L_2B[i,j,0]=min(max(L_1B[i,j]+T_f,L_2A[i,j-1,0]+w21),
                        max(L_1B[i,j]+T_f,L_2B[i,j-1,0]+w21))
            if L_2B[i,j,0]==max(L_1B[i,j]+T_f,L_2A[i,j-1,0]+w21):
                L_record[1,i,j,0]=L_record[0,i,j-1,0]*10
            else:
                L_record[1,i,j,0]=L_record[1,i,j-1,0]*10+1
    #Derive L2
    for i in range(1,L_2A.shape[0]):
        for j in range(1,L_2A.shape[1]):
            for k in range(1,L_2A.shape[2]):

                L_2A[i,j,k]=min(
                    max(max(a[i-1],L_1A[i-1,j]+w11)+T_f,
                    L_2A[i-1,j,k]+w21),
                    max(max(a[i-1],L_1B[i-1,j]+w12)+T_f,
                    L_2B[i-1,j,k]+w21),
                    min(max(max(a[i-1],L_1A[i-1,j]+w11)+T_f,
                    L_2C_A[i-1,j,k]+w22),
                    max(max(a[i-1],L_1B[i-1,j]+w12)+T_f,
                    L_2C_B[i-1,j,k]+w22))
                )
                if L_2A[i,j,k] == max(max(a[i-1],L_1A[i-1,j]+w11)+T_f,L_2A[i-1,j,k]+w21):
                    L_record[0,i,j,k]=L_record[0,i-1,j,k]*10
                elif L_2A[i,j,k] == max(max(a[i-1],L_1B[i-1,j]+w12)+T_f, L_2B[i-1,j,k]+w21):
                    L_record[0,i,j,k]=L_record[1,i-1,j,k]*10+1
                elif L_2A[i,j,k] == max(max(a[i-1],L_1A[i-1,j]+w11)+T_f,L_2C_A[i-1,j,k]+w22):
                    L_record[0,i,j,k]=L_record[2,i-1,j,k]*10+2
                else:
                    L_record[0,i,j,k]=L_record[3,i-1,j,k]*10+3

                L_2B[i,j,k]=min(
                    max(max(b[j-1],L_1A[i,j-1]+w12)+T_f,
                    L_2A[i,j-1,k]+w21),
                    max(max(b[j-1],L_1B[i,j-1]+w11)+T_f,
                    L_2B[i,j-1,k]+w21),
                    min(max(max(b[j-1],L_1A[i,j-1]+w12)+T_f,
                    L_2C_A[i,j-1,k]+w22),
                    max(max(b[j-1],L_1B[i,j-1]+w11)+T_f,
                    L_2C_B[i,j-1,k]+w22))
                )
                if L_2B[i,j,k]==max(max(b[j-1],L_1A[i,j-1]+w12)+T_f,L_2A[i,j-1,k]+w21):
                    L_record[1,i,j,k]=L_record[0,i,j-1,k]*10
                elif L_2B[i,j,k]==max(max(b[j-1],L_1B[i,j-1]+w11)+T_f,L_2B[i,j-1,k]+w21):
                    L_record[1,i,j,k]=L_record[1,i,j-1,k]*10+1
                elif L_2B[i,j,k]==max(max(b[j-1],L_1A[i,j-1]+w12)+T_f,L_2C_A[i,j-1,k]+w22):
                    L_record[1,i,j,k]=L_record[2,i,j-1,k]*10+2
                else:
                    L_record[1,i,j,k]=L_record[3,i,j-1,k]*10+3

                L_2C_A[i,j,k]=min(max(c[k-1],L_2A[i,j,k-1]+w22),
                    max(c[k-1],L_2C_A[i,j,k-1]+w21))
                if L_2C_A[i,j,k]==max(c[k-1],L_2A[i,j,k-1]+w22):
                    L_record[2,i,j,k]=L_record[0,i,j,k-1]*10
                else:
                    L_record[2,i,j,k]=L_record[2,i,j,k-1]*10+2

                L_2C_B[i,j,k]=min(max(c[k-1],L_2B[i,j,k-1]+w22),
                    max(c[k-1],L_2C_B[i,j,k-1]+w21))
                if L_2C_B[i,j,k]==max(c[k-1],L_2B[i,j,k-1]+w22):
                    L_record[3,i,j,k]=L_record[1,i,j,k-1]*10+1
                else:
                    L_record[3,i,j,k]=L_record[3,i,j,k-1]*10+3
    
                
    result=min(min(L_2A[alpha,beta,gamma],L_2B[alpha,beta,gamma],L_2C_A[alpha,beta,gamma]),L_2C_B[alpha,beta,gamma])            
                
    if result==L_2A[alpha,beta,gamma]:
        num=int(L_record[0,alpha,beta,gamma]*10)
    elif result==L_2B[alpha,beta,gamma]:
        num=int(L_record[1,alpha,beta,gamma]*10+1)
    elif result==L_2C_A[alpha,beta,gamma]:
        num=int(L_record[2,alpha,beta,gamma]*10+2)
    else:
        num=int(L_record[3,alpha,beta,gamma]*10+3)
    print(result)
    str_rev=""
    while(num>=10):
        if num%10==0:
            str_rev+="A"
        elif num%10==1:
            str_rev+="B"
        elif num%10==2:
            str_rev+="C"
        else:
            str_rev+="C"
        num=int(num/10)
          
    str_rev=''.join(reversed(str_rev))
    print(str_rev)

if __name__ == '__main__':
    main()