#include<iostream>  
#include<fstream>

using namespace std;  

 void function(int m);  
 int canplace(int row,int col,int c);  
 void outputresult(); 
 //int maxm = 0; 
 int a[9][9];

  


 int main()  {
	int i,j;
	ifstream infile;
	infile.open("soduku.txt");
	if(!infile.is_open()){
		cout<<"cannot open file"<<endl;
	}

	for(i=0;i<9;i++){
		for(j=0;j<9;j++){
			infile>>a[i][j];
        }
    }
    
    function(0);  
    return 0;  
 }  



 void function(int m) { 
    int i,row, col;
	int p=0;
   	
	
	if (m>=81)  { 
        	
		outputresult();
		
		
	
	}  
    else {  
		row = m / 9;  
        col = m % 9;  
        if(a[row][col] != 0) { 
        function(m+1); 
} 
    for(i = 1; i <= 9; i++){  
		if(canplace(row,col,i) == 1){  
			a[row][col] = i;  
            function(m + 1);  
            a[row][col] = 0;  
			}  
        }  
    } 
}


int canplace(int row,int col,int c) {  
    int i, j; 
    int flag = 1;  
    for(i = 0; i < 9; i++ ){  
       if(a[row][i] == c || a[i][col] == c) {  
           flag = 0;  
		   break;  
    }  
} 

	if(flag != 0) { 
	    for(i = (row / 3) * 3; i < (row / 3) * 3 + 3; i++){  
		    for(j = (col / 3) * 3; j < (col / 3) * 3 + 3; j++){  
				if(a[i][j] == c){  
					flag = 0;  
						break;  
    }  
}  

		if(flag == 0) { 
				break; 
        } 
    } 
} 
	return flag;  
}  


 void outputresult() {
	
	 for( int i = 0; i < 9; i++ ){
        for( int j = 0; j < 9; j++ ){
            cout << a[i][j] << " ";
			}
        cout << endl;
    }
    cout << endl;
	
	
 }