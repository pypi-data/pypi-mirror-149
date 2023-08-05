import pandas as pd
from jinja2 import Template
from collections import Counter
class markdown:
    """
    This mark down class is used for generate .md file for IdeaScale Project.


    """
    def __init__(self,csv_file=None):
        self.data_frame=pd.read_csv(csv_file,encoding="utf8")
        self.entity_list=self.data_frame["entity"].tolist()
        self.frequency=self.data_frame["frequency"].tolist()
        self.total_entity=len(self.entity_list)
        self.template=Template("Tesla Ideas - Community Highlights \n \n" 
                               
                               "## Executive Summary \n"
                            
                               '## The Challenge \n'
                                "You've shown your commitment to innovation by providing IdeaScale to your workforce, your customer community, and your collaborators. This expansive IdeaScale Community has provided you with ideas that allow for continuous innovation, but only if you are able to organize them and take action. \n \n \n"
                                
                                'Fundamental to the process of acting on ideas is being able to discover what your community has demonstrated to be popular, salient, and impactful.   Similarly, innovation is what people do, not software or databases, so understanding the Members of your community is essential for driving innovation by assembling teams of people with demonstrated interest and expertise. \n'
                               
                               '### Proposed Solution \n'
                               'IdeaScale is committed to providing the tools that will nurture the entire innovation life cycle of an idea from capture to project completion. In that spirit, we are offering this data analysis service which characterizes the key assets in your Community - your Ideas and Members. \n \n'
                               
                               "With IdeaScale, you have experienced how a platform where everyone involved in this innovation process can provide their input for future directions. The Tesla Ideas community at IdeaScale has a wide variety of participants who suggest Ideas based on their experience and desire of what future innovations should be like. \n \n"
                               
                               "We have built a Natural Language Processing (NLP) system which can categorize and highlight the best ideas and contriburors through machine learning on the content and user interactions.  \n \n"
                               
                               "Through this data management we will be able to provide you highlights of some of the innovative Ideas, which might add value to the company and the society as a whole. These Ideas are direct from both the minds of your employees and people all over the globe who strive for change.\n \n"
                               
                               "In addition to characterizing the Ideas and Members of your community, we also highlight Terms and Topic that are discussed repeatedly, offering you the ability to discover what future project areas are brewing in the minds of all contributors. \n \n"
                               
                               "### Value \n"
                               "The overall purpose of this activity is to provide executives with information that is important to their decision making. With the best Ideas filtered through our system from the Tesla Ideas community, you will be able to get the thoughts and perspective from both the employee and customer point of view. These Ideas if nurtured along with the company vision will help create more value and prestige to your innovative brand. \n"

                               "### Final thoughts & next steps \n"
                               "Ideas can shape lives, through this activity we are reaching global participants and creating an interactive community for their input to help us innovate and provide your prestigious company with relevant information which can help the company for not only improving the current products/processes but also create opportunities to tap into the markets which have all the potential to embrace this change. Let us help you in exploring the future directions for the company through Innovative Ideas and make the future better. \n"
                                
                               "## Highlights \n"
                               
                               "### Topics and Ideas \n"
                               
                               "{{total_entity}} Potentially important terms are in common usage.  These may be important to executive management for product or concept development and enhancement \n \n"
                               
                               "Some notable terms are: \n \n"
                            
                               
                               '{% for data in datas %}  - {{data}} \n {% endfor %}'
                               
                              
                               "\n"
                               
                               "### Commonly used terms \n"
                               "86 Terms are both commonly used and highly specific.  These terms are specific to existing Tesla products or concepts and are frequently discussed in the community. \n \n"
                               
                               "Some notable terms are : \n\n"
                               "TODO \n\n"
                               
                               "### Roles \n\n"
                               "33 Roles that are potentially important from both; company and customer perspective for improvement of products and experiences. \n \n"
                               
                               "Some notable roles are: \n \n"
                               "TODO \n\n"

                               "### Tesla product features \n\n"
                               "Tesla product features that are both significant and commonly discussed in the community. These may be important to the executive management to analyze user experience alignment. \n \n"
                               
                               "Some notable features are: \n\n"
                               
                               "TODO \n\n"
                               
                               "### Top contributors \n\n"
                               
                               "These are the top contributors; based on their reputation and input in the community. These members create and add value to the overall discussions on different Tesla products and concepts. \n \n"
                               
                               "Some of the top contributors are: \n\n"
                               
                               "TODO \n\n"
                               
                               "###  Ranking of Ideas based on Reputation \n\n"
                               
                               "#### A.  Top ranked ideas and their Selection and Implementation status \n\n"
                               
                                "TODO \n\n"
                               
                               "#### B.  Top ranked ideas that have been marked Selected and completed \n\n"
                               
                               "TODO \n\n"
                               
                               "#### C.  Top ranked ideas that have been marked Selected but not completed \n\n"

                               "TODO \n\n"
                               
                               "### Tags in common usage \n\n"
                               
                               "TODO \n\n"
                               
                               "### The Trending Terms in your community over the past month are (TBD):\n\n"
                               "TODO \n\n"
                               
                               "### Novel Terms \n\n"
                               
                               "Based on novelty, some interesting terms are: \n\n"
                               "TODO \n\n"
                               
                               "### Locations \n\n"

                                "Significant Locations mentioned in the community are: \n\n"
                               "TODO \n\n"

                                "### People / Person \n\n"
                               
                               "Significant people mentioned in community discussion are : \n\n"
                                "TODO \n\n"
                               
                               "### Acronyms \n\n"
                               "Some significant Acronyms are: \n\n"
                               )


        # self.save='# Potentially Important Terms \n {{counter}} Potentially important terms are in common usage. These maybe be important to executive \n '
        #                        'management for product or concept development and enhancement.'
        #                         '\n \n'
        #                        'Some notable terms are:'
        #                        '{% for data in datas %} {% for element in data %} <li> {{element}} ({{data[element]}} ideas) {% endfor %} {% endfor %}'
        #



    # def summary(self,column_list):
    #     array_data=[]
    #
    #     for column in column_list:
    #         json_data={}
    #         data=self.data_frame[column].tolist()
    #         json_data[column]=dict(Counter(data))
    #         array_data.append(json_data[column])
    #
    #     self.array_data=array_data
    #     ## get total Num of key
    #     counter=0
    #     for data in array_data:
    #         for key in data:
    #             counter+=1
    #     self.counter=counter
    #

    def write(self):
        """
        This function will create a readme.md file which is generated by the self.template

        """
        with open("readme.md",'w') as f:
            f.write(self.template.render(total_entity=self.total_entity,datas=self.entity_list))
