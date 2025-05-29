def Read_File(Myfile):
    #try now to read my file :
    try:
     file=open(Myfile,"r")
     substance=file.read()#The content of the file 
     file.close()
     print(f"File has been read:{substance}")
     return substance
    
    except FileNotFoundError : #exception if file not found or any error fault
         print("File error,file not found!:(")
         try: 
            file=open(Myfile,"w")
            create_new=("New fill will be created due to the undefined one")
            file.write(create_new)
            file.close()
            print("open a new file")
            return create_new
         except Exception as e :
            print("Cannot create a new file:", e)


    except PermissionError : 
       print("NOT AUTHORIZED")
    except UnicodeDecodeError: #sth in the code wrong
       print("Could not read the file an encoding issue occurred ")
    except Exception as e :
       print("Something went wrong")
    return None 
#desktop file will apear the created one 
Read_File(r"C:\Users\admin\Desktop\hoor.txt") # r, read as string
Read_File(r"C:\Users\admin\Desktop\ho.txt")