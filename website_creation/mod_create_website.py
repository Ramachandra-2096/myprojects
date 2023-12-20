from .mod_create_html import create_html as ch
import os
def website_creation(college,file1,template):
    file1 = file1
    college =college
    """ The below function is for reading and saving the file content """
    def content_creation(file2):
        f1 =open(file2,'r')
        years = []
        subjects = []
        names = []
        lines = f1.readlines()
        for line in lines:
            words = line.split(':')
            if not words[0] in years:
                years.append(words[0])
            subjects.append(words[1])
            names.append(words[2].replace('\n','').split(','))
        return(years,subjects,names)
    
    
    """The below function is to create the directory structure """
    def Directory_creation(college,years,subjects,names):
        import os
        for year in years:
            for  i in range(len(subjects)):
                for j in range(len(names[i])):
                    os.makedirs(os.path.join('dirs',college+'/'+year+'/'+subjects[i]+'/'+names[i][j]),exist_ok =True)
        


    """This below function will help to create files inside a folder """
    def file_creation(root_directory,template):
        
        for root, dirs, files in os.walk(root_directory):
            if not dirs:
                dir_name = os.path.basename(root)
                with open(os.path.join(root, dir_name + '.html'), 'w') as file1:
                        ch(template,dir_name,os.path.basename(os.path.abspath(os.path.join(root, os.pardir))),file1)
    
    #call all the functions here for making it easy to use for User
    years,subjects,names = content_creation(file1)
    Directory_creation(college,years,subjects,names)
    file_creation(os.path.join('dirs',college),template)             
    return "Directory and Files are created successfully"