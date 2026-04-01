import traceback
try:
    from langchain import hub
except Exception as e:
    with open("err_out.txt", "w") as f:
        f.write(traceback.format_exc())
