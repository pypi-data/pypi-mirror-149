a="""//Expt1insertionSort.c
#include<stdio.h>
#include<stdlib.h>
 voidprintArray(intarray[],intsize){
 for(inti=0;i<size;i++){
printf("%d",array[i]);
}
printf("\n");
}
voidinsertionSort(intarray[],intsize){
for(intj=1;j<size;j++){
intkey=array[j];
inti=j-1;

while(key<array[i]&&i>=0){
array[i+1]=array[i];
--i;
}
array[i+1]=key;
}
}
intmain(){
intsize,*Arr;
printf("Entersizeofarray:");
scanf("%d",&size);
Arr=(int*)malloc(size*sizeof(int));
printf("Enterelementofarray:");
for(inti=0;i<size;i++)
scanf("%d",&Arr[i]);
insertionSort(Arr,size);
printf("Sortedarrayinascendingorder:\n");
printArray(Arr,size);
}




//Expt2SelectionSort
#include<stdio.h>
#include<stdlib.h>

voidprintArray(intarray[],intsize){
for(inti=0;i<size;++i){
printf("%d",array[i]);
}
printf("\n");
}

voidswap(int*a,int*b){
inttemp=*a;
*a=*b;
*b=temp;
}

voidselectionSort(intarray[],intsize){
for(intstep=0;step<size-1;step++){
intmin_idx=step;
for(inti=step+1;i<size;i++){
if(array[i]<array[min_idx])
min_idx=i;
}
swap(&array[min_idx],&array[step]);
}
}

intmain(){
intsize,*Arr;
printf("Entersizeofarray:");
scanf("%d",&size);
Arr=(int*)malloc(size*sizeof(int));
printf("Enterelementofarray:");
for(inti=0;i<size;i++)
scanf("%d",&Arr[i]);
selectionSort(Arr,size);
printf("SortedarrayinAcsendingOrder:\n");
printArray(Arr,size);
}

//Expt3QuickSort
#include<stdio.h>
#include<stdlib.h>

voidprintArray(intarray[],intsize){
for(inti=0;i<size;++i){
printf("%d",array[i]);
}
printf("\n");
}

voidswap(int*a,int*b){
intt=*a;
*a=*b;
*b=t;
}

intpartition(intarray[],intlow,inthigh){
intpivot=array[high];
inti=(low-1);

for(intj=low;j<high;j++){
if(array[j]<=pivot){
i++;
swap(&array[i],&array[j]);
}
}
swap(&array[i+1],&array[high]);
return(i+1);
}

voidquickSort(intarray[],intlow,inthigh){
if(low<high){
intmid=partition(array,low,high);
quickSort(array,low,mid-1);
quickSort(array,mid+1,high);
}
}

intmain(){
intsize,*Arr;
printf("Entersizeofarray:");
scanf("%d",&size);
Arr=(int*)malloc(size*sizeof(int));
printf("Enterelementofarray:");
for(inti=0;i<size;i++)
scanf("%d",&Arr[i]);

printf("UnsortedArray\n");
printArray(Arr,size);

quickSort(Arr,0,size-1);
printf("Sortedarrayinascendingorder:\n");
printArray(Arr,size);
}

//Expt4Maxmin_dac.c
#include<stdio.h>
#include<stdlib.h>

structpair{
intmin,max;
};

structpairgetMaxMin(intArr[],intlow,inthigh){
structpairmaxmin;
if(low==high){
maxmin.min=maxmin.max=Arr[low];
}elseif(low==high-1){
if(Arr[low]<Arr[high]){
maxmin.min=Arr[low];
maxmin.max=Arr[high];
}else{
maxmin.min=Arr[high];
maxmin.max=Arr[low];
}
}else{
intmid=(low+high)/2;
structpairLeft=getMaxMin(Arr,low,mid);
structpairRight=getMaxMin(Arr,mid+1,high);

if(Left.max>Right.max){
maxmin.max=Left.max;
}else{
maxmin.max=Right.max;
}
if(Left.min<Right.min){
maxmin.min=Left.min;
}else{
maxmin.min=Right.min;
}
}
returnmaxmin;
}

intmain(){
intsize,*Arr;
size:
printf("Entersizeofarray:");
scanf("%d",&size);
if(size<1){
printf("Error:Sizeofarraycannotbelessthan1!\n");
gotosize;
}
Arr=(int*)malloc(size*sizeof(int));
printf("Enterelementofarray:");
for(inti=0;i<size;i++)
scanf("%d",&Arr[i]);
printf("\n");
structpairmaxmin=getMaxMin(Arr,0,size-1);
printf("Minimumelementis%d\n",maxmin.min);
printf("Maximumelementis%d\n",maxmin.max);
}



//Expt5prim_mcst.c
#include<stdio.h>

#defineINF999999

voidprim_mst(intcost[10][10],intn){
intvisited[10]={0},no_e=1,min_cost=0;
intmin,a,b;

printf("\n");
visited[1]=1;

printf("MSTPath:\n");

while(no_e<n){
min=INF;
for(inti=1;i<=n;i++){
for(intj=1;j<=n;j++){
if(cost[i][j]<min){
if(visited[i]!=0){
min=cost[i][j];
a=i;
b=j;
}
}
}
}

if(visited[b]==0){
printf("%dto%dcost=%d\n",a,b,min);
min_cost=min_cost+min;
no_e++;
}

visited[b]=1;
cost[a][b]=cost[b][a]=INF;
}

printf("\nMSTMinimumcostis%d\n",min_cost);
}

intmain(){
intcost[10][10],n;
printf("Enternumberofnodes:");
scanf("%d",&n);
printf("Entercostinformofadjacencymatrix:\n");

for(inti=1;i<=n;i++){
for(intj=1;j<=n;j++){
scanf("%d",&cost[i][j]);
if(cost[i][j]==0)
cost[i][j]=INF;
}
}

prim_mst(cost,n);
return0;
}


//Expt6fractional_knapsack.c
#include<stdio.h>
#include<stdlib.h>

structitems{
	charname[20];
	floatweight;
	floatprofit;
	floatratio;
	floatfraction;
};

voidknapsack(unsignedintn,structitemsobject[],floatcapacity){
	floattotal_profit=0;
	unsignedinti;

	for(i=0;i<n;i++){
		if(object[i].weight>capacity){
			break;
		}else{
			object[i].fraction=1.0;
			total_profit+=object[i].profit;
			capacity-=object[i].weight;
		}
	}

if(i<n)
		object[i].fraction=capacity/object[i].weight;

total_profit+=(object[i].fraction*object[i].profit);

	printf("==========PrintingResults==========\n");
	printf("Totalprofit=%.2f\n",total_profit);
	printf("Orderofitemswiththeir%%=");
	for(i=0;i<n;i++){
		if(i==n-1)
printf("%s(%.2f%%).\n",object[i].name,object[i].fraction*100);
else
printf("%s(%.2f%%)-->",object[i].name,object[i].fraction*100);

}
}

intmain(void){
	floatcapacity;
	printf("Enterbag'scapacity:");
	scanf("%f",&capacity);

	unsignedintn;
	printf("Entertotalnumberofitems:");
	scanf("%d",&n);

	structitemsitem[n];

for(unsignedinti=0;i<n;i++){
		printf("==========ItemNo%d==========\n",i+1);
printf("ItemName:");
		scanf("%s",item[i].name);
		printf("Weight:");
		scanf("%f",&item[i].weight);
		printf("Profit:");
		scanf("%f",&item[i].profit);
	}

	for(unsignedinti=0;i<n;i++){
		item[i].ratio=item[i].profit/item[i].weight;
		item[i].fraction=0.0;
	}

	for(unsignedinti=0;i<n;i++){
		for(unsignedintj=i+1;j<n;j++){
			if(item[i].ratio<item[j].ratio){
				structitemstemp=item[i];
				item[i]=item[j];
				item[j]=temp;
			}
		}
	}

	knapsack(n,item,capacity);

	return0;
}


//expt7floyd_warshall.c
#include<stdio.h>
#include<stdlib.h>

#defineV6
#defineINF999999

voidprintSolution(intdist[][V])
{
	for(inti=0;i<V;i++){
		for(intj=0;j<V;j++){
			if(dist[i][j]>=(INF%10))
				printf("%7s","INF");
			else
				printf("%7d",dist[i][j]);
		}
		printf("\n");
	}
}

voidfloydWarshall(intgraph[][V]){
	intdist[V][V],i,j,k;

	for(i=0;i<V;i++)
		for(j=0;j<V;j++)
			dist[i][j]=graph[i][j];

	for(k=0;k<V;k++){
		for(i=0;i<V;i++){
			for(j=0;j<V;j++){
				if(dist[i][k]+dist[k][j]<dist[i][j])
					dist[i][j]=dist[i][k]+dist[k][j];
			}
		}
	}

	printSolution(dist);
}

intmain(){
/*Testcase1*/
intgraph[V][V]={
{0,INF,INF,INF,-1,INF},
	{1,0,INF,2,INF,INF},
	{INF,2,0,INF,INF,-8},
{-4,INF,INF,0,3,INF},
{INF,7,INF,INF,0,INF},
{INF,5,10,INF,INF,0}
	};

/*Testcase2
intgraph[V][V]={
{0,8,5},
	{2,0,INF},
	{INF,1,0},
	};
*/

printf("Givengraphmatrixis:\n");
printSolution(graph);

printf("\nShortestpathmatrixusingFloydWarshall'salgorithmis:\n");
floydWarshall(graph);
	return0;
}


//Expt8longestcommonsubsequencelsc.c
#include<stdio.h>
#include<string.h>

#defineMAX20
charB[MAX][MAX];

voidprint_lcs(char*X,char*Y,inti,intj)
{

if(i==0||j==0)
return;

if(B[i][j]=='d')
{
print_lcs(X,Y,i-1,j-1);
printf("%c",X[i-1]);
}
elseif(B[i][j]=='u')
print_lcs(X,Y,i-1,j);
else
print_lcs(X,Y,i,j-1);

}

voidlcs(char*X,char*Y,intm,intn)
{
intC[m+1][n+1];
inti,j;

for(i=0;i<=m;i++)
C[i][0]=0;

for(i=0;i<=n;i++)
C[0][i]=0;

for(i=1;i<=m;i++)
for(j=1;j<=n;j++)
{
if(X[i-1]==Y[j-1])
{
C[i][j]=C[i-1][j-1]+1;
B[i][j]='d';
}
elseif(C[i-1][j]>=C[i][j-1])
{
C[i][j]=C[i-1][j];
B[i][j]='u';
}
else

{
C[i][j]=C[i][j-1];
B[i][j]='l';
}
}

printf("LCSof%sand%sis",X,Y);
print_lcs(X,Y,m,n);
printf("\n");
}

intmain()
{
charX[MAX],Y[MAX];
intm,n;

printf("Enter1stsequence:");
scanf("%s",X);

printf("Enter2ndsequence:");
scanf("%s",Y);

m=strlen(X);
n=strlen(Y);

lcs(X,Y,m,n);

return0;
}


//Expt9nqueen.c
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
intboard[20],count;

voidprint(intn){
	inti,j;
	printf("\n\nSolution%d:\n\n",++count);
	for(i=1;i<=n;++i)
		printf("\t%d",i);
	for(i=1;i<=n;++i){
		printf("\n\n%d",i);
		for(j=1;j<=n;++j){
			if(board[i]==j)
			printf("\tQ");
			else
			printf("\t-");
		}
	}
	
}

intplace(introw,intcol){
	inti;

	for(i=1;i<=row-1;++i){
	if((board[i]==col)||(abs(board[i]-col)==abs(i-row)))
		return0;
	}
	return1;
}

voidqueen(introw,intn)
{
	intcol;
	for(col=1;col<=n;++col){
		if(place(row,col)){
			board[row]=col;
			if(row==n)
				print(n);
			else
				queen(row+1,n);
		}
	}
}

intmain(){
	intn,i,j;
	printf("EnternumberofQueens:");
	scanf("%d",&n);
	queen(1,n);
	printf("\n");
	return0;
}


//Expt10sumofsubest.c
#include<stdio.h>
#defineTRUE1
#defineFALSE0

intinc[50],w[50],sum,n,set_found=0;

voidsumset(int,int,int);

intpromising(inti,intwt,inttotal){
	return(((wt+total)>=sum)&&((wt==sum)||(wt+w[i+1]<=sum)));
}

intmain(){
	inti,j,n,temp,total=0;
	printf("Enterhowmanynumbers:");
	scanf("%d",&n);
	printf("\nEnter%dnumberstotheset:",n);
	for(i=0;i<n;i++){
		scanf("%d",&w[i]);
		total+=w[i];
	}
	printf("\nInputthesumvaluetocreatesubset:");
	scanf("%d",&sum);
	for(i=0;i<=n;i++)
		for(j=0;j<n-1;j++)
			if(w[j]>w[j+1]){
				temp=w[j];
				w[j]=w[j+1];
				w[j+1]=temp;
			}

	if((total<sum)){
		printf("\nSubsetconstructionisnotpossible.\n");
	}else{
		for(i=0;i<n;i++)
			inc[i]=0;
		sumset(-1,0,total);
		if(set_found==0)
			printf("Nofeasiblesetsolution.\n");
		else
			printf("\n");
	}
	return0;
}
voidsumset(inti,intwt,inttotal){
	intj;
	if(promising(i,wt,total)){
		if(wt!=sum){
			inc[i+1]=TRUE;
			sumset(i+1,wt+w[i+1],total-w[i+1]);
			inc[i+1]=FALSE;
			sumset(i+1,wt,total-w[i+1]);
		}else{
			if(set_found==0)
				printf("Thesolutionusingbacktrackingis:");
			else
				printf(",");
			
			printf("{");
			for(j=0;j<=i;j++)
				if(inc[j])
					printf("%d",w[j]);
			printf("}");
			set_found=1;
		}
	}
}



//Expt11naive_str_mat.c
#include<stdio.h>
#include<string.h>

#definemax20

voidsearch(char*pat,char*txt)
{
	intM=strlen(pat);
	intN=strlen(txt);

	for(inti=0;i<=N-M;i++){
		intj;

		for(j=0;j<M;j++)
			if(txt[i+j]!=pat[j])
				break;

		if(j==M)
			printf("Patternfoundatindex%d\n",i);
	}
}

intmain()
{
	chartxt[max],pat[max];
	printf("Entertextstring:");
	scanf("%s",txt);

	printf("Enterpatterntosearch:");
	scanf("%s",pat);
	
	search(pat,txt);
	return0;
}



//Expt12kmp_str_mat.c
#include<stdio.h>
#include<string.h>
#include<stdlib.h>

intpat_f=0;

voidKMP(char*X,char*Y,intm,intn){
	if(*Y=='\0'||n==0)
		printf("Thepatternoccurswithlengthzero");

	if(*X=='\0'||n>m)
		printf("Patternnotfound");

	intnext[n+1];

	for(inti=0;i<n+1;i++)
		next[i]=0;

	for(inti=1;i<n;i++){
		intj=next[i+1];

		while(j>0&&Y[j]!=Y[i])
			j=next[j];

		if(j>0||Y[j]==Y[i])
			next[i+1]=j+1;
	}

	for(inti=0,j=0;i<m;i++){
		if(*(X+i)==*(Y+j)){
			if(++j==n){
				pat_f=1;
				printf("Thepatternoccurswithindex%d\n",i-j+1);
			}
		}elseif(j>0){
			j=next[j];
			i--;
		}
	}
	
	if(pat_f!=1)
		printf("Thepatterncouldnotbefound\n");
}

intmain(){
	chartext[50],pattern[25];

	printf("Enterthemaintext:");
	scanf("%[^\n]%*c",text);

	printf("Enterthepatterntextyouwanttosearch:");
	scanf("%[^\n]%*c",pattern);

	KMP(text,pattern,strlen(text),strlen(pattern));
	return0;
})


//Expt 13 : Linear Search 
/*
 * C program to input N numbers and store them in an array.
 * Do a linear search for a given key and report success
 * or failure.
 */
#include <stdio.h>
 
void main()
{  int num;
 
    int i,  keynum, found = 0;
 
    printf("Enter the number of elements ");
    scanf("%d", &num);
    int array[num];
    printf("Enter the elements one by one \n");
    for (i = 0; i < num; i++)
    {
        scanf("%d", &array[i]);
    }
 
    printf("Enter the element to be searched ");
    scanf("%d", &keynum);
    /*  Linear search begins */
    for (i = 0; i < num ; i++)
    {
        if (keynum == array[i] )
        {
            found = 1;
            break;
        }
    }
    if (found == 1)
        printf("Element is present in the array at position %d",i+1);
    else
        printf("Element is not present in the array\n");
} 

// Expt 14  /* C program for Merge Sort */
#include <stdio.h>
#include <stdlib.h>

// Merges two subarrays of arr[].
// First subarray is arr[l..m]
// Second subarray is arr[m+1..r]
void merge(int arr[], int l, int m, int r)
{
	int i, j, k;
	int n1 = m - l + 1;
	int n2 = r - m;

	/* create temp arrays */
	int L[n1], R[n2];

	/* Copy data to temp arrays L[] and R[] */
	for (i = 0; i < n1; i++)
		L[i] = arr[l + i];
	for (j = 0; j < n2; j++)
		R[j] = arr[m + 1 + j];

	/* Merge the temp arrays back into arr[l..r]*/
	i = 0; // Initial index of first subarray
	j = 0; // Initial index of second subarray
	k = l; // Initial index of merged subarray
	while (i < n1 && j < n2) {
		if (L[i] <= R[j]) {
			arr[k] = L[i];
			i++;
		}
		else {
			arr[k] = R[j];
			j++;
		}
		k++;
	}

	/* Copy the remaining elements of L[], if there
	are any */
	while (i < n1) {
		arr[k] = L[i];
		i++;
		k++;
	}

	/* Copy the remaining elements of R[], if there
	are any */
	while (j < n2) {
		arr[k] = R[j];
		j++;
		k++;
	}
}

/* l is for left index and r is right index of the
sub-array of arr to be sorted */
void mergeSort(int arr[], int l, int r)
{
	if (l < r) {
		// Same as (l+r)/2, but avoids overflow for
		// large l and h
		int m = l + (r - l) / 2;

		// Sort first and second halves
		mergeSort(arr, l, m);
		mergeSort(arr, m + 1, r);

		merge(arr, l, m, r);
	}
}

/* UTILITY FUNCTIONS */
/* Function to print an array */
void printArray(int A[], int size)
{
	int i;
	for (i = 0; i < size; i++)
		printf("%d ", A[i]);
	printf("\n");
}

/* Driver code */
int main()
{
	int arr[] = { 12, 11, 13, 5, 6, 7 };
	int arr_size = sizeof(arr) / sizeof(arr[0]);

	printf("Given array is \n");
	printArray(arr, arr_size);

	mergeSort(arr, 0, arr_size - 1);

	printf("\nSorted array is \n");
	printArray(arr, arr_size);
	return 0;
}


// Binary Search 
// C program to implement recursive Binary Search
#include <stdio.h>

// A recursive binary search function. It returns
// location of x in given array arr[l..r] is present,
// otherwise -1
int binarySearch(int arr[], int l, int r, int x)
{
	if (r >= l) {
		int mid = l + (r - l) / 2;

		// If the element is present at the middle
		// itself
		if (arr[mid] == x)
			return mid;

		// If element is smaller than mid, then
		// it can only be present in left subarray
		if (arr[mid] > x)
			return binarySearch(arr, l, mid - 1, x);

		// Else the element can only be present
		// in right subarray
		return binarySearch(arr, mid + 1, r, x);
	}

	// We reach here when element is not
	// present in array
	return -1;
}

int main(void)
{
	int arr[] = { 2, 3, 4, 10, 40 };
	int n = sizeof(arr) / sizeof(arr[0]);
	int x = 10;
	int result = binarySearch(arr, 0, n - 1, x);
	(result == -1)
		? printf("Element is not present in array")
		: printf("Element is present at index %d", result);
	return 0;
}
// Linear Search Algo 
#include <stdio.h>

// Recursive function to search x in arr[]
int elmntSrch(int arr[], int size, int x) {
	int rec;

	size--;

	if (size >= 0) {
		if (arr[size] == x)
			return size;
		else
			rec = elmntSrch(arr, size, x);
	}
	else
		return -1;

	return rec;
}

int main(void) {
	int arr[] = {12, 34, 54, 2, 3};
	int size = sizeof(arr) / sizeof(arr[0]);
	int x = 3;
	int indx;

	indx = elmntSrch(arr, size, x);

	if (indx != -1)
		printf("Element %d is present at index %d", x, indx);
	else
		printf("Element %d is not present", x);

	return 0;
}
// Min Max Minimum cost spanning tree 
#include <stdio.h>
    #include <conio.h>
    #include <stdlib.h>
    int i,j,k,a,b,u,v,n,ne=1;
    int min,mincost=0,cost[9][9],parent[9];
    int find(int);
    int uni(int,int);
    void main()
    {
    	printf("\n\tImplementation of Kruskal's Algorithm\n");
    	printf("\nEnter the no. of vertices:");
    	scanf("%d",&n);
    	printf("\nEnter the cost adjacency matrix:\n");
    	for(i=1;i<=n;i++)
    	{
    	for(j=1;j<=n;j++)
    	{
    	scanf("%d",&cost[i][j]);
    	if(cost[i][j]==0)
    	cost[i][j]=999;
    	}
    	}
    	printf("The edges of Minimum Cost Spanning Tree are\n");
    	while(ne < n)
    	{
    	for(i=1,min=999;i<=n;i++)
    	{
    	for(j=1;j <= n;j++)
    	{
    	if(cost[i][j] < min)
    	{
    	min=cost[i][j];
    	a=u=i;
    	b=v=j;
    	}
    	}
    	}
    	u=find(u);
    	v=find(v);
    	if(uni(u,v))
    	{
    	printf("%d edge (%d,%d) =%d\n",ne++,a,b,min);
    	mincost +=min;
    	}
    	cost[a][b]=cost[b][a]=999;
    	}
    	printf("\n\tMinimum cost = %d\n",mincost);
    	getch();
    }
    int find(int i)
    {
    	while(parent[i])
    	i=parent[i];
    	return i;
    }
    int uni(int i,int j)
    {
    	if(i!=j)
    	{
    	parent[j]=i;
    	return 1;
    	}
    	return 0;
    }
	/* Implementation of Min Max Algorithm */

#include <stdio.h>

int min(int a, int b)
{
    if (a < b)
    {
        return a;
    }
    else
    {
        return b;
    }
}
int max(int a, int b)
{
    if (a < b)
    {
        return b;
    }
    else
    {
        return a;
    }
}
int findMinRec(int A[], int n)
{
    // if size = 0 means whole array has been traversed
    if (n == 1)
        return A[0];
    return min(A[n - 1], findMinRec(A, n - 1));
}
int findMaxRec(int A[], int n)
{
    // if n = 0 means whole array has been traversed
    if (n == 1)
        return A[0];
    return max(A[n - 1], findMaxRec(A, n - 1));
}
int main()
{

    int A[] = {3, 5, 1, -2,73793, 99};
    int n = sizeof(A) / sizeof(A[0]);
    printf("Max element: %d\n", findMaxRec(A, n));
    printf("Min element: %d\n", findMinRec(A, n));
    return 0;
}
"""
print(a)

