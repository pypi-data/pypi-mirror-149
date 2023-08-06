import os
import shutil
import textile
import templ8.programstate
import pypandoc
from templ8.blessing import makedir
from templ8.blessing import mod_replaces
from templ8.blessing import parse_content

# Divines a website
def divine():
    state = templ8.programstate.ProgramState()
    for subdir, dirs, files in os.walk(state.input_folder):
        for dir in dirs:
            path = os.path.join(subdir, dir).replace(state.input_folder, state.output_folder, 1)
            makedir(path)
            
        for file in files:
            path = os.path.join(subdir, file)
            file_extension = os.path.splitext(path)[1]
            outpath = path.replace(state.input_folder, state.output_folder, 1)
            outhtml = outpath.replace(file_extension, ".html", -1)
            if file_extension in [".textile", ".md"]:
                with open(path, "r") as f:
                    contents = ""
                    file_split = f.read().split("-BEGINFILE-")
                    file_headers = ""
                    file_content = ""
                    if len(file_split) == 2:
                        file_headers = file_split[0]
                        file_content = file_split[1]
                    elif len(file_split) == 1:
                        file_headers = ""
                        file_content = file_split[0]
                    else:
                        raise Exception("More than one -BEGINFILE- markers")
                    
                    # Check if the folder is in txignore
                    in_txignore = False
                    for i in state.txignore:
                        if os.path.join(state.input_folder, os.path.normpath(i)) == path or os.path.join(state.input_folder, os.path.normpath(i)) == subdir:
                            in_txignore = True
                            break
                          
                    
                    if not in_txignore:
                        filerepl = state.replacements.copy()
                        mod_replaces(filerepl, file_headers)
                        
                        
                        # Turn the content into HTML
                        contents = parse_content(file_content, file_extension)
                        
                        # Put the content in the base HTML
                        if not "CUSTOMBASE" in filerepl:
                            contents = state.basehtml_content.replace("##CONTENT##", contents)
                        else:
                            if os.path.exists(filerepl["CUSTOMBASE"]):
                                contents = open(filerepl["CUSTOMBASE"], "r").read().replace("##CONTENT##", contents)
                            else:
                                raise Exception(os.path.join(subdir, file) + " uses a CUSTOMBASE that doesn't exist")
                        
                        
                        for key in filerepl:
                            contents = contents.replace("##"+key+"##", filerepl[key])
                            
                        with open(outhtml, "w") as f:
                            f.write(contents)
                    else:
                        with open(outpath, "w") as f:
                            f.write(file_content)
                    
                    
                    
            elif not os.path.exists(outpath):
                shutil.copy(path, outpath)
    

    print("Finished assembling")