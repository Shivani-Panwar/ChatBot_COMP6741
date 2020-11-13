from rdflib import Graph
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
            
#doc=nlp("What is the POLI 495 about?")
g=Graph()
g.parse("output_graph_all_courses_only_manual_topics.ttl",format="turtle")
g.parse("projectexample1.ttl",format="turtle")
#bot = aiml_bot.Bot(learn="myBot.aiml")

question=10
print("Hello! I am the university Bot. What do you want to know?\n")
flag=True
while flag :
      question=10
      user_input=input("> ")
      doc=nlp(user_input)
      query_input=""
      course_number=""
      
      for t in doc:
          if t.pos_=="NUM":
              question=1
              course_number=str(t)
              break
          elif t.pos_=="VERB" and str(t) in ["take","taken","took", "enrolled", "enroll", "study", "studies"]:
              question=2
              break
          elif (t.pos_=="VERB" and str(t) in ["cover","covered", "covers", "include"]) or (t.pos_=="AUX" and str(t) in ["has","have"]):
              question=3
              break
          elif (t.pos_=="PRON" and str(t) in ["Who", "who"]):
              question=4
              break
          elif (t.pos_=="VERB" and str(t) in ["know","knows","known"]):
              question=5  
              break
          
      for t in doc:
          if t.pos_=="PROPN" or (t.pos_=="NOUN" and (t.dep_=="dobj" or t.dep_=="compound" or t.dep_=="nsubj" or t.dep_=="pobj" or t.dep_=="nsubjpass") and str(t)!="courses"):
              query_input=query_input+" "+str(t)
              
      #What is the POLI 495 about?   
      query_input=query_input.strip()
      if question==1:
                quer1=g.query("""SELECT DISTINCT ?cd 
        		WHERE{   
        				?c rdf:subject '"""+query_input+"""'.
                        ?c rdf:value '"""+course_number+"""'.
        				?c rdf:type focu:Course.
                        ?c rdfs:comment ?cd.
                        }""")
                if len(quer1)!=0:
                    print(query_input + " " + course_number + " description:")
                    for row in quer1:
                        print(row["cd"])
                else:
                    print("Concordia does not offer such a course!")
        #Which courses did Sharon take?           
      elif question==2:
              quer2 = g.query("""SELECT ?g (strafter(str(?sub), "#") as ?name) ?title ?term
        		WHERE{
        				?s foaf:name '"""+query_input+"""'.
                        ?s focu:completed ?sub.
                        ?st rdf:type rdf:Statement.
                        ?st focu:gradeObtained ?g.
                        ?st rdf:subject ?s.
                        ?st rdf:object ?sub.
                        ?st focu:attendedIn ?term.
                        ?sub rdf:type focu:Course.
                        ?sub foaf:name ?title.
                        }""")
              if len(quer2)!=0:
                    print("Courses completed by "+query_input+":")
                    for row in quer2:
                       print("Course: "+row["name"].replace("_",' ')+" - "+row["title"].strip()+"| Grade, Term: "+row["g"]+", "+row["term"])
              else:
                    print(query_input+" did not take any course yet!")
       #Which courses cover cinematography?   
      elif question==3: 
              quer3 =  g.query("""SELECT DISTINCT (strafter(str(?c), "#") as ?course) ?cn 
    		        WHERE{   
    				?t foaf:name '"""+query_input+"""'.
                    ?t rdf:type focu:Topic.
                    ?c focu:includes ?t.
                    ?c rdf:subject ?sub.
    				?c rdf:type focu:Course.
                    ?c foaf:name ?cn.
                    }""")
              if len(quer3)!=0:
                    print("The following courses cover "+ query_input+":")
                    for row in quer3:
                        print(row["course"].replace("_",' ')+" - "+row["cn"].strip())
              else:
                    print(query_input+" is not covered by any course!")
       #Who is familiar with web services?             
      elif question==4:
          quer4=g.query("""SELECT DISTINCT (strafter(str(?s), "#") as ?sname) WHERE{   
                        ?t rdf:type focu:Topic.
                       ?t foaf:name '"""+query_input+"""'.
                       ?c focu:includes ?t.
                       ?st rdf:type rdf:Statement.
                       ?st focu:gradeObtained ?g.
                       ?st rdf:subject ?s.
                       ?st rdf:object ?c.
                       FILTER(?g!='F').
    				 }""")
          if len(quer4)!=0:
             print("Following students are familiar with "+query_input+":")
             for row in quer4:
                print(row["sname"])
          else:
             print("No one is familiar with "+query_input)
    #What does Gregory know?
      elif question==5:
          quer5=g.query("""SELECT DISTINCT ?tn
    		WHERE{   
    				?s rdf:type focu:Student.
                    ?s foaf:name '"""+query_input+"""'.
                    ?s focu:completed ?c.
                    ?st rdf:type rdf:Statement.
                    ?st focu:gradeObtained ?g.
                    ?st rdf:subject ?s.
                    ?st rdf:object ?c.
                    ?c focu:includes ?t.
                    ?t foaf:name ?tn.
                    FILTER(?g!='F').
                    }""")
          if len(quer5)!=0:
                print(query_input+" knows the following topics:")
                for row in quer5:
                    print(row["tn"])
          else:
                print(query_input+" does not know anything!")
       #exit
      elif user_input=="Bye" or user_input=="bye" or user_input=="exit" or user_input=="exit()":
        exit()
       
      else:
        print("Sorry I did not understand!")
              

          