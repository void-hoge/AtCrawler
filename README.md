# AtCrawler
- A crawling tool for submitted codes of AtCoder.

## install
- `git clone https://github.com/void-hoge/AtCrawler`
- `cd AtCrawler`
- `pip install -e .`

## usage
```
usage: atcrawler [-h] [--username USERNAME] [--language LANGUAGE]
                 [--task {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}] [--result RESULT]
                 [--orderby {created,score,source_length,time_consumption,memory_consumption}] [--desc DESC]
                 [--maxsubmissions MAXSUBMISSIONS]
                 {init,crawl} contest

positional arguments:
  {init,crawl}          Specify the mode, (init: inintialize environment, crawl: initialize environment and
                        download submissions)
  contest               Specify the contest name.

options:
  -h, --help            show this help message and exit
  --username USERNAME, -u USERNAME
                        When crawl mode, specify the author.
  --language LANGUAGE, -l LANGUAGE
                        When crawl mode, specify the language.
  --task {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}, -t {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}
                        When crawl mode, specify the task (a-z).
  --result RESULT, -r RESULT
                        When crawl mode, specify the submission result.
  --orderby {created,score,source_length,time_consumption,memory_consumption}, -o {created,score,source_length,time_consumption,memory_consumption}
                        When crawl mode, specify the order.
  --desc DESC, -d DESC  When crawl mode, set when descending order.
  --maxsubmissions MAXSUBMISSIONS, -m MAXSUBMISSIONS
                        When crawl mode, the max submissions number.
```

## author
- MugiNoda (void-hoge)

## lisence
- GPL v3
