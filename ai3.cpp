#include<stdio.h>
#include <bits/stdc++.h>
#include<queue>
#include<map>
using namespace std;
extern "C"{
char arr[10],brr[10]="123804765";
char mapp[1005] = {-1};
int steps = 0, number[1005], cur = 0;
struct node{
	int num,step,cost,zeroPos,way;
	bool operator<(const node &a)const{
		return cost>a.cost;
	}
	node(int n,int s,int p){
		num=n,step=s,zeroPos=p;
		way = -1;
		setCost();
	}
	void setCost(){
		char a[10];
		int c=0;
		sprintf(a,"%09d",num);
		for(int i=0;i<9;i++)
			if(a[i]!=brr[i])
				c++;
		cost=c+step;
	}
	void setWay(int i) {
		way = i;
	}
	void printWay() {
		//if(way!=-1)
		printf("%d\n",zeroPos);
		cur += 1;
		number[cur] = zeroPos;
	}
};
int des=123804765;
int changeId[9][4]={{-1,-1,3,1},{-1,0,4,2},{-1,1,5,-1},//{-1，-1，3，1}表示在九宫格的第一行第一列那个位置（0），
														//不能往左往上（-1），往右就是位置（1），往下便是位置（3）;同理后面几项
					{0,-1,6,4},{1,3,7,5},{2,4,8,-1},
					{3,-1,-1,7},{4,6,-1,8},{5,7,-1,-1}};
map<int,bool>mymap;
priority_queue<node> que;//优先级队列 
void swap(char* ch,int a,int b){char c=ch[a];ch[a]=ch[b];ch[b]=c;}
int bfsHash(int start,int zeroPos){//start是原始棋盘的数字表示，zeroPos是0所在位置
	int first = 1;
	int lastNode = -1;//定义前一个节点位置
	char temp[10];
	node tempN(start,0,zeroPos);//创建一个节点 
	que.push(tempN);//压入优先级队列 
	mymap[start]=1;//标记开始节点被访问过 
	while(!que.empty()){
		tempN=que.top();
		int thisNode = tempN.zeroPos;
		que.pop();//弹出一个节点
		if (first) {
			tempN.printWay();
			first = 0;
		}
		else {
			int ind = cur-1;
			lastNode = number[ind];
			//int legalFlag = 0;
			for (int i = 0; i < 4; i++) {  //如果上一个节点到这个节点是不可一步到达的，就不输出（该点不合法
				if (changeId[lastNode][i] == thisNode) {
				//	legalFlag = 1;
					tempN.printWay();
					//printf("lastNode:%d\n",lastNode);
					//printf("thisNode:%d\n",thisNode);
				}
			}
		}
		sprintf(temp,"%09d",tempN.num);//把num从数字变成字符数组temp
		int pos=tempN.zeroPos,k;
		for(int i=0;i<4;i++){
			if(changeId[pos][i]!=-1){//看0位置pos的上下左右
				swap(temp,pos,changeId[pos][i]);
				sscanf(temp,"%d",&k);//把字符数组temp又变成数字k
				if(k==des)return tempN.step+1;
				if(mymap.count(k)==0){
					node tempM(k,tempN.step+1,changeId[pos][i]);
					// i=0 -> up; i=1 -> left; i=2 -> down; i=3 -> right;
					
					tempM.setWay(i);
					que.push(tempM);//创建一个新节点并压入队列 
					mymap[k]=1;
				}
				swap(temp,pos,changeId[pos][i]);//交换回来
			}
		}
	}
}
char* _main(char *input){
	int n,k,b;
	//scanf("%s",arr);	
	int o = 0;	
	printf("%s\n",input);
	while(input[o])	
	{
		arr[o] = input[o];
		o++;		
		//printf("%d",input[o++]);	
	}	
	arr[o]='\0';
	printf("aaaaa is %s\n",arr);	
	for(k=0;k<9;k++)
		if(arr[k]=='0')break;//k指向0所在的位置
	sscanf(arr,"%d",&n);//n是原始棋盘位置的数字表示
	if(n==des){
		printf("0\n");
		return 0;
	}
	b=bfsHash(n,k);
	printf("%d\n",b);
	//o=0;	
	//while(o<4){
	//printf("\nnumber{%d}:%d",o,number[o]);o++;}
	//cout<<typeid(number).name();	
	char buff[10];
	static char astring[500];
 	int i;
	astring[0]='\0';
 	for(i=0;i<cur;i++)
   	{
      		sprintf(buff,"%d",number[i]);
      		strcat(astring,buff);
   	}
 	//printf("%s\n",astring);	
	



	return (char*)astring;	
}
}


