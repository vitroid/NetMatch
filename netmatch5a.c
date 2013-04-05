/*
netmatch5a -- netmatch5を、NetMatchライブラリを使って書きなおす。機能は同じ。

 *referenceグラフに完全一致する断片を、大きなネットワークの中から数えあげる。もしかしたら時間がかかりすぎるかもしれない。

2つの入力は共に無向グラフ
これで抽出したフラグメントの結合の向きを割りだすのはまた別のプログラムで行う。

出力の方法は未定。
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>
#include "NetMatch.h"
#include "Mark2.h"

int gzipopen(char* fileName, FILE** file)
{
    int gzip;
    int len = strlen( fileName );
    /*
     * ファイル名が.gzで終わる場合は圧縮ファイルとみなす
     */
    if ( 0 == strcmp( &fileName[len-3], ".gz" ) ){
        char cmd[1024];
        sprintf(cmd, "zcat %s", fileName );
        fputs(cmd,stderr);
        *file=popen(cmd,"r");
        gzip=1;
    }
    else{
        *file=fopen(fileName,"r");
        gzip=0;
    }
    return gzip;
}



int main(int argc,char *argv[])
{
  int i;
  int count=0;
  sMark2 *mref;
  FILE *file;
  sIntMatrix2 *ref;
  char buf[20000];

  if((argc!=3)&&(argc!=4)){
    fprintf(stderr,"usage: %s refstruc struc [MaxDiff]\n",argv[0]);
    fprintf(stderr,"structures must be in format @DMTX or @NGPH\n");
    exit(1);
  }
  if(argc==4){
    BestResult = atoi(argv[3]);
  }else{
    /*extract the exact shape only*/
    BestResult = 0;
  }
  /*最初は参照ネットワークフラグメント*/
  int gzip = gzipopen( argv[1], &file );

  while(NULL!=fgets(buf,sizeof(buf),file)){
    if(0==strncmp(buf,"@DMTX",5)){
      ref=IntMatrix2_LoadDMTX(file);
      break;
    }
    if(0==strncmp(buf,"@NGPH",5)){
      ref=IntMatrix2_LoadNGPH(file);
      break;
    }
  }
  if ( gzip )
      pclose( file );
  else
      fclose(file);
  fprintf(stderr,"%d\tMaxDiff\n",BestResult );
  
  mref=Mark2_New(ref->n);
  Mark2_Occupy(mref,0);
  MarkRim(mref,ref,0);
  /*ref側ははじめから順番を決めておく。*/
  while(Mark2_RStackSize(mref)){
      i=Mark2_RStack(mref,0);
      Mark2_Occupy(mref,i);
      MarkRim(mref,ref,i);
  }
  gzip = gzipopen( argv[2], &file );
  while(NULL!=fgets(buf,sizeof(buf),file)){
      sIntMatrix2* big = NULL;
      if(0==strncmp(buf,"@DMTX",5))
          big = IntMatrix2_LoadDMTX(file);
      if(0==strncmp(buf,"@NGPH",5))
          big = IntMatrix2_LoadNGPH(file);
      if( big ){
          sMark2* mbig = Mark2_New(big->n);
          fprintf(stderr,"[%d]",count++);
          printf("@FRAG\n%d %d\n",ref->n,big->n);
          for(i=0;i<big->n;i++){
              Mark2_Occupy(mbig,i);
              MarkRim(mbig,big,i);
              Enumerate(ref,mref,big,mbig,0);
              Mark2_Unoccupy(mbig,i);
              UnmarkRim(mbig,big,i);
          }
          IntMatrix2_Done(big);
          Mark2_Done(mbig);
          for(i=0;i<ref->n;i++){
              printf("-1 ");
          }
          printf("\n");
      }
  }
  if ( gzip )
      pclose( file );
  else
      fclose( file );
  exit(0);
}
