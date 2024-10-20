from flask import Flask, render_template, has_request_context, request, make_response, jsonify
import lxml.etree
from flask.logging import default_handler
from model import *


persons = [
    ["5868362072458741","Oracle", "FREC_Au8LPI7XtzGl84xF35b5slqopmakeGaf", "SDIUR_@#U" ],
    ["6401603733788605","Morpheus", "FREC_gtlcQY7kLIzyt62YXB2LfEFXUzf7VZF5", "IRVSE_&*%" ],
    ["1132041719025981","Trinity", "FREC_yLYI981Dgg8wfGT3MWy8H0mMJyy3qQq1", "LOVNR_!M^" ],
    ["0755720730387431","Cypher", "FREC_XGN62TKewI6NwOj0y4LJWLH7IJrcbHK7", "VNEYR_&E!" ],
    ["4250280188899889","Switch", "FREC_ERbj6bspjsvG5HD3NTnoaYqRs8TLPqmq", "BUNWP_VO#" ],
    ["6706870133920526","Apoc", "FREC_uoX8JQHimqQJZ9JwZyYwcNhmfFyVXhWA", "AWOTR_N!$"],
]

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def start():
    
    # Return main page
    if request.method == 'GET':
                
        #Creating SQLite db and table
        try:
            create_table()
            for element in persons:
                insert_person(element[0], element[1], element[2], element[3])
        except:
            return "Opps Error. DB not initialized"
        
        return render_template("index.html")
    
    #Handle user input
    if request.method == 'POST':
            
        try:
            xml_src = request.get_data()
            print(xml_src)
            
            if ".dtd" in str(xml_src): # Blind XXE via error, need attacker own server
                parser = lxml.etree.XMLParser(resolve_entities=True, no_network=False, huge_tree=True)
                doc = lxml.etree.fromstring(xml_src, parser=parser) 
                result = parser.error_log
                data = {
                    "data" : parser.error_log
                }

                return jsonify(data)
            
            elif "file:///" in str(xml_src): # Add vulnerable func if user input file://  XXE
                parser = lxml.etree.XMLParser(resolve_entities=True, no_network=False, huge_tree=True)
                doc = lxml.etree.fromstring(xml_src, parser=parser)
                data = {
                    "data" : str(lxml.etree.tostring(doc))
                }
                return jsonify(data) 
            
            # Return standard data if no error returned
            else:
                parser = lxml.etree.XMLParser(resolve_entities=True, no_network=False, huge_tree=True)
                doc = lxml.etree.fromstring(xml_src, parser=parser)
                frequency = doc[0].text
                data = {
                    "data" : {
                        "Id" : check(frequency.strip())[0][0],
                        "Name" : check(frequency.strip())[0][1],
                        "Frequency" : check(frequency.strip())[0][2],
                        "SecretCode" : check(frequency.strip())[0][3],
                    }
                }
                return jsonify(data)
        except:
            return "Something get wrong. Try again!"


if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0')
    

    