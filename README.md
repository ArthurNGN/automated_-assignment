# rs-ibm

## INFO :

This is a WIP to build a RS to recommend films to users based on CI and user's ratings.

To try it, you just ahve to download/clone the repo, change the root_path located in the main.py var to fit your environment and call the main() function, it works straight out of the box.

## KEY CHANGES from V0 :

- advanced logging
- automatic join when providing several files with a common key
- automatic title transformation into a std format
- multi threading for faster parallel // triples from plot generation
- incremental triple generation (looks for and discards films already processed)
- produces only unique triples (removes duplicates)
- cleaned and improved workflow, everything called from a main()

## NEXT STEPS :

- Build a graph to represent nodes and relations
- POC with a mini RS pipeline ?
- explore KNN possibilities ?
