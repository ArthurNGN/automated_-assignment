# rs-ibm

## INFO :

This is a WIP to build a RS to recommend films to users based on CI and user's ratings

## KEY CHANGES from V0 :

- advanced logging
- automatic join when providing several files with a common key
- automatic title transformation into a std format
- multi threading for faster // triples from generation
- incremental triple generation (looks for and discards films already processed)
- produces only unique triples (removes duplicates)
- cleaned and improved workflow, everything called from a main()

To try it, you can just download/clone the repo and call the main() in terminal, it works straight out of the box.

## NEXT STEPS :

- Build a graph to represent nodes and relations
- POC with a mini RS ?
- explore KNN possibilities ?
